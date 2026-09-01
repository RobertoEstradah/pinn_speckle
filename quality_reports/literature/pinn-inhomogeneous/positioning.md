# Positioning — PINNs for the Helmholtz Equation in Inhomogeneous Media (Fase 2)

Project: `pinn-inhomogeneous` | Compiled: 2026-09-01 | **Round 2 corrections: 2026-09-01**
(librarian-critic score 85/100; no changes to this file's contribution statement or
differentiation logic were requested — see `annotated_bibliography.md` and
`frontier_map.md` for the substantive corrections made this round: proximity scores for
Luo et al. 2025 and Saba et al. 2022 downgraded to provisional pending verification, and a
new Diffuse Optical Tomography search documented and scoped out on physics grounds.)

Note: per the librarian's mandate, this file suggests a contribution statement and
differentiation points for the writer/strategist to use or revise if/when Fase 2
(NB05-NB07) is implemented — it does not constitute a final claim, and Fase 2 is currently
**not implemented**, so everything below is prospective, not a description of completed
work.

## Suggested contribution statement (draft, for writer to adapt once Fase 2 exists)

> We extend the PINN-SIREN framework validated in the homogeneous-medium regime (relative
> L2 error 0.006%-0.171% against closed-form Helmholtz solutions) to an inhomogeneous
> medium with a spatially-varying refractive index $n(x,y)$, entering the residual as
> $\nabla^2 E + k^2 n(x,y)^2 E = 0$. To our knowledge, this is the first application of a
> Sitzmann-style SIREN architecture, trained end-to-end with a physics-residual loss (rather
> than as a fixed basis inside a data-driven operator, cf. Kim & Lee 2026), to the
> inhomogeneous Helmholtz equation in an explicitly optical regime. [Fill in once
> implemented: validation strategy, quantitative error, and — if pursued — statistical
> consistency of any resulting speckle with Goodman's (2007) criteria under the inhomogeneous
> medium.]

## Differentiation points, by nearest candidate

| Nearest paper | What they do | What Fase 2 would do differently |
|---|---|---|
| Zhang, Ye & Ma (2026), PE-PINN, arXiv:2603.02231 | Sine activation inside an envelope-transformation sub-block + material-aware domain decomposition, for sharply heterogeneous EM dielectrics ($\kappa$ 1-80); not full SIREN | Full SIREN throughout (Sitzmann-style init + $\omega_0 \approx k/(2\pi)$ calibration, already validated in NB01/NB02) rather than sine inside one sub-block; explicit optical framing (visible-light diode laser, adimensionalized domain) rather than generic-EM/microwave dielectric-constant framing; smooth GRIN-style $n(x,y)$ rather than sharp material-region contrast, avoiding the need for their domain-decomposition workaround |
| Luo, Zhang, Wang, Jiang, Song & Wang (2025), PINN-BPM, J. Lightwave Technol. — **proximity provisional (2/5), primary source unverified after two attempts; see annotated_bibliography.md §1.2** | PINN + BPM ($z$-marching) for index-guided light propagation in optical fiber (details not independently verified — see annotated_bibliography.md) | Full-domain BVP solve (as in NB01-NB03) rather than $z$-marching, consistent with `propuesta_lente.md`'s stated constraint that the current formulation is not a marching scheme; SIREN vs. their (unconfirmed) architecture. **Caveat:** this differentiation is provisional until the primary source is read — the comparison itself could shift once verified |
| Es'kin & Ivanov (2025), arXiv:2507.04153 | tanh MLP + Maxwell (not scalar Helmholtz) for EUV lithography-mask diffraction with piecewise permittivity layers | SIREN vs. tanh (tanh activation independently confirmed via primary-source PDF read, 2026-09-01); scalar Helmholtz vs. full Maxwell system; smooth GRIN profile (if that is the Fase 2 target) vs. their piecewise-discontinuous layered structure, which is the harder regime their own results (L2 degrading from ~1e-4 to ~1e-2) illustrate |
| Saba, Gigli, Ayoub & Psaltis (2022), Advanced Photonics — **proximity provisional (3/5), architecture/quantitative figures unverified; core framing confirmed via primary-source abstract read 2026-09-01, see annotated_bibliography.md §1.4** | PINN forward model for Helmholtz-based diffraction tomography of biological (spatially-varying-permittivity) samples; architecture/error not independently verified here | Different physical target (deterministic GRIN/optical-element design vs. biological-tissue reconstruction); SIREN vs. their (unconfirmed) architecture; explicit $\omega_0$-vs-$k$ calibration |
| Kim & Lee (2026), HNO, Applied Sciences 16(12):5997 | SIREN as a fixed basis-function generator inside a data-driven DeepONet-family operator (no physics-residual loss), for high-contrast (15:1) inhomogeneous Helmholtz scattering | Genuine physics-residual PINN training (autodiff-computed Helmholtz residual in the loss, per `src/losses.py`'s existing pattern) rather than supervised operator learning on labeled simulation pairs — a fundamentally different training paradigm despite the shared use of SIREN as an architectural component |
| Chen, Liu, Lin, Chen & Shi (2024), NSNO | Data-driven Neumann-series neural operator for inhomogeneous-coefficient Helmholtz, no optical framing | PINN (physics-residual, no labeled training pairs needed) vs. their supervised operator-learning paradigm; explicit optical/GRIN framing |
| Murari & Sundar (2024), arXiv:2412.14699 | PINN for radiative transfer (not wave/Helmholtz) in a graded-index medium | Wave/Helmholtz physics vs. their radiative-transfer physics — different governing equation entirely, despite the shared "graded-index" terminology |
| Song, Alkhalifah & Bin Waheed (2022) — already known/cited | PINN + variable-velocity Helmholtz, geophysics (seismic) domain, mature and rigorous | Optical framing (diode-laser wavelength, adimensionalized [0,1]^2 domain) instead of seismic; SIREN with the thesis's own $\omega_0 \approx k/(2\pi)$ calibration rule instead of their architecture choice — this remains the single strongest methodological precedent to build on, not to differentiate away from, since it is the most rigorous existing "PINN + inhomogeneous Helmholtz" validation protocol found across both this search and the excluded geophysics literature |

**On diffuse optical tomography:** not included in this table because it solves a
structurally different governing equation (the diffusion approximation of the RTE, not the
full-wave Helmholtz equation) — see `frontier_map.md`, "Diffuse Optical Tomography (DOT) —
searched, explicitly out of scope," for the full search writeup and physics-based scoping
rationale.

## Framing recommendation for Fase 2's introduction/related-work (if and when written)

Two honest framing options, to flag for the strategist/writer rather than decide:

1. **"Optical GRIN is an under-explored transplant of a mature geophysics technique."**
   Lead with Song/Alkhalifah/Moseley (already known) as the rigorous methodological
   precedent (variable $v(x,y) \leftrightarrow n(x,y)$ is a direct mathematical analogy,
   already noted in `propuesta_lente.md`), and position Fase 2 as porting that validated
   approach to an optical, SIREN-based, $\omega_0$-calibrated pipeline — the same framing
   this thesis already uses successfully for the homogeneous case relative to Schoder &
   Kraxberger (2024).
2. **"The optical PINN literature already handles inhomogeneity, but not smoothly or with
   SIREN."** Lead with the four optical-domain papers found here (Es'kin & Ivanov; Luo et
   al.; Saba et al.; PE-PINN) to show the niche is active but fragmented, each solving a
   harder (discontinuous/piecewise) version of the inhomogeneity problem with non-SIREN
   architectures and worse relative accuracy than this thesis's own homogeneous-case
   benchmarks — motivating a controlled, smooth-GRIN, SIREN-first extension as a cleaner
   next step. **Note:** two of these four (Luo et al.; Saba et al.) carry provisional
   proximity scores pending full-text verification — this framing option should lean more
   heavily on Es'kin & Ivanov and PE-PINN, which are independently confirmed, until Luo et
   al./Saba et al. are verified in full.

Recommendation for the strategist (not a librarian decision): framing (1) is the more
defensible contribution claim given how much stronger the geophysics precedent is on
validation rigor; framing (2) is a better hook for the introduction's motivation paragraph
but should not be oversold as "no one has solved inhomogeneous optical PINNs" — four
distinct groups already have, just not with this thesis's exact combination of choices
(and two of those four are still pending full verification, see above).

## Design implication for Fase 2 (flagged from the literature, not a strategist decision)

Every optical-domain paper found that tackles a *discontinuous* inhomogeneity (Es'kin &
Ivanov's mask layers; Huang et al.'s dielectric structures, cross-referenced from
pinn-speckle; PE-PINN's material regions) needed extra machinery — smoothing functions,
domain decomposition, or accepted an order-of-magnitude accuracy penalty — to train
successfully, corroborating `propuesta_lente.md`'s own internal risk flag about "Opción B"
with a hard aperture. If Fase 2 is scoped, starting with a **smooth, non-hard-edged GRIN
profile** (e.g., the parabolic-index lens already sketched in `propuesta_lente.md`, without
a hard numerical aperture) is the literature-supported lower-risk first milestone, before
attempting any piecewise/hard-edged inhomogeneity. This is a design-space observation for
the strategist to weigh, not a determination the librarian is making on its own authority.

## Journal/venue implication

No change to the existing venue analysis in `quality_reports/literature/pinn-speckle/
positioning.md` is implied by this search alone — Fase 2 does not exist yet, so this is
not a submission-relevant question until it does. If/when it is implemented, the same
target-journal logic (Journal of Computational Physics vs. Optics Express/JOSA A) applies,
with the added note that Es'kin & Ivanov (2025), Luo et al. (2025), and PE-PINN (2026) are
all recent enough (2025-2026) that a JCP or Optics Express reviewer at that future
submission time may expect direct comparison to whichever of them has since reached
peer-reviewed, citable form.
