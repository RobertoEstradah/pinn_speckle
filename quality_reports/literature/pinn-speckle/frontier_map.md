# Frontier Map — PINN-SIREN for Optical Speckle Simulation

Project: `pinn-speckle` | Compiled: 2026-08-27 | Revised: 2026-08-27 (round 1 fixes)

## What's been done

**1. PINNs for Helmholtz-class PDEs are well established** — but almost exclusively in
**acoustic** (Schoder & Kraxberger 2024, Rincón-Cardeño et al. 2025, Nair et al. 2025) or
**generic electromagnetic scattering** (Zhang et al. 2025 FE-PIRBN; Huang et al. 2026;
Panagiotakopoulos et al. 2026) contexts. Optical-specific applications exist but concentrate
on **waveguide eigenmode analysis** (Geetanjli & Hiremath 2026) and **nanophotonic inverse
design** (Chen et al. 2020 — already known; Riganti et al. 2024), not on forward field
simulation validated against an analytical benchmark the way this thesis does in NB01/NB02.
The closest architectural match found — Panagiotakopoulos et al. (2026), SIREN + complex
2D Helmholtz + Adam-then-L-BFGS — demonstrates qualitative wave behavior rather than a
quantitative L2-vs-analytical benchmark.

**2. SIREN is validated as the activation of choice for high-frequency PDE solutions**, and
independent confirmation in the optics/EM-Helmholtz space is now stronger than round 0 of
this search found. Sitzmann et al. (2020) demonstrate it on the Helmholtz equation
generically; Tancik et al. (2020) provide the companion NeurIPS-venue theoretical argument
(Fourier-feature/periodic encoding overcomes spectral bias toward low frequencies) alongside
Rahaman et al. (2019, already in the project's bib) for *why* sinusoidal representations
help; Rincón-Cardeño et al. (2025) is an *independent empirical* result where a sine
activation was selected as best-performing for a Helmholtz-class PINN (acoustics); and
Panagiotakopoulos et al. (2026) independently adopts SIREN for complex 2D Helmholtz in an
explicitly optical/EM setting — but none of these propose or test the ω₀ ≈ k/(2π)
calibration rule this thesis contributes.

**3. "PINN + speckle" as a search phrase surfaces real hits, but none solve the forward
Helmholtz problem from a random-phase boundary.** Kazemzadeh et al. (2025) fits a
data-driven modal-superposition model to *measured* fiber speckle (inverse/calibration
problem). Guo et al. (2025) uses a physics-informed GAN to *remove* speckle noise from
microscopy images, borrowing Goodman's negative-exponential statistics as a loss term but
never solving Helmholtz. Neither generates speckle from a governing PDE + rough boundary
condition the way NB03 does.

**4. Quantitative L2-vs-analytical benchmarks for PINN+Helmholtz in any domain are rare
and generally coarse** relative to this thesis's results: FE-PIRBN reports 1.40%–5.82%;
Huang et al. (2026) report ~10% for TM polarization (worse for TE); Schoder & Kraxberger
(already known) report 2.490%; Panagiotakopoulos et al. (2026) report no quantitative L2
figure at all (qualitative validation only). This thesis's reported 0.006% (1D) / 0.171%
(2D, average) is one to three orders of magnitude below every comparable published number
found, and is the only one of these papers to report a quantitative benchmark at all in the
2D optical-Helmholtz-with-SIREN cell.

**5. PINN training instability with fixed loss weights is a known, studied failure mode.**
Krishnapriyan et al. (2021, NeurIPS) and Wang, Teng & Perdikaris (2021, SIAM J. Sci. Comput.
— already in the project's bib as `Wang2021_failurePINNs`/`wang2021failure`) both document
that naive fixed-weight physics-residual losses can produce ill-conditioned optimization or
outright divergence. This directly supports this thesis's own documented finding that
λ_phys = 1.0 causes a CUDA crash in the 2D Helmholtz setup (two residual terms — real and
imaginary — double the effective physics weight), resolved by dropping to λ_phys = 0.1
(`results/ablation_lambda.json`).

## The gap this thesis fills

No paper found in this search combines all four of:
1. SIREN (sinusoidal) activation, explicitly calibrated via ω₀ ≈ k/(2π);
2. The 2D scalar Helmholtz equation in an explicitly **optical** framing (λ = 638 nm diode
   laser, adimensionalized [0,1]² domain);
3. Forward simulation of **optical speckle** generated from a random-phase rough boundary
   condition (not fitted to measured speckle, not a denoising/inverse task);
4. Statistical validation against Goodman's (2007) fully-developed-speckle criteria
   (C ≈ 1, KS test vs. negative-exponential intensity distribution) as the acceptance
   standard, in the absence of a closed-form analytical solution for the speckle field
   itself.

The closest work on each axis:
- Axis 1 (SIREN + calibration): Sitzmann et al. (2020) proposes SIREN generically; Tancik
  et al. (2020) supplies the general spectral-bias/Fourier-feature argument; Rincón-Cardeño
  et al. (2025) empirically confirms sine > alternatives for Helmholtz scattering; and
  Panagiotakopoulos et al. (2026) independently adopts SIREN for complex 2D Helmholtz — but
  none proposes or tests an ω₀-vs-k calibration rule.
- Axis 2 (optical Helmholtz + L2 validation): Geetanjli & Hiremath (2026) and Huang et al.
  (2026) are optical/EM and validate against reference solutions, but neither uses SIREN nor
  reaches comparable accuracy; Panagiotakopoulos et al. (2026) uses SIREN in an optical/EM
  Helmholtz setting but reports no quantitative L2 benchmark at all.
- Axis 3+4 (PINN forward-generates statistically-validated speckle): no paper found does
  this. Kazemzadeh (2025) and Guo et al. (2025) are the nearest "PINN + speckle" hits and
  both attack a different problem (fit/denoise measured speckle, not generate it from a
  PDE + boundary condition). Panagiotakopoulos et al. (2026) generates general Helmholtz
  wave fields from a Gaussian source, not speckle from a rough-phase boundary, and performs
  no Goodman-statistics validation.

## Where this paper sits

This thesis sits at the intersection of three literatures that have not previously been
combined: (a) SIREN-based PINNs for second-order PDEs [Sitzmann 2020; Tancik 2020], (b)
PINNs applied to the Helmholtz equation validated by L2-vs-analytical error [Schoder &
Kraxberger 2024; Geetanjli & Hiremath 2026; Zhang et al. 2025; Huang et al. 2026;
Panagiotakopoulos et al. 2026], and (c) statistical optics' speckle theory [Goodman 2007].
No prior work spans all three with a forward-simulation, from-scratch (no transfer learning
from the 2D plane-wave case), boundary-driven generation of optical speckle.

## Scooping risk assessment

- **HIGHEST watch, not a scoop:** Panagiotakopoulos, Velissaris & Rapsomanikis (2026,
  UCF STARS repository deposit, 9 April 2026) — architecturally the closest paper found:
  SIREN + complex-valued 2D Helmholtz + Adam-then-L-BFGS, the same core pipeline as this
  thesis's NB01–NB03. Differs on validation rigor (qualitative wave-behavior demonstration,
  no L2-vs-analytical benchmark reported), boundary condition (Gaussian source + Sommerfeld
  radiation vs. this thesis's rough random-phase boundary), no ω₀-vs-k calibration rule, and
  no speckle generation or Goodman-statistics validation. Not peer-reviewed and carries no
  DOI as of this search — re-check for a peer-reviewed version before submission, since a
  referee is very likely to ask "how is this different from Panagiotakopoulos et al.?" given
  the near-identical architecture/optimizer choices.
- **HIGH watch, not a scoop:** Huang et al. (2026, arXiv:2607.27349) — same PDE class,
  same explicit optical/EM framing, same L2-vs-reference validation logic, published within
  the search window. Differs on architecture (tanh-smoothed MLP, not SIREN), application
  (scattering off dielectric objects, not speckle generation from a rough phase boundary),
  and accuracy (~10% vs. this thesis's <0.2%). Cite and contrast explicitly; re-check arXiv
  for this author group before submission in case of a v2 that adds speckle or SIREN.
- **MODERATE watch:** Kazemzadeh et al. (2025) is the only paper with "PINN" and "speckle"
  both in title/abstract. Not a scoop (different physics, different ML formulation,
  experimental not from-scratch-PDE), but a referee will likely ask "how is this different
  from Kazemzadeh?" — have the answer ready (see positioning.md).
- **LOW watch:** Rincón-Cardeño et al. (2025/2026) and the FE-PIRBN/Nair et al. lines are
  acoustic/generic-EM, unlikely to be conflated with this thesis by a referee, but useful
  as supporting evidence for the SIREN/sine-activation design choice.

## Open question for the strategist

Given that Panagiotakopoulos et al. (2026) and Huang et al. (2026) are both working
papers/repository deposits (not yet peer-reviewed) published within the same calendar
window as this thesis's defense, the strategist/writer should decide whether to (a) cite
both as contemporaneous, independent working papers (standard practice) or (b) treat one or
both as the primary point of differentiation in the introduction's contribution paragraph.
Recommendation: (a), with a short explicit contrast sentence for each — this is not a
strategy decision the librarian makes.
