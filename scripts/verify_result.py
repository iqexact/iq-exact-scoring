#!/usr/bin/env python3
"""Verify IQ from raw score using published norm tables."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reference"))
from score import ScoringReference  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(
        description="Look up IQ Exact score from raw correct count (Form A, 22 items)."
    )
    p.add_argument("--raw", type=int, required=True, help="Number correct (0–22)")
    p.add_argument("--norms", default="v0", help="Norm version folder (default: v0)")
    args = p.parse_args()

    try:
        scorer = ScoringReference(norms_version=args.norms)
        r = scorer.score_by_raw(args.raw)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"Norms version: {r['norms_version']}")
    print(f"Raw score:     {r['raw_score']} / {r['max_score']}")
    print(f"IQ (Gf):       {r['iq_display']}")
    print(f"95% CI:        {r['iq_ci95'][0]}–{r['iq_ci95'][1]}")
    print(f"Percentile:    {r['percentile']}%")
    print(f"Category:      {r['category']}")
    print(f"Method:        {r['method']}")
    if r.get("boundary"):
        print("Note: boundary raw score — production uses EAP for fine-grained estimate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
