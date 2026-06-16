# Norms v0

**Status:** current production norms for IQ Exact  
**Release tag:** `norms-v0`  
**Date:** 2026-06-11

## Files

| File | Purpose |
|------|---------|
| `scoring-params.json` | Form A item parameters (`a`, `b`), scale definition, categories — **no answer keys** |
| `lookup-raw-iq.json` | Raw score (0–22) → θ, IQ, 95% CI, percentile |

## Scale

- **Model:** 2PL IRT, EAP estimation (121 quadrature nodes on θ ∈ [−4, 4])
- **IQ formula:** IQ = 100 + 15 × θ̂
- **Display clamp:** 55–145; ceiling label **128+** above measurement range
- **Best precision:** IQ ≈ 75–125 (SEM roughly ±4–8 IQ points)

## Verify your result

1. From your IQ Exact report, note **raw score** (e.g. 17 / 22).
2. Run: `python ../../scripts/verify_result.py --raw 17 --norms v0`
3. Compare IQ and CI with your paid report (same `norms_version: v0`).

Pattern-specific EAP scores may differ slightly from lookup rows when errors fall on harder vs easier items; lookup assumes a simplified TCC inversion by raw total.

## Source

Generated from IQ Exact internal calibration export (OMIB Koch et al., 2022).  
Regenerate via `product/scripts/export_github_scoring.py` in the main product workspace.
