# Annotated Bibliography — PINN-SIREN for Optical Speckle Simulation

Project: `pinn-speckle` | Compiled: 2026-08-27 | Revised: 2026-08-27 (round 1 fixes)

Scope note: this search deliberately excludes the seven references the user already holds
(Raissi et al. 2019; Sitzmann et al. 2020; Schoder & Kraxberger 2024; Chen et al. 2020;
Lu et al. 2021; Cuomo et al. 2022; Karniadakis et al. 2021). Those are treated as known
context, not new findings, and are referenced by name only where they help position a new
paper.

**Correction (round 1):** an earlier version of this file incorrectly listed
Panagiotakopoulos et al. (2026) among the "already held" references above. Direct grep of
`paper/fuente_conNB03/references.bib` and `tesis/fuente_conNB03/references.bib` on
2026-08-27 returned zero matches for "Panagiotakopoulos" — it was never in either file. It
is a genuine new find and is now added below as Category 1.1 (proximity 5).

---

## Category 1: Directly Related (same PDE + domain, comparable metric)

### 1.1 Panagiotakopoulos, Velissaris & Rapsomanikis (2026) — "Physics-Informed Neural Network Solution of the 2D Helmholtz Equation with a Gaussian Source"
**Venue:** STARS Faculty Scholarship and Creative Works, University of Central Florida (repository deposit) — published 9 April 2026, no DOI, not yet peer-reviewed
**Proximity: 5 — HIGHEST SCOOPING RISK FLAG**

*Summary.* Solves the complex-valued 2D Helmholtz equation (frequency-domain scalar reduction of Maxwell's equations, TE polarization) with a **SIREN** architecture, for a Gaussian point source in free space and in the presence of a dielectric inclusion. Enforces the Sommerfeld radiation condition for open boundaries. Training pipeline is a hybrid collocation strategy with two-stage optimization: **Adam followed by L-BFGS** — the identical optimizer sequence used throughout this thesis (NB01–NB03). No labeled data used; loss is physics-residual only.

*Identification/validation strategy:* Qualitative assessment of physically consistent wave propagation, refraction, and scattering behavior across free-space and dielectric-inclusion scenarios (no L2-vs-analytical benchmark reported in the abstract/summary pass — unlike this thesis's core NB01/NB02 validation protocol).

*Data source:* Synthetic — collocation points sampled for the Gaussian-source Helmholtz problem; no measured data.

*Main result:* Demonstrates physically plausible wave fields (propagation, refraction at the dielectric interface, scattering) rather than a quantitative accuracy benchmark against a closed-form solution.

*Why it matters — highest scooping risk in this search:* This is architecturally the closest paper found to this thesis's own pipeline: SIREN + complex-valued 2D scalar Helmholtz + Adam-then-L-BFGS, published as a 2026 working deposit (not yet peer-reviewed, no DOI). It does **not** report an L2-vs-analytical accuracy metric the way NB01/NB02 do, does not calibrate ω₀ against k, uses a Gaussian point source + Sommerfeld radiation condition rather than a rough-phase boundary, and does not attempt speckle generation or Goodman-statistics validation — so it is not a scoop of the thesis's actual contribution (ω₀≈k/2π calibration + speckle statistics), but it is the single paper a referee is most likely to ask "how is this different from Panagiotakopoulos et al.?" about, given identical architecture/optimizer choices. Flag for strategist/writer: cite explicitly, contrast on (a) quantitative L2 validation vs. qualitative demonstration, (b) ω₀ calibration rule (absent here), (c) rough-boundary speckle generation + Goodman statistical validation vs. Gaussian-source/dielectric-inclusion scattering. Re-check the STARS repository and arXiv for a peer-reviewed version before submission.

---

### 1.2 Geetanjli & Hiremath (2026) — "Computation of waveguide eigenmodes by physics-informed neural networks"
**Venue:** Machine Learning: Engineering, Vol. 2, No. 1 (IOP Publishing) — published 20 March 2026
**Proximity: 5**

*Summary.* Solves the Helmholtz eigenvalue problem for optical/photonic waveguide mode profiles with a PINN, learning simultaneously the mode field distribution and the propagation constant from the Helmholtz equation + Dirichlet BCs only (no labeled data, no analytical solution used as ground truth for training). 5 hidden layers x 30 neurons, **sigmoid** activation (found superior to alternatives tested), Kaiming-uniform init, Adam, 50k collocation points.

*Identification/validation strategy:* Relative L2 error of the predicted eigenmode against the known analytical mode profile of a rectangular dielectric waveguide, reported as a function of collocation-point count (Fig. 11 in the source).

*Data source:* Synthetic — analytical TM/TE mode solutions of canonical rectangular waveguides.

*Main result:* L2 error decreases monotonically with more collocation points; exact scalar values not extracted from the abstract/summary pass, but the paper explicitly frames L2-vs-analytical as its core validation metric — the same protocol used in NB01/NB02 of this thesis.

*Why it matters:* One of the closest published precedents to NB01/NB02's validation protocol (PINN + Helmholtz + optical domain + L2 vs analytical) found in the search. It does **not** use SIREN (uses sigmoid) and solves an eigenvalue problem (propagation constant unknown) rather than a forward boundary-value problem with a known source/BC — this is the key differentiator to state explicitly in the lit review.

---

### 1.3 Huang, Tian, Zhang & Panoiu (2026) — "Physics-Informed Neural Networks for 2D Plane Wave Scattering in Arbitrary Dielectric Structures"
**Venue:** arXiv:2607.27349 — submitted 29 July 2026 (working paper, not yet peer-reviewed)
**Proximity: 5 — SCOOPING RISK FLAG**

*Summary.* Meshless PINN framework embedding frequency-domain Maxwell's equations (2D Helmholtz reduction) and radiation boundary conditions directly in the loss, for TM/TE plane-wave scattering off arbitrary 2D dielectric structures. Uses a hyperbolic-tangent smoothing function at material discontinuities to stabilize training across the dielectric interface.

*Identification/validation strategy:* Relative L2 error against reference solutions — reported as "mostly ≤ 0.1 (10%)" for TM polarization; TE polarization is less accurate due to permittivity discontinuities, improved with the smoothing trick.

*Data source:* Synthetic — canonical dielectric scattering geometries (not specified in detail from the abstract pass).

*Main result:* L2 error ~10% for TM (worse than this thesis's <5% target and far worse than the 0.006%–0.171% achieved in NB01/NB02), TE harder still.

*Why it matters — scooping risk:* PINN + 2D Helmholtz + explicitly optical/electromagnetic domain + L2-vs-reference metric, published within the same year window as this thesis. It is NOT a scoop in the strict sense — no SIREN, no speckle, coarser error (10% vs. this thesis's <0.2%), and the physical setup (scattering off a dielectric object) differs from this thesis's rough-boundary speckle generation. But it establishes that "PINN for optical 2D Helmholtz with L2 validation" is an active, contested niche as of mid-2026. Flag for the strategist/writer: cite explicitly and contrast (SIREN vs. tanh architecture, ω₀ calibration, order-of-magnitude lower error, speckle application) rather than risk a referee finding it first.

---

### 1.4 Rincón-Cardeño, Pérez Bernal, Montoya Noguera & Guarín-Zapata (2025) — "Benchmarking Physics-Informed Neural Networks and Boundary Elements Methods for Wave Scattering"
**Venue:** arXiv:2509.12483 — submitted 15 Sept 2025, latest revision 21 April 2026 (working paper)
**Proximity: 4**

*Summary.* Head-to-head benchmark of PINNs vs. the Boundary Element Method (BEM) for the 2D Helmholtz wave-scattering equation. Hyperparameter search (via Optuna) finds that a **sine activation function** is the best-performing configuration among those tested — direct external corroboration of the SIREN/sinusoidal-activation design choice used in this thesis, though applied to acoustic scattering, not optics.

*Identification/validation strategy:* Solution accuracy and computation time compared against BEM as the reference numerical method (not an analytical closed form).

*Data source:* Synthetic acoustic scattering configurations.

*Main result:* Sine-activation PINN is competitive with BEM in accuracy; specific error values not extracted in this pass.

*Why it matters:* Domain is acoustic (not optical), so proximity is capped at 4 rather than 5, but this is valuable independent evidence — outside the Sitzmann/Schoder pair the thesis already cites — that sinusoidal activations outperform standard alternatives specifically for Helmholtz-class PDEs. Useful for the "why SIREN and not tanh/ReLU" referee-concern flagged in the domain profile.

---

## Category 2: Same Method, Different Context (PINN + Helmholtz/EM, non-optical or non-SIREN)

### 2.1 Zhang, Li, Xia, Chen, Xiao, Guo & Liu (2025) — "FE-PIRBN: Feature-enhanced physics-informed radial basis neural networks for solving high-frequency electromagnetic scattering problems"
**Venue:** Journal of Computational Physics, Vol. 527, Art. 113798 (2025) — **top field journal**
**Proximity: 4**

*Summary.* Replaces the standard MLP+activation PINN with a physics-informed **radial basis network** (PIRBN) core enhanced with multi-resolution hash encoding, targeting sub-wavelength high-frequency EM scattering — the same high-frequency-representation problem SIREN's ω₀ calibration is designed to solve, but attacked with a different architecture (radial basis features instead of sinusoidal activations).

*Identification/validation strategy:* Relative L2 error vs. numerical (not analytical) reference simulations (single- and double-cylinder scattering).

*Main result:* **1.40%–5.82% relative L2 error**, data-free training. This is a directly comparable magnitude to this thesis's <5% target/threshold and to the achieved 0.006%–0.171%, published in the thesis's top target journal.

*Why it matters:* Strongest same-venue comparator for the "our error is X orders of magnitude below the published high-frequency EM benchmark" claim in the discussion section — cite alongside Schoder & Kraxberger (2.490%) as a second, independent high-frequency-scattering benchmark.

*Note (round 1 correction):* full author list verified via ADS/ScienceDirect metadata — was previously listed as the placeholder "Zhang, et al." in `references.bib`; corrected to the complete seven-author list.

---

### 2.2 Nair, Walsh, Pickrell & Semperlotti (2024/2025) — "Multiple scattering simulation via physics-informed neural networks"
**Venue:** Engineering with Computers, Vol. 41, pp. 31–50 (2025); first posted arXiv 2403.04094 (March 2024)
**Proximity: 2**

*Summary.* PINN with a custom network structure that encodes the physical superposition principle of linear wave interaction, applied to acoustic multiple-scattering problems (not optical, not speckle).

*Why it matters:* Background/methods precedent for embedding known physical structure (superposition) into network architecture — tangential to this thesis's design of the rough-boundary condition, but useful in a "PINNs for scattering-class problems" paragraph of the lit review. Note the December-2025 follow-up "PIBNet: a Physics-Inspired Boundary Network for Multiple Scattering Simulations" (arXiv:2512.02049) if the writer wants a more recent citation from the same line of work.

*Note (round 1 correction):* full author list verified via the arXiv abstract page (Nair, Walsh, Pickrell, Semperlotti) — was previously listed with an unverified "and others" placeholder in `references.bib`; corrected to the complete four-author list.

---

## Category 3: Same Context, Different Method (optical speckle, non-PINN or non-Helmholtz-residual ML)

### 3.1 Kazemzadeh, Collard, Piscopo, De Vittorio & Pisanello (2025) — "A Physics-Informed Neural Network as a Digital Twin of Optically Turbid Media"
**Venue:** Advanced Intelligent Systems — published 11 February 2025
**Proximity: 3**

*Summary.* "Physics-informed" in name but structurally different from a Helmholtz-residual PINN: models multimode-fiber output intensity as a modal superposition |E|²(x,y) = Σ_k |Σ_w U_{k,w}(x,y) e^{jφ_w} + Z_k(x,y)|², with a learned unknown-modulation network (ELU/tanh activations, not SIREN) fit to intensity measurements of speckle patterns exiting a turbid medium/fiber. No explicit PDE residual loss; physics enters via the fixed modal-superposition functional form, not automatic differentiation of Helmholtz.

*Identification/validation strategy:* MAE and SSIM between reconstructed and measured speckle intensity; PCA/UMAP used to characterize the speckle-pattern manifold across datasets.

*Data source:* Experimental camera measurements of multimode-fiber output.

*Why it matters:* Closest "PINN + speckle" title match in the search, but the physics and the ML method are both different from this thesis (data-driven fiber-mode model vs. from-scratch Helmholtz-residual forward simulation from a random-phase boundary; ELU/tanh vs. SIREN; experimental calibration vs. purely simulated/synthetic validation against Goodman's statistics). Cite to preempt "isn't PINN+speckle already done?" — and explicitly contrast: this thesis solves the governing PDE from a random boundary condition to *generate* speckle statistically consistent with Goodman (2007), rather than *fitting* a parametric fiber-mode model to *measured* speckle.

---

### 3.2 Guo, Xie, Yang, Ming & Chen (2025) — "Physics-Informed Generative Adversarial Networks for Laser Speckle Noise Suppression"
**Venue:** Sensors (Basel), published 20 June 2025
**Proximity: 3**

*Summary.* CycleGAN for laser-speckle **denoising** in UV (355 nm) laser microscopy, with two physics-informed loss terms: a KL-divergence term constraining the intensity distribution toward the **negative exponential** (and Rician) statistics of speckle — the exact statistical model (Goodman 2007) this thesis validates C ≈ 1 and the KS test against — and a gradient-consistency term for edge preservation.

*Identification/validation strategy:* MSE, SSIM, **speckle contrast C**, SNR against ground-truth clean images.

*Main result:* MSE 6.79, SSIM 0.95, speckle contrast C = 0.31 (post-denoising target — i.e., they *reduce* C toward a low-noise regime), SNR 7.92.

*Why it matters:* Directly relevant precedent for using the speckle-contrast statistic C and the negative-exponential intensity distribution as loss/evaluation targets in a physics-informed network — same statistical framework (Goodman) as this thesis, but applied to the inverse problem (remove speckle from an image) rather than the forward problem (generate speckle from a physical boundary condition) this thesis solves. Good citation for motivating why C and negative-exponential/KS statistics are an accepted validation currency in optics-ML work beyond this thesis's own use of them.

---

## Category 4: Theoretical Foundations

### 4.1 Tancik, Srinivasan, Mildenhall, Fridovich-Keil, Raghavan, Singhal, Ramamoorthi, Barron & Ng (2020) — "Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains"
**Venue:** Advances in Neural Information Processing Systems (NeurIPS) 33, pp. 7537–7547 (2020)
**Proximity: 3**

*Summary.* Shows theoretically (via neural tangent kernel analysis) and empirically that standard MLPs suffer from "spectral bias" toward low-frequency functions, and that mapping inputs through a Fourier/sinusoidal feature embedding before the MLP dramatically improves the network's ability to learn high-frequency signals — the same class of periodic-encoding argument that motivates SIREN's sin(ω₀·x) activation (Sitzmann et al. 2020).

*Why it matters:* This is the standard companion/alternative citation to Sitzmann et al. for justifying periodic encodings on high-frequency PDE targets. It is conspicuously absent from the project's existing bibliography given that `tesis/fuente_conNB03/references.bib` already carries Rahaman et al. (2019) on spectral bias — Tancik et al. is the natural bridge citation between "networks are biased toward low frequencies" (Rahaman) and "here is one specific fix, periodic feature encoding" (Sitzmann's SIREN uses the fix directly in the activation rather than as a pre-processing layer, which is itself a useful methodological contrast point for the introduction/related-work section).

---

## Category 5: Methods Papers

### 5.1 Krishnapriyan, Gholami, Zhe, Kirby & Mahoney (2021) — "Characterizing Possible Failure Modes in Physics-Informed Neural Networks"
**Venue:** Advances in Neural Information Processing Systems (NeurIPS) 34, pp. 26548–26560 (2021); arXiv:2109.01050
**Proximity: 4**

*Summary.* Systematically documents PDE-based case studies (including a convection equation and a reaction-diffusion equation) where naive fixed-weight PINN training fails to converge to the correct solution even though the loss appears to decrease, tracing the failure to poorly conditioned optimization landscapes created by the interaction between the data/IC loss term and the physics-residual loss term — and shows that simple weighting/curriculum fixes can resolve it.

*Why it matters:* Directly relevant to this thesis's own documented training instability: `CLAUDE.md`'s "Problemas Resueltos" table records that λ_phys = 1.0 in the 2D Helmholtz setup causes a CUDA crash / diverges (float32 overflow from the duplicated real+imaginary residual weight), resolved empirically by dropping to λ_phys = 0.1 (see `results/ablation_lambda.json`). Krishnapriyan et al. is the standard NeurIPS-venue reference for *why* fixed-weight PINN losses are fragile to this class of failure and provides the general vocabulary (loss-landscape conditioning, competing objectives) to frame the λ ablation finding as an instance of a known, studied phenomenon rather than an ad hoc fix. Complements — and is a more directly citable companion to — the gradient-pathologies mechanism described in Wang, Teng & Perdikaris (2021), which is already in the project's bib files as `Wang2021_failurePINNs` / `wang2021failure` (not re-added here; see correction note below).

### 5.2 Liu & Nocedal (1989) — "On the Limited Memory BFGS Method for Large Scale Optimization"
**Venue:** Mathematical Programming, 45(1–3), 503–528
**Proximity: 1**

*Summary.* Foundational L-BFGS reference. Already named in domain-profile.md as the anchor for the fine-tuning optimizer; included here to confirm the bibliographic record for `references.bib`.

---

## Correction Notes (round 1 fixes, 2026-08-27)

- **Removed:** the Category 5 write-up for Wang, Teng & Perdikaris (2021), "Understanding and Mitigating Gradient Flow Pathologies in Physics-Informed Neural Networks" (SIAM J. Sci. Comput. 43(5)) — this paper is **already in the project's bibliography** verbatim as `Wang2021_failurePINNs` (`paper/fuente_conNB03/references.bib`) and `wang2021failure` (`tesis/fuente_conNB03/references.bib`). It was incorrectly re-added as a "new" find in round 0 despite the stated scope note excluding already-held references. The corresponding `wang2021gradientpathologies` entry has been removed from `references.bib`.
- **Removed:** the standalone McKay, Beckman & Conover (1979) LHS write-up and its `mckay1979lhs` bib entry — also already in the project's bibliography verbatim as `Mckay1979_LHS` (`paper/fuente_conNB03/references.bib`) and `mckay1979lhs` (`tesis/fuente_conNB03/references.bib`). Same duplication error as Wang et al. above.
- **Fixed:** `zhang2025fepirbn` and `nair2025multiplescattering` had placeholder/unverified author fields (`{Zhang, et al.}` and `..., G. and others}`). Full author lists were verified via ADS/ScienceDirect metadata (Zhang, Li, Xia, Chen, Xiao, Guo, Liu) and the arXiv abstract page (Nair, Walsh, Pickrell, Semperlotti), and both `references.bib` entries and the Category 2 write-ups above have been corrected.
- **Added:** Panagiotakopoulos et al. (2026) as Category 1.1 (see above) — corrects the false claim that it was already in the project's bib files.
- **Added:** Tancik et al. (2020) as Category 4.1 (see above) — companion citation to SIREN/Rahaman on high-frequency function learning.
- **Added:** Krishnapriyan et al. (2021) as Category 5.1 (see above) — directly relevant to the documented λ=1.0 training-instability finding.

---

## Papers Checked and Excluded (documented for transparency)

- **Riganti, Zhu, Cai, Torquato & Dal Negro (2024)**, "Multiscale Physics-Informed Neural Networks for the Inverse Design of Hyperuniform Optical Materials" (arXiv:2405.07878) — optical PINN, but inverse *design* of dielectric geometries via high-frequency homogenization, not forward field/speckle simulation; no SIREN; no L2-vs-analytical metric surfaced. Proximity 2 (tangential) — omitted from the main tables but flagged here in case the writer wants a photonics-inverse-design citation for the introduction's framing of PINN applications in optics.
- **Wang et al., "Physics-Informed Neural Networks for 2D Transient Electromagnetic Fields"** (MDPI Applied Sciences, 2025) — could not retrieve full text (403 blocked); title/topic suggests proximity 3, but unverified. Flag for the writer to check directly if a broader "PINN+EM 2D" citation count is needed.
- **PIBNet** (arXiv:2512.02049, Dec 2025) — follow-up to Nair et al. 2024/2025, acoustic multiple scattering; not fetched in detail, listed only as a pointer under §2.2.
