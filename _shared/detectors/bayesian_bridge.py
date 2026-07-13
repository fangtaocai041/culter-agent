"""
bayesian_bridge — _bayesian 变化检测的适配器包装

在 _shared.detectors 统一接口基础上，提供 _bayesian 专有的功能：
  - 先验注入（利用领域知识）
  - 可信区间量化
  - 信念融合（多源证据合并）

Usage:
    from _shared.detectors.bayesian_bridge import BayesianDetector

    det = BayesianDetector(prior_mean=100, prior_std=20)
    for v in stream:
        signal = det.update(v)
        print(signal.ci_95)  # 95% 可信区间
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from _shared.detectors import DetectionResult, np_mean, np_std


# ── 尝试导入 _bayesian ──────────────────────────────

try:
    from _bayesian.applications.change_point_detector import ChangePointDetector as _CPD
    from _bayesian.engine import NormalBelief as _NormalBelief
    _HAS_BAYESIAN = True
except ImportError:
    _HAS_BAYESIAN = False


@dataclass
class BayesianSignal:
    """贝叶斯检测的完整输出（含不确定性量化）。"""
    is_anomaly: bool
    confidence: float          # 0-1 涌现强度
    z_score: float
    deviation: float
    ci_95: tuple[float, float]  # 95% 可信区间
    posterior_mean: float       # 后验均值
    posterior_std: float        # 后验标准差
    description: str


class BayesianDetector:
    """贝叶斯变化检测器 — 带先验注入和不确定性量化。

    与普通 _shared.detectors 的区别：
      - 可以用先验知识初始化（而不只是从数据学习）
      - 输出后验分布（可信区间，不只是点估计）
      - 支持信念融合：合并多个检测器的结果
    """

    def __init__(
        self,
        prior_mean: float = 0.0,
        prior_std: float = 10.0,
        threshold: float = 3.0,
        window: int = 10,
    ) -> None:
        self.threshold = threshold
        self.window = max(3, window)
        self._buffer: list[float] = []
        self._prior_mean = prior_mean
        self._prior_std = prior_std

        # 信念对象（随证据更新）
        self._belief: Optional[_NormalBelief] = None
        if _HAS_BAYESIAN:
            self._belief = _NormalBelief(mu=prior_mean, sigma=prior_std)

    def update(self, value: float) -> BayesianSignal:
        """输入新值，返回贝叶斯检测信号。"""
        self._buffer.append(value)
        if len(self._buffer) > self.window:
            self._buffer.pop(0)

        if len(self._buffer) < 3:
            return BayesianSignal(
                is_anomaly=False, confidence=0.0, z_score=0.0, deviation=0.0,
                ci_95=(0, 0), posterior_mean=0, posterior_std=0,
                description="等待数据",
            )

        baseline = self._buffer[:-1]
        current = self._buffer[-1]

        # 更新信念
        if self._belief is not None:
            self._belief.update(observations=[current])

        mu = np_mean(baseline)
        sigma = np_std(baseline) or 1.0
        z = (current - mu) / sigma

        # 使用贝叶斯库（可用时）
        if _HAS_BAYESIAN and _CPD is not None:
            raw = _CPD.emergence_score(current, mu, sigma, len(baseline))
            sig = raw.get("signal", "none")
            is_anomaly = sig in ("strong", "moderate")
            confidence = raw.get("emergence_strength", 0.0)
            desc = sig
        else:
            is_anomaly = abs(z) >= self.threshold
            confidence = min(1.0, abs(z) / (self.threshold * 2))
            desc = f"{'异常' if is_anomaly else '正常'} (Z={z:.2f})"

        # 可信区间（从信念或 Z-score 推导）
        if self._belief is not None:
            lo, hi = self._belief.credible_interval(0.95)
            pm = self._belief.mean()
            ps = self._belief.sigma
        else:
            lo, hi = mu - 1.96 * sigma, mu + 1.96 * sigma
            pm = mu
            ps = sigma

        return BayesianSignal(
            is_anomaly=is_anomaly,
            confidence=round(confidence, 4),
            z_score=round(z, 4),
            deviation=round(current - mu, 4),
            ci_95=(round(lo, 4), round(hi, 4)),
            posterior_mean=round(pm, 4),
            posterior_std=round(ps, 4),
            description=desc,
        )

    def reset(self) -> None:
        """重置缓冲区和信念。"""
        self._buffer.clear()
        if _HAS_BAYESIAN:
            self._belief = _NormalBelief(mu=self._prior_mean, sigma=self._prior_std)

    def status(self) -> dict[str, Any]:
        """返回检测器当前状态。"""
        return {
            "method": "bayesian",
            "window": self.window,
            "buffer_size": len(self._buffer),
            "prior_mean": self._prior_mean,
            "prior_std": self._prior_std,
            "has_bayesian_lib": _HAS_BAYESIAN,
        }

    @staticmethod
    def fuse(signals: list[BayesianSignal]) -> BayesianSignal:
        """信念融合：合并多个检测器的结果。

        使用贝叶斯模型平均：按置信度加权平均。
        """
        if not signals:
            return BayesianSignal(
                is_anomaly=False, confidence=0.0, z_score=0.0, deviation=0.0,
                ci_95=(0, 0), posterior_mean=0, posterior_std=0,
                description="无信号可融合",
            )

        weights = [s.confidence for s in signals]
        total = sum(weights) or 1.0
        w_avg = sum(s.confidence * s.confidence for s in signals) / total

        return BayesianSignal(
            is_anomaly=any(s.is_anomaly for s in signals),
            confidence=round(w_avg, 4),
            z_score=round(sum(s.z_score * w / total for s, w in zip(signals, weights)), 4),
            deviation=round(sum(s.deviation * w / total for s, w in zip(signals, weights)), 4),
            ci_95=(round(min(s.ci_95[0] for s in signals), 4),
                   round(max(s.ci_95[1] for s in signals), 4)),
            posterior_mean=round(sum(s.posterior_mean * w / total for s, w in zip(signals, weights)), 4),
            posterior_std=round(sum(s.posterior_std * w / total for s, w in zip(signals, weights)), 4),
            description=f"fusion({len(signals)} signals)",
        )
