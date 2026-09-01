# Positioning — PINN-SIREN for Optical Speckle Simulation

Project: `pinn-speckle` | Compiled: 2026-08-27 | Revised: 2026-08-27 (round 1 fixes)

Note: per the librarian's mandate, this file suggests a contribution statement and
differentiation points for the writer/strategist to use or revise — it does not
constitute the final claim, which the writer owns and the writer-critic scores.

## Suggested contribution statement (draft, for writer to adapt)

> We present, to our knowledge, the first physics-informed neural network with sinusoidal
> (SIREN) activation applied end-to-end to the 2D scalar Helmholtz equation in an explicitly
> optical regime (λ = 638 nm), validated in two stages: (i) against closed-form analytical
> solutions in 1D and 2D, achieving relative L2 error of 0.006% and 0.171% respectively —
> one to three orders of magnitude below the closest comparable published benchmarks
> (Schoder & Kraxberger 2024: 2.490%; Zhang et al. 2025, FE-PIRBN: 1.40–5.82%; Huang et al.
> 2026: ~10% for TM polarization; Panagiotakopoulos et al. 2026 report no quantitative L2
> benchmark for their SIREN-based 2D Helmholtz solver); and (ii) by generating optical
> speckle from a random-phase rough boundary condition and confirming statistical
> consistency with Goodman's (2007) fully-developed-speckle criteria (contrast C ≈ 1,
> Kolmogorov–Smirnov test against the negative-exponential intensity distribution). We
> further propose and validate a simple calibration rule, ω₀ ≈ k/(2π), linking the SIREN
> frequency hyperparameter to the physical wavenumber — addressing a gap-tuning step left
> unspecified in both Sitzmann et al. (2020) and Panagiotakopoulos et al. (2026), the only
> other SIREN-based 2D complex Helmholtz solver found in this search.

## Differentiation points, by nearest competitor

| Nearest paper | What they do | What this thesis does differently |
|---|---|---|
| Panagiotakopoulos, Velissaris & Rapsomanikis (2026), UCF STARS repository deposit | SIREN + complex-valued 2D Helmholtz + Adam-then-L-BFGS, Gaussian source + Sommerfeld radiation BC, dielectric-inclusion scattering; qualitative wave-behavior validation, no L2-vs-analytical benchmark, no DOI/peer review yet | Same core architecture/optimizer pipeline, but adds: quantitative L2-vs-analytical validation (0.006%/0.171%); the ω₀ ≈ k/(2π) calibration rule (absent in their work); a rough random-phase boundary condition generating optical speckle (they use a fixed Gaussian source, no speckle); Goodman (2007) statistical validation (C ≈ 1, KS test) — entirely absent from their qualitative approach |
| Huang et al. (2026), arXiv:2607.27349 | PINN (tanh-smoothed MLP) for 2D optical/EM plane-wave scattering off dielectric structures; L2 ≈ 10% (TM) | SIREN with explicit ω₀-vs-k calibration; forward generation of speckle from a random-phase boundary (not scattering off a fixed geometric object); L2 two orders of magnitude lower on the validation stage |
| Geetanjli & Hiremath (2026) | PINN (sigmoid) for optical waveguide eigenmodes, L2 vs. analytical | Different problem class (eigenvalue/mode profile vs. forward field with known source/BC); SIREN vs. sigmoid; adds the speckle-generation stage entirely absent here |
| Kazemzadeh et al. (2025) | Data-driven modal-superposition network fit to *measured* fiber speckle; ELU/tanh; MAE/SSIM against experimental ground truth | This thesis solves the governing PDE from scratch given a random boundary condition — no experimental calibration, no modal-superposition ansatz; validation is against a statistical model (Goodman) rather than a specific measured pattern, so it demonstrates *simulation* capability, not *reconstruction* of one physical fiber |
| Guo et al. (2025) | Physics-informed CycleGAN for speckle *denoising*, using Goodman's negative-exponential statistics as a loss term | This thesis performs the inverse task at the physics level: it *generates* speckle consistent with the same statistics, rather than removing it from an image; GAN vs. PINN; image-domain vs. PDE-domain |
| Rincón-Cardeño et al. (2025) | Confirms sine activation as empirically best for acoustic Helmholtz PINN vs. BEM | Optical vs. acoustic domain; adds the explicit ω₀ ≈ k/(2π) calibration rule this benchmarking paper does not propose |
| Zhang et al. (2025), FE-PIRBN | Radial-basis PINN variant for high-frequency EM scattering, 1.40–5.82% L2, published in JCP (top target journal) | SIREN/MLP vs. radial-basis architecture; optical vs. generic EM; lower error; adds the speckle-generation application this paper does not attempt |

## Framing recommendation for the introduction

Three-way positioning table for the writer:

| | PINN + Helmholtz, non-optical | PINN + optical Helmholtz, no speckle | Speckle + ML, non-forward-PDE |
|---|---|---|---|
| Representative work | Schoder & Kraxberger 2024; Rincón-Cardeño et al. 2025; Zhang et al. 2025; Nair et al. 2025 | Geetanjli & Hiremath 2026; Huang et al. 2026; Panagiotakopoulos et al. 2026; Chen et al. 2020 | Kazemzadeh et al. 2025; Guo et al. 2025 |
| This thesis | Optical, not acoustic/generic | Adds SIREN + ω₀ calibration + speckle (Panagiotakopoulos et al. 2026 is the closest architecturally — SIREN + complex Helmholtz — but lacks the calibration rule, speckle generation, and quantitative L2 benchmark) | Adds forward PDE-based generation, not fitting/denoising |

This thesis is the only cell that is optical + SIREN + Helmholtz + speckle-generation +
statistically validated against Goodman (2007) simultaneously. Panagiotakopoulos et al.
(2026) is the paper requiring the most explicit contrast sentence in the introduction, given
the shared SIREN + complex-Helmholtz + Adam/L-BFGS pipeline.

## Journal/venue implication

Given the frontier map, `Journal of Computational Physics` (where FE-PIRBN appears) and
`Optics Express` / `JOSA A` (optical-domain, statistical-optics readership familiar with
Goodman's framework) are both defensible targets — JCP reviewers will expect direct
comparison to FE-PIRBN, Huang et al., and Panagiotakopoulos et al.'s reported results;
Optics Express/JOSA A reviewers will weight the Goodman-consistency validation more heavily
than the raw L2 figure. Final venue choice is an Orchestrator/user decision, not the
librarian's — flagging only that the literature found supports both framings.
