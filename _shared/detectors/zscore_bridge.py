"""
zscore_bridge — infrastructure 涌现检测的适配器包装

在 _shared.detectors 统一接口基础上，提供 infrastructure 专有的功能：
  - D₀-D₃ 维度追踪
  - 涌现实时监控
  - 理论模式匹配

Usage:
    from _shared.detectors.zscore_bridge import ZScoreMonitor

    monitor = ZScoreMonitor(threshold=3.0)
    for value in stream:
        signal = monitor.record("biomass", value)
        if signal.emergence_signals:
            print(f"⚠ 涌现: {signal.description}")
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from _shared.detectors import DetectionResult, np_mean, np_std

# ── 尝试导入 infrastructure ─────────────────────────

try:
    from infrastructure.unified_emergence import (
        EmergenceMonitor as _EM,
        EmergenceSignal as _ES,
        DimensionalLevel as _DL,
        EmergenceType as _ET,
    )
    _HAS_INFRA = True
except ImportError:
    _HAS_INFRA = False


@dataclass
class ZScoreSignal:
    """Z-score 实时监控信号。"""
    metric: str
    value: float
    z_score: float
    is_anomaly: bool
    confidence: float
    deviation: float
    baseline_stats: dict[str, float] = field(default_factory=dict)
    description: str = ""
    details: dict[str, Any] = field(default_factory=dict)


class ZScoreMonitor:
    """频率派 Z-score 实时监控器（包装 infrastructure.EmergenceMonitor）。

    设计为轻量替代：不需要 infrastructure 的完整 ML 栈也可运行。
    """

    def __init__(
        self,
        threshold: float = 3.0,
        min_sources: int = 3,
        window: int = 20,
    ) -> None:
        self.threshold = threshold
        self.min_sources = min_sources
        self.window = max(3, window)
        self._buffers: dict[str, list[float]] = {}
        self._infra_monitor: Any = None

        # infrastructure 可用时使用原生实现
        if _HAS_INFRA:
            try:
                self._infra_monitor = _EM(
                    emergence_threshold_sigma=threshold,
                    min_sources=min_sources,
                )
            except Exception:
                self._infra_monitor = None

    def record(
        self,
        metric: str,
        value: float,
        dimension: Optional[str] = None,
    ) -> ZScoreSignal:
        """记录一个新观测值，返回检测结果。"""
        if metric not in self._buffers:
            self._buffers[metric] = []
        buf = self._buffers[metric]
        buf.append(value)
        if len(buf) > self.window:
            buf.pop(0)

        # 使用 infrastructure 原生监控（如果可用）
        if self._infra_monitor is not None:
            try:
                from infrastructure.unified_emergence import DimensionalLevel
                dl = getattr(DimensionalLevel, dimension or "D1", DimensionalLevel.D1)
                self._infra_monitor.record(metric, value, dl)
                signals = self._infra_monitor.check_emergence()
                if signals:
                    s = signals[0]
                    return ZScoreSignal(
                        metric=metric, value=value,
                        z_score=s.deviation_sigma,
                        is_anomaly=s.confidence > 0.8,
                        confidence=s.confidence,
                        deviation=s.deviation_sigma,
                        description=s.description,
                        details={"emergence_type": str(s.emergence_type),
                                  "dimensional_level": str(s.dimensional_level)},
                    )
            except Exception:
                pass  # fallthrough to pure implementation

        # 纯 numpy 实现（无 infrastructure 依赖）
        if len(buf) < 3:
            return ZScoreSignal(
                metric=metric, value=value, z_score=0.0,
                is_anomaly=False, confidence=0.0, deviation=0.0,
                description="等待更多数据",
            )

        baseline = buf[:-1]
        mu = np_mean(baseline)
        sigma = np_std(baseline) or 1e-10
        z = (value - mu) / sigma
        is_anomaly = abs(z) >= self.threshold
        confidence = min(1.0, abs(z) / (self.threshold * 2))

        return ZScoreSignal(
            metric=metric, value=value,
            z_score=round(z, 4),
            is_anomaly=is_anomaly,
            confidence=round(confidence, 4),
            deviation=round(value - mu, 4),
            baseline_stats={"mean": round(mu, 4), "std": round(sigma, 4), "n": len(baseline)},
            description=f"{metric}: {value:.2f} (Z={z:.2f}, {'异常' if is_anomaly else '正常'})",
        )

    def health(self) -> dict[str, Any]:
        """返回监控器状态。"""
        return {
            "method": "zscore",
            "metrics": list(self._buffers.keys()),
            "threshold": self.threshold,
            "window": self.window,
            "using_infrastructure": self._infra_monitor is not None,
        }

    def reset(self, metric: Optional[str] = None) -> None:
        """重置指定指标（或全部）。"""
        if metric:
            self._buffers.pop(metric, None)
        else:
            self._buffers.clear()
        if self._infra_monitor is not None:
            try:
                self._infra_monitor.reset()
            except Exception:
                pass
