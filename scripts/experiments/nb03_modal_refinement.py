"""Controlled refinement of saved NB03 checkpoints; no reference labels in training.

Run from project root: python scripts/experiments/nb03_modal_refinement.py --help
"""
import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time

os.environ.setdefault('MPLBACKEND', 'Agg')
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
import torch
from torch.func import jvp
from scripts.experiments import nb03_modal_multiseed_summary as previous
from scripts.experiments import nb03_modal_pinn_siren as modal
from scripts.experiments import nb03_pinn_slabs as base


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def residual_values(model, coordinates, kz2):
    scale = model.correction_scale.reshape(1, -1, 2)
    return modal.modal_residual(model, coordinates, kz2) / scale


def residual_score(model, coordinates, kz2):
    chunks = []
    for chunk in coordinates.split(256):
        chunks.append(residual_values(model, chunk, kz2).detach())
    values = torch.cat(chunks).cpu().numpy()
    return {'mse': float(np.mean(values ** 2)),
            'rmse': float(np.sqrt(np.mean(values ** 2))),
            'max_abs': float(np.max(np.abs(values))),
            'p99_abs': float(np.quantile(np.abs(values), .99))}


def evaluate(model, ref, field_scale, kx, kz2):
    dtype = next(model.parameters()).dtype
    # Independent test grid, never used to select a checkpoint.
    z_test = torch.tensor(np.linspace(0, 1, 2001), dtype=dtype).reshape(-1, 1)
    test_residual = residual_score(model, z_test, kz2)
    z = np.linspace(0, 1, 201)
    with torch.no_grad():
        values = model(torch.tensor(z, dtype=dtype).reshape(-1, 1))
    values = values.cpu().numpy().reshape(len(z), -1, 2)
    coeff = values[..., 0] + 1j * values[..., 1]
    phase = np.exp(1j * np.outer(ref['x_lambda'], kx))
    pred = field_scale * (coeff @ phase.T)
    spectrum = np.fft.fft(np.exp(1j * ref['phase']))
    all_kz = np.sqrt((base.K ** 2 - ref['kx'] ** 2).astype(complex))
    full = np.fft.ifft(spectrum[None, :] * np.exp(1j * z[:, None] * all_kz), axis=1)
    active = ref['propagating_mask'].astype(bool)
    prop = np.fft.ifft(np.where(active, np.fft.fft(full, axis=1), 0), axis=1)
    full_norm = np.linalg.norm(full, axis=1)
    prop_norm = np.linalg.norm(prop, axis=1)
    l2_full = np.linalg.norm(pred - full, axis=1) / full_norm
    l2_prop = np.linalg.norm(pred - prop, axis=1) / prop_norm
    floor = np.linalg.norm(full - prop, axis=1) / full_norm
    neural_common = np.linalg.norm(pred - prop, axis=1) / full_norm
    identity = np.max(np.abs(l2_full ** 2 - floor ** 2 - neural_common ** 2))
    assert identity < 1e-10, identity
    assert np.isfinite(pred).all()
    z0 = torch.zeros((1, 1), dtype=dtype)
    value0, dz0 = jvp(model, (z0,), (torch.ones_like(z0),))
    boundary_error = float((value0 - model.coefficient0).abs().max().detach())
    derivative_error = float((dz0 - model.derivative0).abs().max().detach())
    assert boundary_error < 1e-6 and derivative_error < 1e-6
    metrics = base.complex_field_metrics(pred[-1], full[-1])
    c_full = base.intensity_statistics(full[-1])['contrast']
    c_pred = base.intensity_statistics(pred[-1])['contrast']
    result = {
        'l2_full_final': float(l2_full[-1]),
        'l2_propagating_final': float(l2_prop[-1]),
        'l2_propagating_max': float(l2_prop.max()),
        'l2_propagating_max_z': float(z[np.argmax(l2_prop)]),
        'l2_full_max': float(l2_full.max()),
        'evanescent_floor_final': float(floor[-1]),
        'coherence_full_final': metrics['target_complex_coherence'],
        'intensity_correlation_full_final': metrics['target_intensity_pearson_correlation'],
        'contrast_full': c_full, 'contrast_pinn': c_pred,
        'contrast_difference': abs(c_pred - c_full),
        'original_contrast_rule_pass': abs(c_pred - 1) < .1,
        'test_residual': test_residual,
        'cauchy_field_max_abs': boundary_error,
        'cauchy_derivative_max_abs': derivative_error,
        'spectral_error_identity_max_abs': float(identity),
    }
    return result, {'z_lambda': z, 'l2_full': l2_full, 'l2_propagating': l2_prop,
                    'evanescent_floor': floor, 'field_pred': pred,
                    'field_full': full, 'field_propagating': prop}


def train(model, ref, arm, seconds, n_train, learning_rate=None,
          selection_interval=10):
    if selection_interval < 1:
        raise ValueError('selection_interval must be positive')
    dtype = next(model.parameters()).dtype
    active = ref['propagating_mask'].astype(bool)
    kz2 = torch.tensor(np.maximum(base.K ** 2 - ref['kx'][active] ** 2, 0), dtype=dtype)
    # Identical fixed collocation for all arms, no random closure re-sampling.
    z_train = torch.tensor((np.arange(n_train) + .5) / n_train, dtype=dtype).reshape(-1, 1)
    z_selection = torch.tensor(np.random.default_rng(1717).uniform(size=997),
                               dtype=dtype).reshape(-1, 1)
    initial = residual_score(model, z_selection, kz2)
    best_mse = initial['mse']
    best_state = copy.deepcopy(model.state_dict())
    best_step = 0
    history = [{'step': 0, 'seconds': 0., 'selection_mse': best_mse}]
    if arm == 'adam32':
        adam_lr = 5e-5 if learning_rate is None else float(learning_rate)
        optimizer = torch.optim.Adam(model.parameters(), lr=adam_lr)
    else:
        optimizer = torch.optim.LBFGS(model.parameters(), lr=1., max_iter=10,
                                     max_eval=15, history_size=50,
                                     tolerance_grad=1e-10, tolerance_change=1e-12,
                                     line_search_fn='strong_wolfe')
    closure_calls = 0
    step = 0
    t0 = time.perf_counter()

    def closure():
        nonlocal closure_calls
        optimizer.zero_grad(set_to_none=True)
        loss = residual_values(model, z_train, kz2).square().mean()
        if not torch.isfinite(loss):
            raise FloatingPointError('Nonfinite physical loss')
        loss.backward()
        if arm == 'adam32':
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)
        closure_calls += 1
        return loss

    while time.perf_counter() - t0 < seconds:
        if arm == 'adam32':
            elapsed_fraction = min((time.perf_counter() - t0) / seconds, 1.)
            min_lr = adam_lr * .02
            optimizer.param_groups[0]['lr'] = min_lr + .5 * (adam_lr - min_lr) * (
                1 + math.cos(math.pi * elapsed_fraction))
            closure()
            optimizer.step()
        else:
            optimizer.step(closure)
        step += 1
        if arm != 'adam32' or step % selection_interval == 0:
            score = residual_score(model, z_selection, kz2)
            if score['mse'] < best_mse:
                best_mse = score['mse']
                best_state = copy.deepcopy(model.state_dict())
                best_step = step
            history.append({'step': step, 'seconds': time.perf_counter() - t0,
                            'selection_mse': score['mse']})
    # Include the last state even if the Adam evaluation interval was not reached.
    score = residual_score(model, z_selection, kz2)
    if score['mse'] < best_mse:
        best_mse, best_state, best_step = score['mse'], copy.deepcopy(model.state_dict()), step
    elapsed = time.perf_counter() - t0
    model.load_state_dict(best_state)
    verified = residual_score(model, z_selection, kz2)['mse']
    assert np.isclose(verified, best_mse, rtol=1e-6, atol=1e-12)
    return kz2, {'seconds': elapsed, 'budget_seconds': seconds, 'steps': step,
                 'closure_calls': closure_calls, 'best_step': best_step,
                 'learning_rate_initial': adam_lr if arm == 'adam32' else None,
                 'selection_initial_mse': initial['mse'], 'selection_best_mse': verified,
                 'history': history, 'optimizer_state_resumed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seeds', type=int, nargs='+', default=[42, 123])
    parser.add_argument('--arms', nargs='+', choices=['adam32', 'lbfgs32', 'lbfgs64'],
                        default=['adam32', 'lbfgs32', 'lbfgs64'])
    parser.add_argument('--seconds', type=float, default=60.)
    parser.add_argument('--n-train', type=int, default=1024)
    parser.add_argument('--threads', type=int, default=4)
    parser.add_argument('--name', default='pilot1')
    args = parser.parse_args()
    if args.seconds <= 0 or args.n_train < 2 or args.threads < 1:
        parser.error('seconds, n-train and threads must be positive')
    if not args.name.replace('_', '').replace('-', '').isalnum():
        parser.error('name must be an alphanumeric label')
    out = ROOT / 'results' / 'nb03_refinement' / args.name
    out.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(args.threads)
    torch.manual_seed(42)
    # Lock architecture; inherited NB03 environment overrides must not change the pilot.
    modal.HIDDEN_DIM, modal.NUM_LAYERS = 128, 4
    modal.FIRST_OMEGA, modal.HIDDEN_OMEGA = 30., 1.
    summary = {'configuration': vars(args),
               'runtime': {'python': sys.version, 'torch': torch.__version__,
                           'numpy': np.__version__, 'platform': platform.platform(),
                           'device': 'cpu', 'threads': torch.get_num_threads()},
               'source_sha256': digest(Path(__file__)),
               'protocol': 'Continue the same saved 8000-epoch Adam weights in each arm. '
                           'Fixed training points; post-update checkpoint selection on 997 fixed '
                           'random points; independent 2001-point residual test and 201 field planes. '
                           'No field labels for training/selection. All inherited float32 boundary '
                           'buffers are cast, not recomputed, in float64.',
               'cases': []}
    for seed in args.seeds:
        case = next(c for c in previous.CASES if c[0] == seed)
        ref_path = ROOT / 'results' / f'nb03_angular_spectrum_reference{case[1]}.npz'
        model_path = ROOT / 'results' / 'models' / f'nb03_modal_pinn_siren{case[3]}.pt'
        ref = dict(np.load(ref_path))
        original, scale, kx = previous.build_model(ref, model_path)
        original_kz2 = torch.tensor(np.maximum(base.K ** 2 - kx ** 2, 0), dtype=torch.float32)
        baseline, base_arrays = evaluate(original, ref, scale, kx, original_kz2)
        np.savez_compressed(out / f'seed{seed}_baseline.npz', **base_arrays)
        entry = {'seed': seed, 'input_model': str(model_path),
                 'input_model_sha256': digest(model_path), 'reference_sha256': digest(ref_path),
                 'baseline': baseline, 'arms': {}}
        summary['cases'].append(entry)
        for arm in args.arms:
            model = copy.deepcopy(original).to(dtype=torch.float64 if arm.endswith('64') else torch.float32)
            print(f'Seed {seed}, {arm}, budget {args.seconds}s', flush=True)
            kz2, training = train(model, ref, arm, args.seconds, args.n_train)
            metrics, arrays = evaluate(model, ref, scale, kx, kz2)
            entry['arms'][arm] = {'training': training, 'metrics': metrics}
            torch.save(model.state_dict(), out / f'seed{seed}_{arm}.pt')
            np.savez_compressed(out / f'seed{seed}_{arm}.npz', **arrays)
            (out / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
            print(f'  prop={100*metrics["l2_propagating_final"]:.4f}% '
                  f'full={100*metrics["l2_full_final"]:.4f}% '
                  f'max_prop={100*metrics["l2_propagating_max"]:.4f}% '
                  f'residual={metrics["test_residual"]["rmse"]:.3e} '
                  f'seconds={training["seconds"]:.1f}', flush=True)
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, len(summary['cases']), figsize=(6 * len(summary['cases']), 4.5), squeeze=False)
    for ax, entry in zip(axes[0], summary['cases']):
        seed = entry['seed']
        for arm in ['baseline'] + args.arms:
            data = np.load(out / f'seed{seed}_{arm}.npz')
            ax.plot(data['z_lambda'], data['l2_propagating'] * 100, label=arm)
        ax.set(title=f'Pantalla {seed}: referencia propagante', xlabel='z/lambda', ylabel='L2 (%)')
        ax.grid(alpha=.25)
        ax.legend()
    fig.tight_layout()
    fig.savefig(out / 'comparison.png', dpi=150)
    plt.close(fig)
    print(f'Completed: {out}', flush=True)


if __name__ == '__main__':
    main()
