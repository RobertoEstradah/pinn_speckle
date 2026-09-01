# Annotated Bibliography — PINNs for the Helmholtz Equation in Inhomogeneous Media

Project: `pinn-inhomogeneous` | Compiled: 2026-09-01 | **Round 2 corrections: 2026-09-01**
(librarian-critic score 85/100 — see `quality_reports/reviews/` for the critic report;
this round addresses findings #1 and #2 only, marked inline as "Ronda 2")

**Scope.** This search targets literature for the thesis's planned Fase 2 (NB05-NB07, not yet
implemented): extending PINN-SIREN from the homogeneous-medium Helmholtz equation
$\nabla^2 E + k^2 E = 0$ (current NB01-NB03) to the inhomogeneous-medium form
$\nabla^2 E + k^2 n(x,y)^2 E = 0$. Four sub-questions were searched: (1) PINNs solving
Helmholtz/wave with variable $n(x,y)$ or $v(x,y)$; (2) PINNs for GRIN (gradient-index)
optics; (3) SIREN specifically in inhomogeneous media; (4) PINN + inhomogeneous medium +
speckle/optical diffusion.

**Excluded by task instruction (already known/cited by the user — not reported as new):**
Song, Alkhalifah & Bin Waheed (2022, *Geophysical Journal International* 228(3),
1750-1762); Moseley, Markham & Nissen-Meyer (2020, arXiv); Alkhalifah, Song, Waheed & Hao
(2021, *Artificial Intelligence in Geosciences*). All three are geophysical-domain PINN +
variable-velocity Helmholtz papers already cited in `tesis/Tesis_Actual/references.bib`
(verified by direct grep on 2026-09-01: `moseley2020wave` at line 219, the Alkhalifah/Song/
Waheed entry at line 238). They are used below only as reference points for how covered
the geophysics side of this niche already is — the point of this search is the optical/
photonic side, which is comparatively sparse.

**A note on a citation already in the project's own documents.** `propuesta_lente.md`
(2026-08-31, analysis of a future thin-lens extension) and the original thesis protocol
document (`master_supporting_docs/supporting_protocolo_md/Protocolo_tesis_maestria_
Roberto_Hernandez_Estrada.md`, line 623) both cite: *"Fang, Z., & Zhan, J. (2020). A
physics-informed neural network framework for wave scattering in inhomogeneous media. IEEE
Antennas and Wireless Propagation Letters, 19(9), 1640-1644."* I searched for this specific
title/venue/page combination across IEEE Xplore, Semantic Scholar, Google Scholar, and
ResearchGate through multiple query variants and **could not locate it**. Fang & Zhan did
publish two verifiable 2020 PINN papers — "Deep Physical Informed Neural Networks for
Metamaterial Design" (IEEE Access 8, 24506-24513) and "A Physics-Informed Neural Network
Framework for PDEs on 3D Surfaces: Time Independent Problems" (IEEE Access 8, 26328-26335)
— but neither matches the claimed title, journal, or page range. **This citation should be
treated as unverified and not relied upon until confirmed via a direct IEEE Xplore DOI
lookup** (I do not have a subscription-gated IEEE Xplore search tool available in this
session). Given this project's documented history of citation-verification issues, flagging
this explicitly rather than silently repeating it. It is not included in `references.bib`.

---

## Category 1: Directly Related (PINN + Helmholtz-class PDE + explicit inhomogeneous/
## spatially-varying refractive index or permittivity, optical/photonic domain)

### 1.1 Zhang, Ye & Ma (2026) — "Physics-Informed Neural Networks with Architectural Physics Embedding for Large-Scale Wave Field Reconstruction" (PE-PINN)
**Venue:** arXiv:2603.02231 (2026, working paper)
**Proximity: 5 — closest architectural match found**

*Summary.* Proposes PE-PINN, which embeds physics into the network architecture rather
than only the loss: an "envelope transformation layer" decomposes the field into a
physically-parameterized oscillatory kernel (plane-wave or spherical-wave phase term,
$e^{-jk\mathbf{d}^T\mathbf{x}}$ or $e^{-jk\|\mathbf{x}-\mathbf{x}_m\|}$) multiplied by a
learned smooth envelope, with **sine (SIREN-style) activation functions** used for the
derivative computation, plus material-aware domain decomposition (a separate sub-network
per material region) and incident/scattered-field separation.

*Identification/validation strategy:* MSE against COMSOL FEM reference solutions across
free-space, diffraction, and refraction scenarios.

*Data source:* Synthetic — 2D electromagnetic scenarios with heterogeneous dielectric
regions, relative permittivity $\kappa$ ranging from 1 to 80 across materials.

*Main result:* MSE vs. COMSOL of 3.38e-3 (free space), 7.94e-3 (diffraction), 7.12e-3
(refraction); reports >10x faster convergence than a vanilla PINN (~18 min vs. >26 hours)
and orders-of-magnitude lower memory than FEM on the same problem.

*Verification method (Ronda 2, added 2026-09-01):* Re-verified today by fetching the arXiv
abstract page directly (`arxiv.org/abs/2603.02231`) via WebFetch. The abstract independently
confirms: the envelope-transformation-layer architecture, the framing as addressing "slow
convergence, optimization instability, and spectral bias," the >10x convergence speedup vs.
a standard PINN, and the orders-of-magnitude memory reduction vs. FEM. A follow-up fetch of
the PDF (`arxiv.org/pdf/2603.02231`) was attempted to independently re-confirm the
sine/SIREN-activation detail, the exact $\kappa=1$-$80$ contrast range, and the specific MSE
figures (3.38e-3 / 7.94e-3 / 7.12e-3) against raw primary-source text; that PDF text
extraction was partial (compressed content streams not fully decoded by the fetch tool) and
did not surface those specific numbers or the sine-activation sentence on this pass. **Net
status:** the qualitative architecture/result claims above are abstract-confirmed
(high confidence); the exact numeric figures and the sine/SIREN-activation detail are
carried over from the original search pass and were not independently re-confirmed
digit-for-digit against primary-source PDF text in this round — treat them with the same
caution as any secondary-source-summarized figure until a manual full-text read is done.

*Why it matters.* This is the closest single paper found to what Fase 2 would need to
build: a **sine/SIREN-style activation** applied to the **Helmholtz-type equation across a
sharply heterogeneous medium** (dielectric contrast $\kappa$ 1-80, i.e., far more extreme
than a smooth GRIN profile), including an explicit strategy (domain decomposition per
material, envelope-kernel parameterization) for handling the discontinuity-at-interface
problem that Krishnapriyan et al. (2021, already cited in the thesis's Cap4) documents as a
generic PINN failure mode. It is framed as EM/microwave (dielectric constant language, not
explicitly visible-optics or an optical-fiber refractive-index framing), and it does not
use the "vanilla" full SIREN (sinusoidal activation *throughout* the network with
Sitzmann-style initialization) — only a sine nonlinearity inside its envelope-kernel
sub-block. Flag for strategist: this is the paper most likely to be asked about if Fase 2
proposes anything resembling a per-region or domain-decomposed treatment of a hard-edged
inhomogeneity (e.g., a GRIN lens with a hard aperture, per the Opción B risk noted in
`propuesta_lente.md`).

---

### 1.2 Luo, Zhang, Wang, Jiang, Song & Wang (2025) — "PINN-BPM: An Enhanced Physics-Informed Neural Network Framework of Solving Helmholtz Equation for Light Field Propagation in Optical Fiber"
**Venue:** Journal of Lightwave Technology, 43(23), 10380-10401 — accepted 26 Sept 2025, published 30 Sept 2025
**Proximity: 2 (provisional — pending content verification; see note below. Do not treat
as equal to the proximity-4/5 papers in this category until the primary source is read.)**

*Summary.* Solves the slowly-varying-field Helmholtz equation (SVHE) for light-field
propagation in optical fiber via a PINN combined with the Beam Propagation Method (BPM) —
i.e., a $z$-marching scheme rather than a full boundary-value-problem solve over the whole
domain at once. Adds residual-based adaptive sampling, self-adaptive loss weights, and
causal weighting to the training procedure.

*Identification/validation strategy, data source, architecture, exact error figures:* **Not
independently confirmed.** Original pass: the Optica Publishing Group abstract page is
paywalled; only the abstract-level description above could be retrieved (via search-engine
summarization, not a verified primary-source read of the methods/results). No arXiv
preprint was located. **Ronda 2 re-verification attempt (2026-09-01):** repeated the search
(WebSearch for the exact title/venue/authors) and confirmed only the same
search-engine-paraphrased description already used above (title, authors, venue,
page range, and the one-paragraph BPM/SVHE framing) — the Optica abstract page itself
remains inaccessible with the tools available in this session, and no arXiv or other
open-access copy was found. **Verification status is unchanged from the original pass:
zero primary-source access achieved across two independent attempts.** Do not cite
specific numbers, architecture details, or the exact BPM-vs-full-BVP mechanics from this
paper without obtaining and reading the full text directly.

*Why proximity was lowered (Ronda 2).* This paper was originally scored Proximity 5 (the
highest score in the entire bibliography) based only on an abstract-level,
search-engine-mediated description — i.e., the single least-verified entry in the
document was carrying the single highest proximity score. That is inconsistent: proximity
should reflect confidence-weighted closeness, not just how close the paper *would be* if
every unconfirmed detail turns out to be true. Lowered to 2 (provisional) to reflect that
the specific claims driving the high original score (index-guided fiber propagation
architecturally matching the Fase 2 target equation) are exactly the claims that remain
unverified. If a full-text read later confirms the abstract-level description, this should
be revised back up toward 4-5.

*Why it matters (with the caveat above).* If the abstract-level description holds up under
full-text verification, this is the single closest **optical-fiber, index-guided,
PINN+Helmholtz** paper found — optical fiber propagation is governed by a refractive-index
profile $n(r)$ (step-index or graded-index) that is architecturally exactly the "Fase 2"
target equation. It differs from the thesis's planned approach on one structural axis worth
flagging early: it uses BPM $z$-marching (propagate an initial field forward slice by
slice) rather than the thesis's from-scratch full-domain BVP solve with only a $y=0$
boundary active (per `CLAUDE.md`'s NB03 description) — the same z-marching vs. full-BVP
distinction that `propuesta_lente.md` raises as relevant to how a lens/GRIN element could be
incorporated (its "Opción B" analysis explicitly flags BPM as the natural fit for
mid-domain optical elements, citing this same paper). **All of this remains conditional on
verification that has not yet been achieved.**

---

### 1.3 Es'kin & Ivanov (2025) — "Physics-informed neural networks and neural operators for a study of EUV electromagnetic wave diffraction from a lithography mask"
**Venue:** arXiv:2507.04153, submitted 5 July 2025 (working paper)
**Proximity: 4**

*Summary.* PINN and a novel hybrid Waveguide Neural Operator (WGNO — a waveguide-method
solver with its most expensive step replaced by a neural network) for EUV lithography mask
diffraction. The medium is explicitly inhomogeneous: each layer of the mask has its own
dielectric permittivity $\varepsilon_j(x,y)$, piecewise-constant across layers. Solves the
frequency-domain Maxwell system for $H_x, H_y$ in 2D and 3D. **Architecture: tanh MLP (3
hidden layers x 128 neurons)** — not SIREN.

*Identification/validation strategy:* Relative L2 error against reference solutions.

*Main result:* 2D canonical test problems: L2 error 1.7e-4 to 5.5e-2 (PINN). 2D
lithography-mask geometry: PINN L2 error 4.9e-2 to 8.9e-2; the WGNO hybrid achieves
9.5e-7 to 3.9e-6 — several orders of magnitude better, illustrating that the pure-PINN
baseline degrades substantially once real permittivity discontinuities are introduced.

*Verification method (Ronda 2, added 2026-09-01):* Re-verified today via WebFetch on the
arXiv abstract page (`arxiv.org/abs/2507.04153`), confirming the title, the WGNO
(Waveguide Neural Operator) framing, and the EUV lithography-mask diffraction application
directly from the primary source's own abstract text. A follow-up fetch of the PDF
(`arxiv.org/pdf/2507.04153`) additionally confirmed, from extracted primary-source text,
that the PINN baseline uses **tanh activation** — consistent with (not previously stated as
independently confirmed in) this entry. The PDF extraction did not surface the exact layer
configuration (3x128) or the specific relative-L2-error figures listed above
(1.7e-4-5.5e-2 canonical; 4.9e-2-8.9e-2 mask; WGNO 9.5e-7-3.9e-6) — those remain carried
over from the original search pass, not yet re-confirmed digit-for-digit against raw PDF
text, though nothing found today contradicts them.

*Why it matters.* Directly verifies that even a well-resourced, published (arXiv, 2025)
PINN baseline loses two-to-three orders of magnitude of accuracy (from ~1e-4 to ~1e-2)
once a piecewise-inhomogeneous permittivity structure is introduced, relative to this
thesis's homogeneous-medium NB01/NB02 benchmarks (0.006%-0.171%). This is useful evidence
for the strategist when scoping Fase 2's expected error budget — the <5% target used
throughout `CLAUDE.md`/domain-profile.md is *not* automatically achievable by simply adding
$n(x,y)$ to the residual; Es'kin & Ivanov's own tanh-MLP baseline sits close to that 5%
ceiling on the harder (piecewise, discontinuous) case. Also EUV/lithography, not
visible-light optics — a different wavelength regime the writer should note explicitly if
citing it as an "optical" precedent.

---

### 1.4 Saba, Gigli, Ayoub & Psaltis (2022) — "Physics-informed neural networks for diffraction tomography"
**Venue:** Advanced Photonics, 4(6), 066001 — published 22 November 2022, doi:10.1117/1.AP.4.6.066001
**Proximity: 3 (provisional — core framing confirmed via primary-source abstract text on
2026-09-01; architecture and quantitative results still unconfirmed. See note below.)**

*Summary.* Uses a PINN as the *forward model* for tomographic reconstruction of biological
samples: the Helmholtz equation is imposed as a physical loss so the network predicts the
scattered field given a sample's (spatially-varying) permittivity distribution, without
needing labeled scattered-field training data for that specific sample; a pretrained
network can then be fine-tuned per-sample faster than solving the forward scattering
problem numerically from scratch each time.

*Identification/validation strategy, exact architecture/activation, and quantitative error
figures:* **Not independently confirmed.** Original pass: the full PDF fetch returned
corrupted/binary content and the SPIE abstract page did not return readable text via the
available fetch tool. Venue, authors, and publication date were confirmed via multiple
independent secondary sources (SPIE DOI, arXiv:2207.14230 cross-listing, ADS abstract,
ResearchGate). **Ronda 2 re-verification (2026-09-01):** successfully fetched the arXiv
cross-listing abstract page directly (`arxiv.org/abs/2207.14230`) via WebFetch — this is a
primary-source read (the authors' own arXiv-hosted abstract), not a secondary paraphrase,
and it independently confirms the core summary above word-for-word in substance: "physics-
informed neural networks as a forward model for tomographic reconstructions of biological
samples," "training this network with the Helmholtz equation as a physical loss," pretrained
networks fine-tuned per-sample faster than conventional numerical methods, and validation
against "both numerical simulations and experimental data." **Architecture (activation
function, layer sizes) and exact quantitative error/speed figures remain unconfirmed** — the
abstract text itself does not state them, and the full PDF was not successfully retrieved in
either pass.

*Why proximity was lowered and re-graded (Ronda 2).* Originally scored Proximity 4 despite
the architecture/quantitative claims being flagged as unverified — an inconsistency the
critic flagged. Set to 3 (provisional) rather than a flat downgrade to match Luo et al.
(1.2, provisional-2) because today's re-verification did achieve a genuine primary-source
abstract read for this paper (unlike Luo et al., where the primary source remains fully
inaccessible) — the qualitative framing (Helmholtz-as-physical-loss forward model for
biological tomography) is now confirmed at the abstract level, only the architecture and
numbers remain open. Revise upward if a full-text PDF read confirms those remaining details.

*Why it matters (with the caveat above).* This is the clearest "PINN + Helmholtz + optical
+ inhomogeneous medium" application found outside the geophysics literature already known
to the user — biological tissue is exactly a spatially-varying-permittivity medium, and
"train once per sample, reuse the forward solve" is conceptually close to the amortized-
training argument this thesis already makes for its own PINN-vs-FEM speed-up comparison
(per domain-profile.md's referee-concern list on single-query vs. amortized comparison).

---

## Category 2: Same Method, Different Context (Helmholtz + inhomogeneous medium, but
## data-driven neural operator rather than a physics-residual PINN)

### 2.1 Kim & Lee (2026) — "FFT-Free Neural Operators for Helmholtz Scattering via Adaptive Coefficient Modulation" (HNO)
**Venue:** Applied Sciences (MDPI), 16(12), 5997 — published 13 June 2026, doi:10.3390/app16125997
**Proximity: 3-4**

*Summary.* A DeepONet-family operator ("Helmholtz Neural Operator") that replaces the FFT-
based spectral trunk of a Fourier Neural Operator with a **hybrid basis: a three-layer
SIREN ($\omega_0 = 30$) plus 16 learnable Fourier frequencies (64 total basis outputs)**,
paired with a rank-32 hypernetwork branch with bounded multiplicative gating on per-mode
coefficients. Targets the "mode saturation" failure of standard FNOs on high-contrast
inhomogeneous media (tested at a 15:1 refractive-index-contrast ratio).

*Identification/validation strategy:* Out-of-distribution generalization gap vs. a matched-
parameter-count FNO baseline.

*Main result:* 2.6x lower OOD generalization gap than FNO at matched ~1.05M parameters
(19.6% vs. ~51%).

*Verification method (Ronda 2, added 2026-09-01):* Re-verified today. A direct WebFetch of
the MDPI article page (`mdpi.com/2076-3417/16/12/5997`) returned HTTP 403 (blocked — no
subscription-gated access tool available in this session). Verified instead via WebSearch,
which surfaced a search-result snippet keyed to the DOI listing
(`doi.org/10.3390/app16125997`) that reads as quoted abstract language and matches this
entry's architecture description verbatim in substance: "a physics-informed, FFT-free
branch-trunk operator in the DeepONet family, with a hybrid SIREN+learnable-Fourier trunk
and a dual-path rank-32 hypernetwork branch, with bounded multiplicative gating," and "2.6x
lower out-of-distribution generalization gap than FNO at matched parameter count." This is
treated as a reliable confirmation of the qualitative architecture and headline result, but
it is a search-engine-surfaced snippet, not a direct primary-source page load — the
$\omega_0=30$ value, the 19.6%-vs-~51% breakdown, and the ~1.05M-parameter figure were not
independently re-confirmed against the primary PDF/HTML in this round.

*Why it matters.* This is **the only paper found in this search that explicitly uses SIREN
inside a Helmholtz-equation-for-inhomogeneous-media architecture** — directly answering
sub-question (3) of the task. It is *not* a PINN in the thesis's sense: it is trained on
labeled input-output simulation pairs (data-driven operator learning), not by minimizing a
Helmholtz-residual loss via autodiff the way NB01-NB03 do. The SIREN component here is
used purely as a fixed/learnable *basis function generator* for the trunk network, not as
the network solving the PDE end-to-end. Useful precedent to cite for "SIREN's spectral
properties are useful for representing high-contrast inhomogeneous wavefields," but should
not be conflated with a genuine SIREN-PINN precedent.

---

### 2.2 Chen, Liu, Lin, Chen & Shi (2024) — "NSNO: Neumann Series Neural Operator for Solving Helmholtz Equations in Inhomogeneous Medium"
**Venue:** Journal of Systems Science and Complexity, 37, 413-440 (2024); first posted arXiv:2401.13494 (25 Jan 2024)
**Proximity: 2-3**

*Summary.* A Neumann-series-structured neural operator (with an embedded U-Net for
multiscale feature capture) that learns the solution operator of the Helmholtz equation for
spatially-varying coefficient/wave-speed fields and source terms — explicitly targeting the
high-wavenumber regime where standard neural operators degrade.

*Identification/validation strategy:* Relative L2 error vs. baseline neural operators (FNO
and others), reported as at least 60% lower error and 50% lower compute cost at high
wavenumber.

*Verification method (Ronda 2, added 2026-09-01):* Re-verified today via WebFetch directly
on the arXiv abstract page (`arxiv.org/abs/2401.13494`) — a primary-source read that
independently confirms the Neumann-series operator structure, the embedded U-Net for
multiscale-feature capture, the targeting of the high-wavenumber degradation regime, and
the >=60% lower relative-L2-error / 50% lower compute cost vs. an FNO baseline. No
discrepancies found between the abstract text and this entry.

*Why it matters.* Same PDE class (Helmholtz, inhomogeneous coefficient field) as the Fase 2
target, but a fully data-driven operator-learning method rather than a PINN, and not framed
in an optical context (the coefficient field is generic — could represent wave speed in
acoustics/geophysics or a permittivity/index field in optics, but the paper does not use
optical framing or terminology). Useful as a "same PDE, different method" methodological
contrast: shows that operator-learning approaches to inhomogeneous Helmholtz are an active
alternative to the PINN route the thesis is committed to, with different failure modes
(these papers report degradation mainly as *generalization gap across unseen coefficient
fields*, rather than *training-time convergence failure* the way PINN literature — e.g.
Krishnapriyan et al. 2021, already cited in Cap4 — typically frames it).

---

## Category 3: Same Context, Different Physics (graded-index/GRIN medium, PINN, but not the wave/Helmholtz equation)

### 3.1 Murari & Sundar (2024) — "Physics informed neural network for forward and inverse radiation heat transfer in graded-index medium"
**Venue:** arXiv:2412.14699, submitted 19 December 2024, revised 24 December 2024 (working paper, no journal publication found)
**Proximity: 2**

*Summary.* Applies a PINN to the **radiative transfer equation (RTE)** — not the wave/
Helmholtz equation — inside a graded-index (GRIN) participating medium, for both forward
(predict radiative intensity given the medium) and inverse (recover medium properties from
observed intensity) problems. Reports improved numerical stability and reduced oscillatory
error relative to finite-element/meshfree baselines as the refractive-index gradient
becomes more pronounced.

*Verification method (Ronda 2, added 2026-09-01):* Re-verified today via WebFetch directly
on the arXiv abstract page (`arxiv.org/abs/2412.14699`) — a primary-source read that
independently confirms the governing equation is the radiative transfer equation (explicitly
not Helmholtz/wave), the graded-index-medium framing, the forward/inverse problem setup, and
the qualitative claim of improved numerical stability and reduced oscillatory error under
pronounced refractive-index gradients. The abstract text itself does not report numeric
benchmarks, consistent with this entry already describing the finding only qualitatively.

*Why it matters.* This is the only paper found in this search that pairs "PINN" with the
literal keyword "graded-index medium" (sub-question 2 of the task), but the underlying
physics is radiative heat transfer (an integro-differential transport equation), not
Helmholtz-equation wave propagation — the two share the term "graded-index" and the
qualitative challenge of a smoothly-varying medium property inside a PDE residual, but are
not the same governing equation and the finding should not be over-read as evidence for
how a wave-optics GRIN PINN would behave. Useful only as a keyword-adjacent pointer, not a
methodological precedent to build on directly.

---

## Cross-references to the pinn-speckle project's bibliography (relevant here too, not re-added to `references.bib` to avoid duplicate keys)

These three papers are already documented in `quality_reports/literature/pinn-speckle/`
(Category 1 of that project's annotated bibliography) but are also directly relevant to the
inhomogeneous-medium question, because each one already involves a spatially-varying
permittivity/dielectric structure — i.e., each is a *partial* precedent for Fase 2, found
under the *speckle* search and worth cross-checking here rather than re-verifying from
scratch:

- **Panagiotakopoulos, Velissaris & Rapsomanikis (2026)** — SIREN + complex 2D Helmholtz +
  Adam-then-L-BFGS, tested in free space **and in the presence of a dielectric inclusion**
  (a localized region of different permittivity — a simple form of inhomogeneous medium,
  though not a smooth GRIN-style gradient). This is the closest existing precedent for
  "SIREN + inhomogeneous Helmholtz" as a combination, even though the pinn-speckle search
  found it primarily for its architectural match to NB01-NB03's homogeneous-medium
  pipeline. Worth re-reading with the dielectric-inclusion scenario specifically in mind if
  Fase 2 proceeds.
- **Huang, Tian, Zhang & Panoiu (2026, arXiv:2607.27349)** — PINN (tanh-smoothed MLP) for
  2D plane-wave scattering off **arbitrary dielectric structures** — i.e., explicitly
  piecewise-inhomogeneous permittivity, with a smoothing trick at material discontinuities
  to stabilize training. Directly relevant methodological precedent for handling the
  "hard-edged inhomogeneity" risk flagged in `propuesta_lente.md`'s Opción B discussion.
- **Kazemzadeh, Collard, Piscopo, De Vittorio & Pisanello (2025)** — data-driven (not
  Helmholtz-residual) modal-superposition/digital-twin model of speckle exiting a
  turbid/multimode-fiber medium; turbid media are a statistically-inhomogeneous scattering
  medium in the broad sense, though the paper does not solve a PDE with a spatially-resolved
  $n(x,y)$ field. **Confirmed today (Ronda 2, 2026-09-01) via WebSearch to be titled "A
  Physics-Informed Neural Network as a Digital Twin of Optically Turbid Media"** (*Advanced
  Intelligent Systems*, doi:10.1002/aisy.202400574, published online 11 Feb 2025) — this is
  a transmission-matrix/wavefront-retrieval digital twin, not a diffusion-equation-residual
  solver (see the new Diffuse Optical Tomography discussion in `frontier_map.md`, Ronda 2).
  Relevant if Fase 2's long-term ambition includes turbid/diffusive media rather than
  smooth deterministic GRIN profiles.

## Papers checked and excluded from the main tables

- **Zhang, Shi et al., "SirenFNO: Efficient and Full Frequency Learning of Fourier Neural
  Operators"** (arXiv:2606.11518) — combines SIREN with Fourier Neural Operators, but is a
  general parameter-efficiency contribution for operator learning with no stated
  application to the Helmholtz equation or optical/refractive-index problems in the
  abstract-level material retrieved; not included given no confirmed link to this project's
  inhomogeneous-Helmholtz-optics scope.
- **Balaji, Teolis, Mis, Lara Benitez, Wang & de Hoop, "Hybrid operator learning of wave
  scattering maps in high-contrast media"** (arXiv:2602.11197) — FNO + Vision Transformer
  hybrid for high-contrast Helmholtz scattering, but explicitly seismic/subsurface (salt-
  body imaging) framing, no SIREN, data-driven operator not PINN. Proximity 2 at most;
  omitted from the main tables.
- **(Ronda 2, added 2026-09-01) Sánchez López, Díaz Cortés, Domínguez Zacarías & Fuentes
  Cruz (2026), "Modeling the Diffusion Equation with Physics-Informed Neural Networks
  (PINNs) and Artificial Neural Networks (ANNs)"** (Springer book chapter,
  doi:10.1007/978-3-032-08894-9_11, published 2 January 2026) — found while searching for
  diffuse optical tomography (DOT) coverage. Solves a generic 1D Cartesian and radial
  diffusion equation via PINN/ANN with a Laplace-domain/Stehfest-inversion setup — a strong
  signature of a reservoir-engineering/well-testing application, not an optical or
  biological-tissue one; no DOT or optical framing found in the available abstract-level
  material (full chapter paywalled). Excluded as off-domain. See `frontier_map.md` for the
  full DOT search writeup.
