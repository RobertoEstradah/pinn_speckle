# Manuscript Review — Tesis UJAT: Simulación acelerada de speckle óptico con PINN-SIREN

**Date:** 2026-08-21
**Reviewer:** writer-critic
**Artifact:** `tesis/fuente_conNB03/main.tex` and included files
**Paper type:** Descriptive/Methodological — computational engineering thesis (non-causal). INV-8 (causal-language check), INV-4/6 (AEA stars, JEL codes) do not apply; INV-9/10 (biblatex/biber, hyperref+cleveref) evaluated only where the working-paper-format.md rule is generically applicable, per task instructions.
**Score:** 0/100 (see Score Breakdown — deductions from independently blocking Critical issues exceed 100; floored per rubric)
**Mode:** Full (8 categories)

Note on tooling: I do not have a Bash/Write tool in this session, so I did not execute `latexmk`. The compilation verdict below is based on static analysis (missing `\include` target, undefined macro) rather than an actual compile run — this should be confirmed by an actual compile pass, but the evidence is unambiguous.

---

## 1. Structure and Flow: ISSUES

- **Missing Conclusiones/Discusión/Trabajo-futuro chapter — Major.** `tesis/fuente_conNB03/main.tex:132-135` includes only `Cap1-Generalidades`, `Cap2-Marcos`, `Cap3-Modelo`, `Cap4-Resultados`. There is no `Cap5-Conclusiones` (or equivalent). A UJAT maestría thesis is expected to close with a dedicated conclusions/discussion/future-work chapter that synthesizes the three hypotheses, discusses the unmet objective (NB04/FEM benchmark), and gives closure. `Cap4-Resultados.tex:415-448` ("Resumen de experimentos completados") gestures at this but is a results-chapter subsection, not a conclusions chapter. As currently structured, the document ends abruptly on a results table.
- Introduction (Cap1 §Introducción, `Cap1-Generalidades.tex:3-44`) follows a reasonable motivation → bottleneck → PINN → SIREN → positioning arc, appropriate for a methodological thesis.
- The explicit "brecha en el conocimiento" (gap) statement is deferred to Cap2 (`Cap2-Marcos.tex:229-233`) rather than stated in Cap1's introduction. Not a violation for a UJAT thesis format (separate marco teórico chapter is standard), but worth noting since it means the reader doesn't get the contribution statement in the first pages.
- Objectives, hypotheses, scope/limitations, and methodology-by-phase sections in Cap1 are clear and well organized (`Cap1-Generalidades.tex:120-247`).

## 2. Claims and Evidence: GAPS

- **No claim-source map exists (INV-22) — Critical.** Searched `quality_reports/` for `claim_source_map*` — no file found (only `2026-05-31_comprehensive_review.md` and `2026-06-08_comia_paper_review.md` exist, neither is a claim-source map). Every numerical claim in the manuscript (L² errors, contrast, KS statistic, multiseed stats, ablation values, parameter counts) currently has no documented script-line/output-file trace.
- **Abstract overclaim without caveat — Major.** `Abstract.tex:10-13` and `Resumen.tex:11-14` state "outperforming the state-of-the-art by factors of ×415 and ×11.2" as an unqualified headline claim. The necessary caveat — that Schoder et al. (2024) is a 3D feasibility study using `tanh` activation and FEM references, while this thesis compares only the 1D/2D adimensional sub-components with a different architecture — exists only in the *table note* of `Cap4-Resultados.tex:402-410` ("El factor de mejora refleja tanto la ventaja arquitectural de SIREN sobre tanh/ReLU como la diferencia de complejidad dimensional"), not in the Abstract/Resumen where the number is first presented to a reader. This is a fairness-of-comparison issue that should be hedged where the number is headlined.
- Where verifiable, the headline numbers are internally consistent: Abstract and Resumen match each other exactly (0.006%, 0.171%, ×415, ×11.2, C=1.0253, 0.155±0.020%), and match `results/multiseed_results.json` and `results/ablation_lambda.json` exactly for NB02/multiseed/ablation values. The ×415 and ×11.2 factors are arithmetically correct (2.49/0.006≈415; 1.91/0.171≈11.2).
- See Category 8 for specific numeric mismatches against the project's verified hyperparameter record (also implicates INV-11/INV-22 traceability).

## 3. Identification / Methodology Fidelity: MISREPRESENTED (partial)

- **NB01 boundary condition description omits the documented anti-collapse fix — Major.** `Cap3-Modelo.tex:14-21` (eq. `helmholtz1d`) and `Cap4-Resultados.tex:17-19` both describe the NB01 Dirichlet boundary conditions as only two points: $E(0)=1$, $E(1)=\cos(k)$. Per the project's own documented history (`CLAUDE.md` hyperparameter table: "N_boundary 5 pts (0,0.25,0.5,0.75,1)" for NB01; "Problemas Resueltos" table: "BCs simétricas E(0)=E(1)=1 colapsan a constante → Agregar puntos intermedios conocidos"), the actual, working NB01 configuration uses **5** boundary points, because the naive 2-point (or symmetric) BC collapses the network to a constant solution. The thesis's methodology section describes the naive setup that is documented elsewhere as *not working*, without mentioning the fix that was actually applied. A reader trying to reproduce NB01 from Chapter 3/4 alone would hit the documented failure mode. This is a real fidelity gap between the described methodology and the actual, verified experimental design.
- No causal claims are made anywhere; the physics/statistical claims (contrast, KS, tail fraction) are appropriately framed as descriptive validation against Goodman's theoretical criteria, with the KS test's low p-value honestly discussed as a statistical-power artifact rather than suppressed (`Cap4-Resultados.tex:327-333`) — this is good practice and should be credited.
- The unmet objective (NB04/FEM benchmark, "Pendiente") is transparently disclosed (`Cap4-Resultados.tex:420-448`), which is appropriate — not treated as a violation.

## 4. Writing Quality: CLEAN (mostly)

- Prose is technical, direct, and largely free of AI-writing tells. Em dash usage is low (5 instances across all four chapters — well under thresholds). Only one mild significance-inflation phrase found: "Un resultado notable de este experimento..." (`Cap4-Resultados.tex:373`) — below the 3-instance threshold for deduction.
- No filler phrases, no "In the next section we will..." announcements, no vague attributions detected in the searched patterns.
- **Minor:** Title-page grammar/typo. `main.tex:66-67`: `\newcommand{\Titulo}{Simulación acelerada de speckle óptico: Un enfoque basado redes neuronales físicamente informadas (PINN's)}` is missing the preposition "en" ("basado **en** redes neuronales") and uses an incorrect English-plural apostrophe ("PINN's" should be "PINNs"). The project's own roadmap document (`docs/RUTA_TESIS_ROBERTO_HERNANDEZ_ESTRADA.pdf`, p.1) has the correct phrasing ("Un enfoque basado **en** redes neuronales físicamente informadas (PINNs)"), confirming this is a regression/typo, not a deliberate title choice. This is the thesis title — it appears on the cover page, in `Declaracion-autoria.tex:17`, and in `Cesion-derechos.tex:16`.

## 5. LaTeX and Format: ISSUES

- No `\hline` anywhere in the source (verified via grep across `tesis/fuente_conNB03`) — booktabs (`\toprule`/`\midrule`/`\bottomrule`) used consistently. INV-3 compliant.
- All 6 tables use `threeparttable` + `\begin{tablenotes}` with substantive notes (sample/mesh size, architecture, GPU, seed). INV-1 compliant.
- All figure captions include explanatory notes (what is shown, how to read it, key metric values, GPU/seed). INV-2 compliant on the caption side.
- **INV-12 violation — figure titles baked into the images themselves, Major (-9, capped).** I opened `figures/resultados_pinn_1d.png` and `figures/resultados_speckle_nb03.png` directly. Both contain prominent matplotlib `suptitle`/`title` text baked into the raster image: e.g., "Resultados PINN 1D — Helmholtz", "PINN vs Solución Analítica — Helmholtz 1D (k = 2π) / Error L2 = 0.006% | Meta tesis: <5%", "PINN 2D — Speckle Óptico SIREN (ω₀=1.0) | k=2π | C = 1.0253 | KS p = 0.0000 | N_φ = 256", plus per-subplot titles like "E_real — Predicción PINN". These are full descriptive titles, not the INV-12-exempted "Panel A: ..." style sub-panel labels — the information duplicates and partially conflicts with what belongs in the LaTeX `\caption{}` (e.g., the image says "KS p = 0.0000" while the LaTeX table reports "$< 0.0001$" — not contradictory but redundant and a maintenance risk). Given both sampled figures show this pattern, it likely affects all 6 figures referenced in `Cap4-Resultados.tex` (`resultados_pinn_1d.png`, `metricas_adicionales_1d.png`, `resultados_pinn_2d.png`, `metricas_adicionales_2d.png`, `resultados_speckle_nb03.png`, `estadistica_speckle_nb03.png`), though only the two above were directly inspected.
- Manual `Tabla~\ref{}` / `Figura~\ref{}` / `Capítulo~\ref{}` / `Sección~\ref{}` used consistently (13 instances checked) instead of `cleveref`. `cleveref` is not loaded in `main.tex`. Per the task's instructions this is *not* penalized — `working-paper-format.md`'s hyperref/cleveref requirement is a working-paper (economics) convention and does not apply to this UJAT `report`-class thesis; the manual referencing style used here is internally consistent, which is what matters.
- `biblatex` + `biber`, `style=apa` — appropriate for UJAT APA format (`main.tex:33`).

## 6. Compilation: FAIL (static analysis; not executed)

- **Critical — missing include target.** `main.tex:106`: `\include{PortadaBlanca}`. No `PortadaBlanca.tex` exists in `tesis/fuente_conNB03/` — only a stale `PortadaBlanca.aux` from a prior compile was found. Current source will fail with "File `PortadaBlanca.tex' not found" on this `\include`.
- **Critical — undefined macro.** `Portada.tex:51` and `Portada.tex:97` both use `\Codirector` (`{\bfseries\MakeUppercase\Codirector}`). `main.tex` defines `\Titulo`, `\Autor`, `\Matricula`, `\Grado`, `\Nivel`, `\Director`, `\DirectorGrado`, `\Ciudad`, `\Mes`, `\Anho`, `\Dia`, `\DiaLetra` (lines 66-78) — **`\Codirector` is never defined anywhere in the source tree** (confirmed via grep across the whole `tesis/fuente_conNB03` directory: only match is the two usages in `Portada.tex`). This produces an "Undefined control sequence" error on both the blue and white cover pages.
- A stale `main.pdf` exists in the directory from a prior successful build, which may mask this regression if the author isn't recompiling from a clean tree — worth flagging explicitly since `git status` shows `tesis/` as entirely untracked (`??`), i.e., no prior committed-good version to fall back to.
- Cannot verify `\ref{}`/`\cite{}` resolution or hbox warnings without an actual compile pass; recommend running `latexmk` after fixing the two blockers above.

## 7. Voice Fidelity: NOT SCORED

`.claude/references/personal-style-guide.md` contains only the unfilled template (bracketed placeholders throughout, no extracted corpus). Per protocol, voice fidelity is not scored. Run `/write style-guide [paper-dir]` to enable this check in a future pass.

## 8. Notation Consistency: INCONSISTENCIES

- **Symbol collision: $d$ — Major (INV-7).** `Cap3-Modelo.tex:70-71` defines $d$ as the hidden-layer width ("Capas ocultas: $L=5$ capas de dimensión $d$ neuronas cada una ($d=64$ en NB01, $d=128$ en NB02/NB03)"). The same chapter, ~60 lines later, `Cap3-Modelo.tex:133` reuses $d$ for the LHS sampling dimensionality: "usando `scipy.stats.qmc.LatinHypercube` con dimensión $d = 2$." Two unrelated quantities share the same symbol within the same chapter.
- **Introduced-then-abandoned symbol — Minor.** `Cap3-Modelo.tex:8`: "el número de onda adimensional es $\tilde{k} = 2\pi$" introduces a tilde notation for the dimensionless wavenumber, but every subsequent equation in Cap2 and Cap3 (eqs. `helmholtz`, `helmholtz2d`, `helmholtz1d`, `solucion2d`, etc.) uses plain $k$, never $\tilde{k}$ again. Either drop the tilde at first use or use it consistently.
- Elsewhere notation is consistent: $E_\text{real}/E_\text{imag}$, $\lambda_\text{fís}$, $N_c$/$N_b$/$N_\phi$, $C=\sigma_I/\langle I\rangle$, $\omega_0$ are used identically across Cap2, Cap3, and Cap4, and match between prose and table headers.

### Numeric mismatches against the project's verified record (cited in `CLAUDE.md`) — Critical, INV-11/INV-22

| Claim | Manuscript value | Verified value (CLAUDE.md) | Location |
|---|---|---|---|
| NB01 parameter count | "${\sim}8{,}400$ parámetros" | 16,833 params (SIREN 5×64) | `Cap3-Modelo.tex:75`; `Cap4-Resultados.tex:15-16` |
| NB01 collocation points | "$N_c = 1{,}000$ puntos uniformes" | 2,000 uniforme | `Cap4-Resultados.tex:17` |
| NB01 L-BFGS history size | "100" (table row lists NB01 together with NB02/NB03) | 50 (NB01 max_iter/history = 500/50; NB02/03 = 1,000/100) | `Cap3-Modelo.tex:168` (Tabla `tab:hiperparametros`) |
| Python version | "Python 3.14" | Python 3.11 (per `environment.yml` / project env `pinn_speckle`) | `Cap2-Marcos.tex:255` |

These are exactly the kind of claims a claim-source map (missing, see Category 2) should catch — none of the four traces to a script/output that would have produced these specific values.

---

## Score Breakdown

Starting: 100

**Critical:**
- Compilation failure (missing `PortadaBlanca.tex` include + undefined `\Codirector`) — INV-none/format: **-20**
- No claim-source map exists (INV-22) — **-15**
- Numeric mismatches vs. verified project record, 4 instances (NB01 params, NB01 N_c, NB01 L-BFGS history, Python version), capped: **-30**
- Methodology section misrepresents actual NB01 boundary-condition design (omits documented anti-collapse fix) — **-15**

**Major:**
- Missing Conclusiones/Discussion/Future-work chapter (structural gap) — **-10**
- INV-12: figure titles embedded in images across multiple figures — **-9** (capped)
- Notation collision: symbol $d$ reused for two quantities within Cap3 (INV-7) — **-5**
- Abstract states ×415/×11.2 comparison without the dimensionality/method caveat present in the body — **-5**

**Minor:**
- Notation: $\tilde{k}$ introduced then abandoned — **-2**
- Title-page grammar/typo ("basado redes neuronales", "PINN's") — **-3**

Sum of deductions: **-114** → **Final: 0/100** (floored; raw deduction total of 114 reflects that four independently blocking Critical issues co-occur — a compile-breaking bug, an absent traceability infrastructure, real numeric discrepancies against the project's own verified record, and a genuine methodology-fidelity gap. Each alone would already block a "ready" verdict.)

**Reading the score correctly:** this is not a verdict that the underlying research or the bulk of the writing is weak — the physics content, the headline results (L² errors, contrast, multiseed/ablation numbers), the table formatting (INV-1/INV-3 compliant), and the prose quality are largely solid and internally consistent. The score is driven by a small number of concrete, independently fixable defects (two LaTeX bugs, four specific numbers, one missing chapter, one missing tracking artifact, embedded figure titles, two notation slips) that should each be individually correctable in a short revision pass.

## Claim-Source Map Status
- Map exists: **NO**
- Claims mapped: 0/many
- Broken links: N/A (map absent)
- Recommendation: produce `quality_reports/claim_source_map_tesis.md` mapping every numeric claim in Cap4 (and the hyperparameter values in Cap1/Cap3) to the specific script (`notebooks/01_...ipynb`, `notebooks/02_...ipynb`, `notebooks/03_...ipynb`, `scripts/experiments/run_ablation_lambda.py`, `scripts/experiments/run_multiseed.py`) and output file (`results/*.json`) that produced it — this would have caught the four numeric mismatches above.

## Escalation Status: Strike — recommend Orchestrator review

Given the combination of a compile-breaking bug, a methodology-description gap versus the documented actual design, and a missing final chapter, this looks like more than a polish pass: **recommend escalating to the Orchestrator** with the message: "The thesis has structural and fidelity issues beyond prose polish — (1) it does not currently compile due to a missing include file and an undefined macro in the cover-page files, (2) there is no conclusions chapter, (3) the NB01 methodology description in Cap3/Cap4 omits the documented boundary-condition fix that made NB01 actually work. Consider re-drafting the cover-page includes, adding a Conclusiones chapter, and revisiting the NB01 methodology description before the next writer-critic round."

---

**Files reviewed (absolute paths):**
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\main.tex`
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\Portada.tex`
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\Declaracion-autoria.tex`
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\Cesion-derechos.tex`
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\Abstract.tex`
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\Resumen.tex`
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\chapters\Cap1-Generalidades.tex`
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\chapters\Cap2-Marcos.tex`
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\chapters\Cap3-Modelo.tex`
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\chapters\Cap4-Resultados.tex`
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\references.bib`
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\figures\resultados_pinn_1d.png`
- `C:\roberto\Tesis_Maestria\tesis\fuente_conNB03\figures\resultados_speckle_nb03.png`
- `C:\roberto\Tesis_Maestria\results\ablation_lambda.json`
- `C:\roberto\Tesis_Maestria\results\multiseed_results.json`
- `C:\roberto\Tesis_Maestria\CLAUDE.md` (verified-numbers source)
