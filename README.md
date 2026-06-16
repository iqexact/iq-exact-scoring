# IQ Exact — Open Scoring Methodology

Transparent IQ scoring for [IQ Exact](https://iqexact.com): formulas, norm tables, and reference code.

**This repository documents scoring only.** It does not include test items, answer keys, or the web application.

## Quick verify

After taking the test, compare your **raw score** (correct out of 22) with the lookup table:

```bash
python scripts/verify_result.py --raw 17 --norms v0
```

Or open [`norms/v0/lookup-raw-iq.json`](norms/v0/lookup-raw-iq.json) and find your row.

## Contents

| Path | Description |
|------|-------------|
| [`METHOD.md`](METHOD.md) | Full scoring methodology (English) |
| [`norms/v0/`](norms/v0/) | Norm version **v0** — IRT parameters (no answer keys) + raw→IQ lookup |
| [`reference/score.py`](reference/score.py) | Reference EAP 2PL implementation |
| [`scripts/verify_result.py`](scripts/verify_result.py) | CLI to look up IQ from raw score |
| [`ATTRIBUTION.md`](ATTRIBUTION.md) | OMIB / Koch et al. (2022) attribution |

## Scientific basis

- **Item bank:** Open Matrices Item Bank (OMIB)
- **Paper:** Koch, M., Spinath, F. M., Greiff, S., & Becker, N. (2022). *Journal of Intelligence*, 10(3), 41. [DOI 10.3390/jintelligence10030041](https://doi.org/10.3390/jintelligence10030041)
- **Model:** 2PL IRT, EAP estimation, IQ = 100 + 15θ
- **Calibration sample:** N = 2561 (OMIB norming study)

## Norm versions

| Version | Status | Folder |
|---------|--------|--------|
| **v0** | Current (production) | [`norms/v0/`](norms/v0/) |

Each IQ Exact result includes a `norms_version` field pointing to the norm set used.

## What is **not** published here

- Answer keys (`Item Solution` bitstrings)
- Test item graphics or rendering code
- User data

You can verify your IQ from **raw score** and published formulas without answer keys.

## License

- Reference code in this repo: [MIT](LICENSE)
- OMIB item bank: [GPLv3](ATTRIBUTION.md) — see attribution file

## Regenerating norms (IQ Exact team)

From the main product repo:

```bash
python product/scripts/export_github_scoring.py
```

Copies public JSON from `product/backend/scoring/scoring.json` (strips `solution` fields).
