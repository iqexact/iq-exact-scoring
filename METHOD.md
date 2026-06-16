# IQ Exact Scoring Methodology — OMIB Fluid Reasoning Test

**Norm version:** v0 (OMIB calibration anchor)  
**Document date:** 2026-06-11  
**Status:** production methodology for IQ Exact ([iqexact.com](https://iqexact.com))

This document describes how **IQ Exact** converts responses on Form A (22 matrix items) into a fluid intelligence (Gf) score. Answer keys are **not** published; verification is by **raw score** and the lookup table in [`norms/v0/lookup-raw-iq.json`](norms/v0/lookup-raw-iq.json).

---

## 1. Scientific basis

| Parameter | Value |
|---|---|
| Item source | Open Matrices Item Bank (OMIB) |
| Publication | Koch, M., Spinath, F. M., Greiff, S., & Becker, N. (2022). *Journal of Intelligence*, 10(3), 41. [DOI 10.3390/jintelligence10030041](https://doi.org/10.3390/jintelligence10030041) |
| Calibration sample | N = 2561, German medical university applicants, mean age 19.3 (15–45), 73% female |
| Calibration conditions | Online, unproctored, **no time limit** (mean ~26 min) |
| Psychometric model | 2PL IRT, calibrated with mirt + equateMultiple (R) |
| Reliability | α ≈ 0.92 |
| Construct | Fluid reasoning (Gf) |
| OMIB license | GPLv3 |

**What the test measures:** inductive reasoning on figural matrices (Gf). It is **not** a full clinical IQ battery (WAIS, Stanford-Binet). Users are informed explicitly.

---

## 2. Test form (fixed)

**Form A = OMIB Set 1: 22 items**, fixed order (by increasing rule count). Anchor items 1–6 are not included in this 22-item form.

### 2.1 Form A composition (calibration parameters)

| # | Item ID | Rules | mean (p) | b (difficulty) | a (discrimination) |
|---|---------|-------|----------|----------------|---------------------|
| 1 | 1 | 1 | 0.95 | -1.28 | 2.48 |
| 2 | 2 | 1 | 0.95 | -1.49 | 2.04 |
| 3 | 21 | 2 | 0.84 | -0.73 | 1.74 |
| 4 | 22 | 2 | 0.64 | 0.13 | 1.90 |
| 5 | 23 | 2 | 0.82 | -0.64 | 1.70 |
| 6 | 24 | 2 | 0.85 | -0.96 | 1.43 |
| 7 | 25 | 2 | 0.84 | -1.28 | 1.02 |
| 8 | 71 | 3 | 0.73 | -0.35 | 1.33 |
| 9 | 72 | 3 | 0.61 | 0.04 | 1.05 |
| 10 | 73 | 3 | 0.74 | -0.37 | 1.39 |
| 11 | 74 | 3 | 0.91 | -1.06 | 1.94 |
| 12 | 75 | 3 | 0.61 | 0.21 | 1.81 |
| 13 | 76 | 3 | 0.65 | 0.02 | 1.44 |
| 14 | 77 | 3 | 0.69 | -0.20 | 1.34 |
| 15 | 78 | 3 | 0.78 | -0.24 | 2.41 |
| 16 | 151 | 4 | 0.53 | 0.43 | 1.51 |
| 17 | 152 | 4 | 0.60 | 0.27 | 1.93 |
| 18 | 153 | 4 | 0.64 | 0.03 | 1.44 |
| 19 | 154 | 4 | 0.67 | 0.22 | 4.05 |
| 20 | 155 | 4 | 0.64 | 0.21 | 2.44 |
| 21 | 201 | 5 | 0.31 | 1.11 | 1.74 |
| 22 | 202 | 5 | 0.55 | 0.44 | 2.58 |

Rule structure: 2×(1 rule), 5×(2), 8×(3), 5×(4), 2×(5).

Full machine-readable parameters: [`norms/v0/scoring-params.json`](norms/v0/scoring-params.json).

### 2.2 Administration (IQ Exact product)

| Parameter | Value |
|---|---|
| Practice items | 2, with feedback |
| Time limit | Soft recommendation ~30 min; no hard auto-submit in v0 |
| Item order | Fixed, ascending rule count |
| Skipped items | Count as incorrect (u_i = 0) |

---

## 3. Scoring algorithm

### Step 1. Item score

User response: 20-bit string (selected construction elements).

```
u_i = 1  if response string equals the item key (exact match)
u_i = 0  otherwise (including skip, empty, partial — no partial credit)
```

*Item keys are stored server-side only and are not published in this repository.*

### Step 2. Raw score

```
raw = Σ u_i     (0 … 22)
```

### Step 3. Ability estimate θ — EAP (primary)

2PL model per item:

```
P_i(θ) = 1 / (1 + exp(−a_i · (θ − b_i)))
```

Likelihood:

```
L(θ) = Π  P_i(θ)^u_i · (1 − P_i(θ))^(1−u_i)
```

EAP with N(0,1) prior:

```
θ̂ = Σ_k [θ_k · L(θ_k) · φ(θ_k)] / Σ_k [L(θ_k) · φ(θ_k)]
```

Quadrature: θ_k from −4 to +4, step 8/120 (121 nodes).

Posterior SD:

```
SE(θ̂) = sqrt( E[θ²|u] − θ̂² )
```

**Why EAP:** stable at extreme patterns (0/22, 22/22) where MLE diverges.

Implementation: [`reference/score.py`](reference/score.py).

### Step 4. IQ scale

```
IQ = 100 + 15 · θ̂
IQ_display = clamp(round(IQ), 55, 145)

CI95 = [IQ − 1.96·15·SE(θ̂);  IQ + 1.96·15·SE(θ̂)]
```

After test equating, θ ~ N(0,1) on the OMIB calibration sample, so IQ = 100 + 15θ is standard metric (M=100, SD=15) relative to that sample.

### Step 5. Percentile

```
percentile = Φ(θ̂) × 100
```

Φ = standard normal CDF. Interpretation: “better than X% of the calibration sample.”

---

## 4. Raw score → IQ lookup (Form A)

Built by inverting the test characteristic curve TCC(θ) = Σ P_i(θ). Used for verification, caching, and fallback.

**Full table:** [`norms/v0/lookup-raw-iq.json`](norms/v0/lookup-raw-iq.json)

| Raw | IQ | 95% CI (approx.) | Percentile |
|-----|-----|------------------|------------|
| 0 | 55 | 55–103 | <1% |
| 5 | 83 | 73–92 | 12% |
| 10 | 95 | 87–103 | 37% |
| 13 | 101 | 94–108 | 53% |
| 17 | 110 | 101–118 | 74% |
| 20 | 120 | 107–134 | 91% |
| 21 | 128 | 108–145 | 97% |
| 22 | 145* | 65–145 | >99% |

\* At raw 0 and 22, TCC inversion hits scale bounds; production uses EAP (~≤65 and ~≥130 display). See boundary notes in lookup JSON.

**Anchor points:**
- IQ 100 ≈ **12–13** correct (E(raw|θ=0) ≈ 12.4)
- IQ 110 ≈ **17** correct
- IQ 120 ≈ **20** correct

---

## 5. Measurement precision

Information I(θ) = Σ a_i² P_i(θ)(1−P_i(θ)), SEM(θ) = 1/√I(θ).

**Practical range:** IQ **75–125** (SEM roughly ±4–8 IQ points).  
Above ~**128**, Form A hits a measurement ceiling — reported as **128+**.

---

## 6. Result categories

| IQ | Category |
|----|----------|
| ≤ 79 | Below average |
| 80–89 | Slightly below average |
| 90–109 | Average |
| 110–119 | Above average |
| 120–127 | High |
| 128+ | Very high (measurement ceiling) |

---

## 7. User-facing report (after payment)

1. Gf IQ index  
2. 95% confidence interval (always)  
3. Percentile vs calibration sample  
4. Raw score (N / 22)  
5. Category  
6. Methodological disclaimer (see §8)

---

## 8. Required disclaimer (site / certificate)

> This test measures fluid intelligence (Gf) using figural matrices from the OMIB item bank (Koch et al., 2022, *Journal of Intelligence*, DOI: 10.3390/jintelligence10030041). Scores use 2PL IRT (EAP) with published calibration parameters (N = 2561, German university applicants, mean age ~19, unproctored, untimed calibration). Scale: M = 100, SD = 15 relative to the calibration sample. Not a clinical diagnosis (WAIS, Stanford-Binet); no age norms in v0.

---

## 9. Known limitations (v0)

| # | Limitation | Planned mitigation |
|---|------------|-------------------|
| 1 | Norms: German applicants ~19y, not general population | v1: re-anchor on IQ Exact sample (500–1000+) |
| 2 | Unproctored calibration → possible inflation | Stated in disclaimer; v1 own norms |
| 3 | Ceiling ~IQ 128 (22 items) | Expand form with anchors / more items |
| 4 | No age norms | v2 at N ≥ 2000 |
| 5 | Percentile via normal CDF, not empirical | v1 empirical percentiles |

---

## 10. Norm versioning

| Version | Trigger | Change |
|---------|---------|--------|
| **v0** (current) | — | OMIB anchor: θ~N(0,1) → IQ=100+15θ |
| v1 | ≥ 500–1000 completions | Re-center on IQ Exact sample |
| v2 | ≥ 2000 | Age groups, optional timed/untimed splits |

Each issued result stores `norms_version`. GitHub release tags match (`norms-v0`, …).

---

## 11. Reproducibility (without answer keys)

You **can** verify:

- Raw score → IQ via [`lookup-raw-iq.json`](norms/v0/lookup-raw-iq.json) or `scripts/verify_result.py`
- EAP formula via [`reference/score.py`](reference/score.py) if you supply a 0/1 vector

You **cannot** reproduce item-level grading from this repo alone (by design).

Official OMIB parameters: supplementary [Table S1](https://pmc.ncbi.nlm.nih.gov/articles/PMC9326670/) and [DOI paper](https://doi.org/10.3390/jintelligence10030041).

---

*IQ Exact · norms v0 · [GitHub](https://github.com/iqexact/iq-exact-scoring)*
