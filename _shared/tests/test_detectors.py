"""Tests for _shared/detectors — unified change detection."""

from __future__ import annotations

import pytest
from _shared.detectors import detect_change, OnlineDetector, DetectionResult
from _shared.detectors.bayesian_bridge import BayesianDetector, BayesianSignal
from _shared.detectors.zscore_bridge import ZScoreMonitor, ZScoreSignal


class TestDetectChange:
    def test_detects_anomaly(self):
        result = detect_change([100, 105, 102, 98, 200, 210, 205])
        assert result.is_anomaly is True
        assert result.method in ("bayesian", "zscore")

    def test_normal_sequence_no_anomaly(self):
        result = detect_change([100, 101, 99, 100, 102, 98, 101])
        assert result.is_anomaly is False

    def test_auto_selects_bayesian_when_available(self):
        result = detect_change([1, 2, 1, 2, 10], method="auto")
        assert result.method == "bayesian"

    def test_short_sequence_returns_no_anomaly(self):
        result = detect_change([1])
        assert result.is_anomaly is False
        assert result.description == "数据点不足（需 ≥2）"

    def test_zscore_method_works(self):
        result = detect_change([100, 101, 99, 100, 200], method="zscore")
        assert isinstance(result, DetectionResult)
        assert result.z_score is not None


class TestOnlineDetector:
    def test_streaming_detects_anomaly_eventually(self):
        det = OnlineDetector(method="zscore", window=5)
        for v in [100, 101, 99, 100, 102]:
            det.update(v)
        result = det.update(300)
        assert result.is_anomaly is True

    def test_reset_clears_buffer(self):
        det = OnlineDetector(method="zscore", window=5)
        det.update(100)
        det.reset()
        result = det.update(999)
        assert result.is_anomaly is False  # buffer too small


class TestBayesianDetector:
    def test_detects_anomaly(self):
        bd = BayesianDetector(prior_mean=100, prior_std=15)
        for v in [100, 102, 98, 105]:
            bd.update(v)
        result = bd.update(200)
        assert result.is_anomaly is True
        assert isinstance(result, BayesianSignal)

    def test_ci_95_is_valid(self):
        bd = BayesianDetector(prior_mean=100, prior_std=20)
        for v in [100, 105, 98, 102]:
            bd.update(v)
        result = bd.update(103)
        lo, hi = result.ci_95
        assert lo <= hi

    def test_status_returns_dict(self):
        bd = BayesianDetector()
        s = bd.status()
        assert s["method"] == "bayesian"

    def test_fuse_combines_signals(self):
        s1 = BayesianSignal(is_anomaly=True, confidence=0.8, z_score=3.0, deviation=10,
                            ci_95=(90, 110), posterior_mean=100, posterior_std=5,
                            description="anomaly")
        s2 = BayesianSignal(is_anomaly=False, confidence=0.2, z_score=0.5, deviation=1,
                            ci_95=(95, 105), posterior_mean=100, posterior_std=3,
                            description="normal")
        fused = BayesianDetector.fuse([s1, s2])
        assert fused.is_anomaly is True  # any anomaly = anomaly
        assert 0.3 < fused.confidence < 0.9


class TestZScoreMonitor:
    def test_detects_anomaly(self):
        zm = ZScoreMonitor(threshold=3.0, window=5)
        for v in [100, 101, 99, 100, 102]:
            zm.record("test", v)
        result = zm.record("test", 300)
        assert result.is_anomaly is True
        assert isinstance(result, ZScoreSignal)

    def test_short_window_no_anomaly(self):
        zm = ZScoreMonitor(threshold=3.0, window=5)
        result = zm.record("test", 100)
        assert result.is_anomaly is False

    def test_health_returns_info(self):
        zm = ZScoreMonitor(threshold=3.0)
        zm.record("m1", 100)
        zm.record("m2", 200)
        h = zm.health()
        assert "metrics" in h
        assert len(h["metrics"]) == 2
