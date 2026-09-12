"""Combine the two-screen pilot and three-screen L-BFGS confirmation.

Reads existing artifacts, verifies metrics and preserves the historical runs.
"""
from pathlib import Path
import hashlib
import json
import os
import numpy as np

os.environ.setdefault('MPLBACKEND', 'Agg')
ROOT = Path(__file__).resolve().parents[2]
RUNS = [('pilot1', {42, 123}), ('confirmation3', {321, 777, 2026})]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stats(values):
    a = np.asarray(values, dtype=float)
    return {'mean': float(a.mean()), 'std_population': float(a.std()),
            'min': float(a.min()), 'max': float(a.max())}


def main():
    rows, curves, histories = [], [], []
    for run, seeds in RUNS:
        folder = ROOT / 'results' / 'nb03_refinement' / run
        summary_path = folder / 'summary.json'
        data = json.loads(summary_path.read_text())
        config = data['configuration']
        assert config['seconds'] == 60 and config['n_train'] == 1024 and config['threads'] == 4
        histories.append({'path': str(summary_path.relative_to(ROOT)), 'sha256': sha(summary_path),
                          'source_sha256': data['source_sha256'], 'runtime': data['runtime']})
        assert {c['seed'] for c in data['cases']} == seeds
        for case in data['cases']:
            seed = case['seed']
            assert sha(Path(case['input_model'])) == case['input_model_sha256']
            arm = case['arms']['lbfgs32']
            metrics = arm['metrics']
            path = folder / f'seed{seed}_lbfgs32.npz'
            arrays = dict(np.load(path))
            old = dict(np.load(folder / f'seed{seed}_baseline.npz'))
            assert all(np.isfinite(a).all() for a in arrays.values())
            p, full, prop = [arrays[k] for k in ['field_pred', 'field_full', 'field_propagating']]
            full_l2 = np.linalg.norm(p-full, axis=1) / np.linalg.norm(full, axis=1)
            prop_l2 = np.linalg.norm(p-prop, axis=1) / np.linalg.norm(prop, axis=1)
            np.testing.assert_allclose(full_l2, arrays['l2_full'], rtol=1e-10, atol=1e-12)
            np.testing.assert_allclose(prop_l2, arrays['l2_propagating'], rtol=1e-10, atol=1e-12)
            assert abs(full_l2[-1]-metrics['l2_full_final']) < 1e-12
            assert abs(prop_l2[-1]-metrics['l2_propagating_final']) < 1e-12
            curves.append({'seed': seed, 'z': arrays['z_lambda'],
                           'before': old['l2_propagating'], 'after': prop_l2})
            rows.append({'seed': seed, 'run': run, 'baseline': case['baseline'],
                         'refined': metrics, 'training': arm['training'],
                         'model_path': str((folder / f'seed{seed}_lbfgs32.pt').relative_to(ROOT)),
                         'model_sha256': sha(folder / f'seed{seed}_lbfgs32.pt')})
    assert len({r['seed'] for r in rows}) == 5
    assert histories[0]['source_sha256'] == histories[1]['source_sha256']
    rows.sort(key=lambda r:r['seed'])
    agg = {side: {key: stats([r[side][key] for r in rows]) for key in
                  ['l2_propagating_final', 'l2_propagating_max', 'l2_full_final',
                   'contrast_difference']} for side in ['baseline', 'refined']}
    agg['residual_rmse'] = stats([r['refined']['test_residual']['rmse'] for r in rows])
    agg['additional_seconds_total'] = sum(r['training']['seconds'] for r in rows)
    agg['propagating_final_below_1pct_count'] = sum(r['refined']['l2_propagating_final'] < .01 for r in rows)
    agg['propagating_all_201_planes_below_1pct_count'] = sum(r['refined']['l2_propagating_max'] < .01 for r in rows)
    agg['full_final_below_5pct_count'] = sum(r['refined']['l2_full_final'] < .05 for r in rows)
    agg['original_contrast_rule_pass_count'] = sum(r['refined']['original_contrast_rule_pass'] for r in rows)
    out = ROOT / 'results' / 'nb03_refinement' / 'five_screen_lbfgs32'
    out.mkdir(exist_ok=True)
    report = {'scope': 'Five known screens, each independently trained; same architecture and fixed '
                       '60-second L-BFGS float32 refinement. Not held-out screens or optimizer seeds.',
              'sources': histories, 'per_screen': rows, 'aggregate': agg}
    (out / 'summary.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    lines = ['# NB03: confirmación de L-BFGS float32 en cinco pantallas', '',
             'Se completó el mismo protocolo en las pantallas 321, 777 y 2026 y se combinaron',
             'con el piloto 42/123. Cada corrida continúa sus propios pesos de 8000 épocas Adam.', '',
             '| Pantalla | Propagante antes | Propagante después | Máximo propagante después | Completo después | RMSE modal | Segundos adicionales |',
             '|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        b, m = r['baseline'], r['refined']
        lines.append(f"| {r['seed']} | {100*b['l2_propagating_final']:.4f}% | {100*m['l2_propagating_final']:.4f}% | {100*m['l2_propagating_max']:.4f}% | {100*m['l2_full_final']:.4f}% | {m['test_residual']['rmse']:.5f} | {r['training']['seconds']:.2f} |")
    lines += ['', f"Error propagante final medio: {100*agg['refined']['l2_propagating_final']['mean']:.4f}%.",
              f"Error completo final medio: {100*agg['refined']['l2_full_final']['mean']:.4f}%.",
              f"Tiempo adicional acumulado: {agg['additional_seconds_total']:.2f} s (no incluye los entrenamientos Adam anteriores).", '',
              '## Interpretación y límites', '',
              '- Las referencias completa y propagante se identifican por separado.',
              '- El campo completo conserva componentes evanescentes ausentes en los 41 modos de la red.',
              '- Los máximos se refieren a 201 planos; no son cotas continuas ni máximos del error completo.',
              '- La selección de pesos usa únicamente residuo físico en 997 puntos fijos; la prueba usa 2001 puntos.',
              '- Se conservaron las condiciones de Cauchy de la entrada proyectada.',
              '- Las cinco pantallas son conocidas, cada una tiene su propio entrenamiento y la semilla de red sigue fija.',
              '- El umbral exploratorio de fidelidad de contraste no reemplaza la hipótesis original contra C=1.',
              '- No se incorporaron evanescentes ni se ensayaron nuevas distancias, FEM o mediciones ópticas.', '',
              '## Reproducción', '', 'Desde la raíz del proyecto:', '', '```powershell',
              'python -u scripts/experiments/nb03_modal_refinement.py --seeds 321 777 2026 --arms lbfgs32 --seconds 60 --name replica_confirmation',
              '```', '', 'El nombre de salida debe ser nuevo. Los resultados originales están en `confirmation3`.',
              'La consolidación lee `pilot1` y `confirmation3`:', '', '```powershell',
              'python scripts/experiments/nb03_refinement_summary.py', '```', '',
              'Se verificaron los NPZ frente a las métricas JSON y los hashes de los modelos históricos.',
              'Configuraciones, modelos, versiones y trazabilidad: [summary.json](summary.json).', '',
              '![Error propagante antes y después](comparison.png)', '']
    (out / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True, constrained_layout=True)
    for c in curves:
        axes[0].plot(c['z'], 100*c['before'], label=str(c['seed']))
        axes[1].plot(c['z'], 100*c['after'], label=str(c['seed']))
    for ax, title in zip(axes, ['Antes: Adam', 'Después: Adam + L-BFGS float32']):
        ax.axhline(1, color='black', ls='--', lw=1, label='1%')
        ax.set(title=title, xlabel='z/lambda', ylabel='L2 propagante (%)')
        ax.grid(alpha=.25)
        ax.legend(ncol=2, title='Pantalla')
    fig.savefig(out / 'comparison.png', dpi=170)
    plt.close(fig)
    print(json.dumps(agg, indent=2))
    print(out)


if __name__ == '__main__':
    main()
