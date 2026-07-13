"""Tests for _bayesian core engine."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _bayesian import BetaBelief, NormalBelief, DirichletBelief
from _bayesian.self_check import SelfCheckReport

class TestBetaBelief:
    def test_prior_mean(self):
        b = BetaBelief(alpha=2, beta=2)
        assert b.mean() == 0.5
    def test_update(self):
        b = BetaBelief(alpha=2, beta=2)
        b.update(successes=8, trials=10)
        assert 0.7 < b.mean() < 0.8
    def test_credible_interval(self):
        b = BetaBelief(alpha=2, beta=2)
        b.update(successes=5, trials=10)
        lo, hi = b.credible_interval()
        assert lo < hi
    def test_weight(self):
        b = BetaBelief(alpha=1, beta=1)
        b.update(successes=5, trials=10)
        assert b.weight() > 10
    def test_fusion(self):
        b1 = BetaBelief(alpha=5, beta=2)
        b2 = BetaBelief(alpha=3, beta=4)
        fused = b1 + b2
        assert fused is not None

class TestNormalBelief:
    def test_prior(self):
        n = NormalBelief(mu=0, sigma=10)
        assert n.mean() == 0
    def test_update(self):
        n = NormalBelief(mu=0, sigma=10)
        n.update(observations=[5.0, 5.5, 4.8, 5.2, 5.1])
        assert 4.0 < n.mean() < 6.0
    def test_credible_interval(self):
        n = NormalBelief(mu=0, sigma=10)
        n.update(observations=[1, 2, 3])
        lo, hi = n.credible_interval()
        assert lo < hi

class TestDirichletBelief:
    def test_prior_sum_to_one(self):
        d = DirichletBelief(alphas=[1, 1, 1])
        assert abs(sum(d.mean()) - 1.0) < 0.01
    def test_update(self):
        d = DirichletBelief(alphas=[1, 1, 1])
        d.update(observations=[0, 1, 2, 0, 1, 0])
        means = d.mean()
        assert means[0] > means[1]

class TestSelfCheck:
    def test_beta_self_check(self):
        b = BetaBelief(alpha=2, beta=2)
        b.update(successes=5, trials=10)
        report = b.self_check()
        assert isinstance(report, SelfCheckReport)
