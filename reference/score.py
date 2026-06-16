#!/usr/bin/env python3
"""
Reference IQ scorer for IQ Exact (public norms, no answer keys).

Supports:
  - EAP 2PL when given a 0/1 response vector (22 values, Form A order)
  - Lookup by raw score (matches norms/v0/lookup-raw-iq.json)

Does NOT grade raw 20-bit answer strings (answer keys are not published).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

_QUAD_POINTS = 121
_THETA_LO, _THETA_HI = -4.0, 4.0
_Z95 = 1.96

REPO_ROOT = Path(__file__).resolve().parents[1]


def _normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _p_2pl(theta: float, a: float, b: float) -> float:
    return 1.0 / (1.0 + math.exp(-a * (theta - b)))


class ScoringReference:
    def __init__(self, norms_version: str = "v0", repo_root: Path | None = None):
        root = repo_root or REPO_ROOT
        base = root / "norms" / norms_version
        with open(base / "scoring-params.json", encoding="utf-8") as f:
            self.params = json.load(f)
        with open(base / "lookup-raw-iq.json", encoding="utf-8") as f:
            self.lookup = json.load(f)

        self.items = self.params["items"]
        self.n = self.params["n_items"]
        self.iq_min, self.iq_max = self.params["scale"]["iq_clamp"]
        self.display_ceiling = self.params["scale"]["iq_display_ceiling"]

        step = (_THETA_HI - _THETA_LO) / (_QUAD_POINTS - 1)
        self._grid = [_THETA_LO + step * k for k in range(_QUAD_POINTS)]
        self._prior = [math.exp(-t * t / 2.0) for t in self._grid]

    def eap(self, u: list[int]) -> tuple[float, float]:
        if len(u) != self.n:
            raise ValueError(f"Expected {self.n} responses, got {len(u)}")
        num = den = num2 = 0.0
        for theta, prior in zip(self._grid, self._prior):
            like = prior
            for it, ui in zip(self.items, u):
                p = _p_2pl(theta, it["a"], it["b"])
                like *= p if ui else (1.0 - p)
            num += theta * like
            den += like
            num2 += theta * theta * like
        theta_hat = num / den
        var = max(num2 / den - theta_hat * theta_hat, 1e-9)
        return theta_hat, math.sqrt(var)

    def score_vector(self, u: list[int]) -> dict:
        raw = sum(u)
        theta, se = self.eap(u)
        iq_exact = 100.0 + 15.0 * theta
        iq = self._clamp(iq_exact)
        return {
            "raw_score": raw,
            "max_score": self.n,
            "theta": round(theta, 3),
            "se_theta": round(se, 3),
            "iq": iq,
            "iq_display": self._display(iq),
            "iq_ci95": [
                self._clamp(iq_exact - _Z95 * 15.0 * se),
                self._clamp(iq_exact + _Z95 * 15.0 * se),
            ],
            "percentile": round(_normal_cdf(theta) * 100.0, 1),
            "category": self._category(iq),
            "method": "EAP (2PL IRT)",
            "norms_version": self.params["norms_version"],
        }

    def score_by_raw(self, raw: int) -> dict:
        if not 0 <= raw <= self.n:
            raise ValueError(f"raw must be 0..{self.n}")
        row = self.lookup["rows"][raw]
        return {
            "raw_score": raw,
            "max_score": self.n,
            "theta": row["theta"],
            "iq": row["iq"],
            "iq_display": self._display(row["iq"]),
            "iq_ci95": row["iq_ci95"],
            "percentile": row["percentile"],
            "category": self._category(row["iq"]),
            "method": "TCC lookup table",
            "norms_version": self.params["norms_version"],
            "boundary": row.get("boundary", False),
        }

    def _clamp(self, iq: float) -> int:
        return max(self.iq_min, min(self.iq_max, round(iq)))

    def _display(self, iq: int) -> str:
        if iq >= self.display_ceiling:
            return f"{self.display_ceiling}+"
        if iq <= 65:
            return "<=65"
        return str(iq)

    def _category(self, iq: int) -> str:
        for c in self.params["categories"]:
            if iq <= c["max_iq"]:
                return c["label"]
        return self.params["categories"][-1]["label"]


if __name__ == "__main__":
    scorer = ScoringReference()
    print("Lookup raw=17:", scorer.score_by_raw(17))
    demo = scorer.score_vector([1] * 13 + [0] * 9)
    print("EAP 13/22:", demo["iq_display"], demo["iq_ci95"])
