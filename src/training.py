"""
training.py — Loop de entrenamiento Adam + L-BFGS
==================================================
Proyecto : Simulacion Acelerada de Speckle Optico mediante PINNs
Autor    : Roberto Hernandez Estrada
Director : Dr. Jose Adan Hernandez Nolasco — UJAT

Nota: training.py es una referencia documentada del loop de entrenamiento.
Los notebooks NB01 y NB02 tienen el loop inline por legibilidad pedagogica.
Este archivo puede usarse en NB03+ para simplificar el codigo.

Funcion principal:
    train_adam_lbfgs — entrena con Adam (early stopping) + L-BFGS

Uso (opcional, desde NB03+):
    from src.training import train_adam_lbfgs
"""

import time
import torch


def train_adam_lbfgs(model, loss_fn, loss_kwargs, config, device, verbose=True):
    """
    Entrenamiento hibrido Adam + L-BFGS para PINNs de Helmholtz.

    Args:
        model       : PINN_1D_SIREN o PINN_2D_SIREN
        loss_fn     : pinn_loss_1d o pinn_loss_2d
        loss_kwargs : argumentos para loss_fn (sin model)
        config      : CONFIG del notebook con claves:
                        n_epochs, lr, patience, lbfgs_max_iter,
                        lbfgs_history, seed
        device      : torch.device
        verbose     : imprimir progreso

    Returns:
        dict con history, history_lbfgs, epoch_final,
             iter_lbfgs, best_loss, tiempo_adam, tiempo_lbfgs
    """
    torch.manual_seed(config['seed'])
    torch.cuda.manual_seed(config['seed'])

    optimizer  = torch.optim.Adam(model.parameters(), lr=config['lr'])
    history    = {'total': [], 'data': [], 'physics': []}
    PATIENCE   = config.get('patience', 800)
    MIN_DELTA  = 1e-7
    best_loss  = float('inf')
    best_state = None
    sin_mejora = 0
    epoch_final = config['n_epochs']

    t0_adam = time.time()

    for epoch in range(config['n_epochs']):
        optimizer.zero_grad()
        loss, loss_data, loss_physics = loss_fn(model=model, **loss_kwargs)
        loss.backward()
        optimizer.step()

        current_loss = loss.item()
        history['total'].append(current_loss)
        history['data'].append(loss_data.item())
        history['physics'].append(loss_physics.item())

        if current_loss < best_loss - MIN_DELTA:
            best_loss  = current_loss
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
            sin_mejora = 0
        else:
            sin_mejora += 1

        if verbose and (epoch + 1) % 1000 == 0:
            elapsed = time.time() - t0_adam
            print(f'  Epoca {epoch+1:5d} | L_total: {current_loss:.3e} | '
                  f'Mejor: {best_loss:.3e} | Sin mejora: {sin_mejora} | '
                  f'Tiempo: {elapsed:.1f} s')

        if sin_mejora >= PATIENCE:
            epoch_final = epoch + 1
            if verbose:
                print(f'\n  Early stopping en epoca {epoch_final}')
            model.load_state_dict(best_state)
            break

    tiempo_adam = time.time() - t0_adam

    # ── L-BFGS ────────────────────────────────────────────────────────────────
    optimizer_lbfgs = torch.optim.LBFGS(
        model.parameters(),
        lr             = 1.0,
        max_iter       = config.get('lbfgs_max_iter', 1000),
        history_size   = config.get('lbfgs_history', 100),
        line_search_fn = 'strong_wolfe'
    )

    history_lbfgs = {'total': [], 'data': [], 'physics': []}
    iter_count    = [0]
    t0_lbfgs      = time.time()

    def closure():
        optimizer_lbfgs.zero_grad()
        loss, loss_data, loss_physics = loss_fn(model=model, **loss_kwargs)
        loss.backward()
        history_lbfgs['total'].append(loss.item())
        history_lbfgs['data'].append(loss_data.item())
        history_lbfgs['physics'].append(loss_physics.item())
        iter_count[0] += 1
        return loss

    optimizer_lbfgs.step(closure)
    tiempo_lbfgs = time.time() - t0_lbfgs

    return {
        'history'       : history,
        'history_lbfgs' : history_lbfgs,
        'epoch_final'   : epoch_final,
        'iter_lbfgs'    : iter_count[0],
        'best_loss'     : best_loss,
        'tiempo_adam'   : tiempo_adam,
        'tiempo_lbfgs'  : tiempo_lbfgs,
    }
