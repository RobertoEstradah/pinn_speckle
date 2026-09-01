# Frontier Map — PINNs for the Helmholtz Equation in Inhomogeneous Media

Project: `pinn-inhomogeneous` | Compiled: 2026-09-01 | **Round 2 corrections: 2026-09-01**
(librarian-critic score 85/100; this round adds the Diffuse Optical Tomography search
below (finding #3) and reflects the Category-1 proximity-score corrections made in
`annotated_bibliography.md` (finding #1))

This map is scoped to the thesis's planned Fase 2 (NB05-NB07, not yet implemented):
extending the validated NB01-NB03 pipeline from $\nabla^2 E + k^2 E = 0$ (homogeneous, $n$
constant) to $\nabla^2 E + k^2 n(x,y)^2 E = 0$ (inhomogeneous $n(x,y)$).

## What's been done

**1. PINN + inhomogeneous-Helmholtz is well established in geophysics** (variable
seismic velocity $v(x,y)$) — this is exactly the corner the user already cites (Song,
Alkhalifah & Bin Waheed 2022; Moseley et al. 2020; Alkhalifah et al. 2021) and it is
excluded from "new findings" here per task scope. That corner is mature and the
$n(x,y)^2 \leftrightarrow v(x,y)^{-2}$ mathematical analogy the domain-profile.md and
`propuesta_lente.md` both already note means these three papers remain the strongest
methodological precedent available for Fase 2 — this search did not find an optical-domain
paper that matches them on rigor or maturity.

**2. The optical/photonic side of "PINN + inhomogeneous Helmholtz" is real but comparatively
young, fragmented across sub-communities, and thinner than the geophysics side.** Four
distinct optical-domain PINN-plus-inhomogeneous-medium efforts were found, each addressing
a different flavor of inhomogeneity: EUV lithography-mask layers (Es'kin & Ivanov 2025,
piecewise permittivity, proximity 4, abstract- and partial-PDF-confirmed), optical-fiber
propagation (Luo et al. 2025 PINN-BPM, index-guided, **proximity downgraded to 2
(provisional)** — the primary source remains inaccessible after two independent
verification attempts, see `annotated_bibliography.md`), biological-sample diffraction
tomography (Saba et al. 2022, spatially-varying permittivity, **proximity downgraded to 3
(provisional)** — abstract-level primary-source confirmation obtained 2026-09-01, but
architecture/quantitative figures remain unconfirmed), and general heterogeneous-dielectric
EM scattering (PE-PINN, Zhang, Ye & Ma 2026, $\kappa$ 1-80 contrast, proximity 5,
abstract-confirmed). None of these four uses the thesis's own architecture (SIREN with
$\omega_0 \approx k/(2\pi)$ calibration) unmodified — the closest is PE-PINN, which uses a
sine activation only inside one architectural sub-block, not throughout the network as
SIREN does, and even that specific detail is not yet independently re-confirmed against raw
PDF text (see verification note in `annotated_bibliography.md` §1.1).

**Note on proximity scoring (Ronda 2 correction):** the original pass scored Luo et al.
(2025) and Saba et al. (2022) at proximity 5 and 4 — the two highest scores in the
inhomogeneous-medium optical category — while their technical content (architecture, exact
error figures) was simultaneously flagged as unverified (paywalled / failed fetch). That
combination inflated their apparent competitive weight relative to fully-verified entries
like PE-PINN (proximity 5, abstract-confirmed) and Es'kin & Ivanov (proximity 4,
abstract- and partial-PDF-confirmed). Both scores have been lowered and marked
"provisional" in `annotated_bibliography.md` — Luo et al. to 2 (primary source still fully
inaccessible after a second attempt) and Saba et al. to 3 (a genuine primary-source
abstract read was obtained today, though architecture/quantitative detail is still open).
**Proximity scores in this document should always be read alongside the verification-method
note for each paper** — a high provisional score is not equivalent to a high confirmed
score, and the strategist/writer should not cite either Luo et al. or Saba et al.'s specific
numbers until a full-text read is done.

**3. SIREN specifically applied to an inhomogeneous-medium Helmholtz problem is genuinely
rare.** Only one paper found combines SIREN with an explicitly inhomogeneous-medium
Helmholtz-class problem: Kim & Lee (2026), and even there SIREN is a *basis-function
generator inside a data-driven neural operator*, not a PINN trained by minimizing a
Helmholtz-residual loss end-to-end the way NB01-NB03 do. No paper found trains a
Sitzmann-style full-SIREN network with a physics-residual loss against
$\nabla^2 E + k^2 n(x,y)^2 E = 0$.

**4. GRIN (gradient-index) optics specifically, as a PINN application, is nearly absent.**
The only "graded-index" + "PINN" hit found (Murari & Sundar 2024) is radiative heat
transfer (RTE), not the wave/Helmholtz equation — a different governing physics that shares
only the qualifying adjective. No paper found applies a PINN to a classical GRIN lens
($n(x,y) = n_0(1 - \alpha^2 x^2/2)$ or similar parabolic-index profile) solving a wave
equation.

**5. Handling hard-edged inhomogeneities (aperture/interface discontinuities in $n(x,y)$)
is a documented, active failure mode across this literature, not solved.** Es'kin & Ivanov
(2025) show PINN accuracy dropping ~2-3 orders of magnitude (from ~1e-4 to ~1e-2) once
piecewise permittivity discontinuities are introduced; Huang et al. (2026, already known
from the pinn-speckle search) needed an explicit tanh-smoothing trick at material
interfaces to stabilize training; PE-PINN (Zhang, Ye & Ma 2026) uses material-aware domain
decomposition (a separate sub-network per region) specifically to sidestep this. This
directly corroborates the risk flagged independently in `propuesta_lente.md` (which cites
Krishnapriyan et al. 2021, already in the thesis's Cap4, on ill-conditioned optimization
landscapes from discontinuities) about "Opción B" (a hard-aperture GRIN lens) being the
riskiest of the three lens-implementation options considered there.

**6. No paper found combines all of: PINN + SIREN + inhomogeneous Helmholtz + optical
speckle.** The pinn-speckle project's own search already established that "PINN + speckle"
is a thin niche (Kazemzadeh et al. 2025; Guo et al. 2025), and neither of those touches a
spatially-resolved $n(x,y)$ field. This search adds no exception to that finding for the
inhomogeneous case specifically.

## Diffuse Optical Tomography (DOT) — searched, explicitly out of scope (Ronda 2, added 2026-09-01)

The librarian-critic flagged that Diffuse Optical Tomography (PINNs applied to the
diffusion approximation of the radiative transfer equation, for highly-scattering
biological/turbid media) is an active, adjacent sub-field that had not been searched or
explicitly excluded. A directed search was run today: "PINN + diffusion equation + diffuse
optical tomography / turbid media" and "PINN photon diffusion equation biological tissue
near-infrared reconstruction." Findings:

1. **No new paper found that is both (a) a genuine physics-residual PINN and (b) solving
   the photon-diffusion approximation** ($-\nabla\cdot(D(\mathbf{r})\nabla\Phi) +
   \mu_a(\mathbf{r})\Phi = S(\mathbf{r})$, the governing PDE of DOT) **for a turbid or
   biological medium**, beyond what this project and the sister `pinn-speckle` search
   already found.
2. **Kazemzadeh, Collard, Piscopo, De Vittorio & Pisanello (2025)** — already
   cross-referenced in `annotated_bibliography.md` from the `pinn-speckle` search — turns
   out on closer inspection today to be titled "A Physics-Informed Neural Network as a
   Digital Twin of Optically Turbid Media" (*Advanced Intelligent Systems*,
   doi:10.1002/aisy.202400574, published online 11 Feb 2025). This confirms it is the one
   and only turbid-media PINN hit found across both searches, and that it is a
   transmission-matrix/wavefront-retrieval digital twin (estimates how light exiting a
   turbid medium relates to the light that entered it) rather than a diffusion-equation-
   residual forward solver — it does not add a new DOT precedent, it is simply the same
   paper already accounted for, now with its correct full title on record.
3. **Sánchez López, Díaz Cortés, Domínguez Zacarías & Fuentes Cruz (2026)**, "Modeling the
   Diffusion Equation with Physics-Informed Neural Networks (PINNs) and Artificial Neural
   Networks (ANNs)" (Springer book chapter, doi:10.1007/978-3-032-08894-9_11, published 2
   January 2026) — found via this search. Solves a generic 1D Cartesian and radial
   diffusion equation with a Laplace-domain solution numerically inverted via the Stehfest
   method. The Stehfest-inversion detail is a strong domain signature of
   reservoir-engineering/well-testing analysis (a standard technique for radial-flow
   pressure-transient analysis in petroleum engineering), not an optical or
   biological-tissue application; no DOT or optical framing was found in the available
   abstract-level material (the chapter itself is paywalled). **Excluded as off-domain** —
   same PDE family, unrelated physical application; not added to `references.bib` or the
   main tables. See `annotated_bibliography.md`, "Papers checked and excluded," for the
   full note.
4. **Why DOT is out of scope regardless of what is found.** DOT's forward model — the
   diffusion approximation of the radiative transfer equation, an elliptic PDE for the
   diffuse photon fluence rate $\Phi(x,y)$ in a highly-scattering medium — is a
   structurally different governing equation from the full-wave scalar Helmholtz equation
   $\nabla^2 E + k^2 n(x,y)^2 E = 0$ this thesis solves (NB01-NB03, and the planned Fase 2
   target). The diffusion approximation is valid precisely in the regime where coherent
   phase information is lost to multiple scattering (the opposite of the coherent,
   phase-resolved speckle field this thesis's NB03 already produces and Fase 2 would
   extend). **This is a scope boundary declared on physics grounds, not an artifact of an
   incomplete search** — even a well-executed, rigorously-verified DOT-PINN paper would not
   be a direct precedent or competitor for this thesis's governing equation, and none was
   found to exist as a close match in any case.

## The gap Fase 2 would fill

No paper found in this search combines:
1. **SIREN** (sinusoidal activation throughout, Sitzmann-style initialization, with the
   $\omega_0 \approx k/(2\pi)$ calibration rule this thesis already contributes for the
   homogeneous case);
2. The 2D scalar Helmholtz equation with an **explicit, smooth, deterministic $n(x,y)$
   field** (e.g., a parabolic GRIN profile) rather than a piecewise-discontinuous
   permittivity structure or a statistically-random turbid medium;
3. An explicitly **optical** framing (visible-light diode laser wavelength, adimensionalized
   domain) consistent with the rest of the thesis, rather than microwave/EUV/geophysics
   framing;
4. Validation against either a closed-form/semi-analytical GRIN solution or, if speckle is
   layered on top per the propuesta_lente.md roadmap, Goodman (2007) statistical
   consistency.

**Closest work on each axis:**
- Axis 1 (SIREN, calibrated): none of the inhomogeneous-medium papers found use full SIREN
  with the $\omega_0$-vs-$k$ calibration; Kim & Lee (2026) uses SIREN only as a basis
  generator inside a non-PINN operator, and PE-PINN (Zhang, Ye & Ma 2026) uses sine
  activation only inside one sub-block (abstract-confirmed architecture framing; the sine-
  activation detail itself is not yet independently re-confirmed against raw PDF text —
  see `annotated_bibliography.md` §1.1).
- Axis 2 (smooth deterministic $n(x,y)$, not discontinuous/random): most optical-domain
  hits found (Es'kin & Ivanov; Huang et al.; PE-PINN) target piecewise/discontinuous
  permittivity (masks, dielectric inclusions, material boundaries) — exactly the harder,
  Krishnapriyan-style failure regime — rather than a smooth GRIN gradient. A smooth GRIN
  profile without hard apertures may in fact be an *easier* regime than what most of this
  literature already tackles, per the `propuesta_lente.md` risk analysis (Opción B without
  a hard aperture is "más manejable").
- Axis 3 (explicitly optical, visible-light framing): Luo et al. (2025, optical fiber) and
  Saba et al. (2022, biological-sample tomography) are the closest on paper, but their
  proximity scores are now provisional (2 and 3 respectively, see above) precisely because
  neither is independently verified in full technical detail — Luo et al.'s primary source
  remains fully inaccessible, and neither uses SIREN in any case.
- Axis 4 (Goodman-statistics-validated speckle on top of an inhomogeneous medium): no paper
  found attempts this in any domain.

## Where Fase 2 would sit

If implemented as scoped in `propuesta_lente.md` (Opción B: $n(x,y)$ variation entering the
Helmholtz residual directly, e.g., for a GRIN lens), Fase 2 would sit at the intersection of
four literatures with only partial overlap so far: (a) SIREN-based PINNs for second-order
PDEs [Sitzmann 2020, already known]; (b) PINNs for the Helmholtz equation with variable
medium properties, currently dominated by geophysics [Song/Alkhalifah/Moseley, already
known] with a thin, fragmented optical periphery [Es'kin & Ivanov 2025; Luo et al. 2025
(provisional); Saba et al. 2022 (provisional); PE-PINN 2026]; (c) GRIN optics as a physical
target, essentially untouched by the PINN literature outside one unrelated-physics paper
[Murari & Sundar 2024]; and (d) Goodman (2007) speckle statistics [already known], not
combined with (b) or (c) by anyone found in either this search or the prior pinn-speckle
search — and explicitly not overlapping with the structurally distinct Diffuse Optical
Tomography sub-field (see above), which solves the diffusion approximation rather than the
full-wave Helmholtz equation.

## Scooping risk assessment

- **LOW risk overall for Fase 2 as currently scoped (not yet implemented).** No paper found
  combines SIREN + a smooth deterministic optical $n(x,y)$ field + a wave equation. The
  closest candidates on paper (PE-PINN, Es'kin & Ivanov) target harder, discontinuous-
  permittivity regimes with non-SIREN architectures; the closest SIREN+inhomogeneous-
  Helmholtz hit (Kim & Lee 2026) is a data-driven operator, not a PINN; and the two
  candidates with the highest *nominal* proximity in the optical sub-field (Luo et al.;
  Saba et al.) carry that proximity provisionally, pending verification, which further
  lowers their weight as a scooping threat until confirmed.
- **WATCH, not urgent:** PE-PINN (Zhang, Ye & Ma 2026) and Luo et al. (2025, PINN-BPM) are
  both 2025-2026 working/recently-published items in adjacent optical/EM sub-fields;
  re-check both closer to Fase 2 implementation time in case a follow-up paper narrows the
  gap toward SIREN-specific or GRIN-specific treatment, and re-attempt full-text
  verification of Luo et al. specifically before that time.
- **Methodological risk, not scooping risk:** the strongest finding of this search is not
  "someone else already did this" but "the discontinuous/hard-edged-inhomogeneity failure
  mode is real and repeatedly documented across four independent papers" — this is a design
  constraint for Fase 2 (favor smooth GRIN profiles over hard-aperture lenses, consistent
  with `propuesta_lente.md`'s own recommendation), not a competitive threat.

## Open question for the strategist

`propuesta_lente.md` already identifies three implementation options (A: boundary-condition
phase mask, no residual change; B: $n(x,y)$ in the residual, i.e., the literal Fase 2 target
equation; C: post-hoc field transformation) and recommends A unless a mid-domain lens is
specifically required, in which case B is accepted only for smooth (non-hard-aperture)
index profiles. This literature search independently corroborates that recommendation from
the *external* evidence side: every optical-domain paper found that attacks a
discontinuous-permittivity version of Option B needed extra machinery (smoothing functions,
domain decomposition, or accuracy roughly an order of magnitude worse) to make it work. This
is not a strategy decision for the librarian to make, but the strategist should weigh it
alongside `propuesta_lente.md`'s own internal risk analysis when scoping Fase 2's first
milestone (e.g., start with a smooth parabolic-index GRIN profile before attempting any
hard-aperture case).
