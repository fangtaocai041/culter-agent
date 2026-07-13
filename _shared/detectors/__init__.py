"""
detectors — 统一变化检测接口

提供 `detect_change()` 统一入口，自动选择底层检测引擎：
  - bayesian: 贝叶斯变点检测 (_bayesian.applications.ChangePointDetector)
  - zscore: 频率派 Z-score 涌现检测 (infrastructure.EmergenceMonitor)
  - auto: 自动选择（有 scipy 时用 bayesian，否则 zscore）

Usage:
    from _shared.detectors import detect_change, DetectionResult

    # 一键检测
    result = detect_change(
        values=[100, 110, 105, 95, 200, 210, 205],
        method="auto",
    )
    print(result.is_anomaly, result.confidence, result.method)

    # 在线实时检测
    from _shared.detectors import OnlineDetector
    det = OnlineDetector(method="bayesian")
    for v in stream:
        signal = det.update(v)
        if signal.is_anomaly:
            print(f"⚠ 检测到变化: {signal}")
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from _shared.types import CheckItem

MethodType = Literal["bayesian", "zscore", "auto"]


# ── 统一结果类型 ─────────────────────────────────────


@dataclass
class DetectionResult:
    """统一检测结果 — 无论底层用哪种算法，输出格式一致。"""
    is_anomaly: bool = False
    confidence: float = 0.0
    method: str = "unknown"
    z_score: Optional[float] = None
    deviation: Optional[float] = None
    description: str = ""
    details: dict[str, Any] = field(default_factory=dict)


# ── 自动选择 ─────────────────────────────────────────


def _has_scipy() -> bool:
    """检测 scipy 是否可用（bayesian 方法需要）。"""
    try:
        import scipy  # noqa: F401
        return True
    except ImportError:
        return False


def detect_change(
    values: list[float],
    method: MethodType = "auto",
    threshold: float = 3.0,
    **kwargs: Any,
) -> DetectionResult:
    """
    统一变化检测入口。

    参数:
        values: 时间序列数据点列表（至少需 2 个点）
        method: bayesian / zscore / auto（默认 auto）
        threshold: 异常阈值（σ 倍数）
        **kwargs: 透传给底层检测器的额外参数

    返回:
        DetectionResult 统一格式
    """
    if len(values) < 2:
        return DetectionResult(
            is_anomaly=False,
            confidence=0.0,
            method=method,
            description="数据点不足（需 ≥2）",
        )

    # 自动选择
    resolved: MethodType
    if method == "auto":
        resolved = "bayesian" if _has_scipy() else "zscore"
    else:
        resolved = method

    if resolved == "bayesian":
        return _detect_bayesian(values, threshold=threshold, **kwargs)
    else:
        return _detect_zscore(values, threshold=threshold, **kwargs)


# ── 底层实现 ─────────────────────────────────────────


def _detect_bayesian(values: list[float], threshold: float = 3.0, **kwargs: Any) -> DetectionResult:
    """使用贝叶斯变点检测。"""
    try:
        from _bayesian.applications.change_point_detector import ChangePointDetector
    except ImportError:
        return DetectionResult(method="bayesian", description="_bayesian 不可用，请检查导入路径")

    # 分离基线和新观测
    baseline = values[:-1]
    current = values[-1]

    if len(baseline) < 2:
        return DetectionResult(method="bayesian", description="基线数据不足")

    mu = float(np_mean(baseline))
    sigma = float(np_std(baseline)) or 1.0

    result = ChangePointDetector.emergence_score(
        current_value=current,
        baseline_mean=mu,
        baseline_std=sigma,
        n_baseline=len(baseline),
    )

    is_anomaly = result.get("signal") in ("strong", "moderate")
    return DetectionResult(
        is_anomaly=is_anomaly,
        confidence=result.get("emergence_strength", 0.0),
        method="bayesian",
        z_score=result.get("z_score"),
        deviation=current - mu,
        description=result.get("signal", "none"),
        details={
            "baseline_mean": round(mu, 4),
            "baseline_std": round(sigma, 4),
            "current_value": current,
            "p_value": result.get("p_value"),
            "raw": result,
        },
    )


def _detect_zscore(values: list[float], threshold: float = 3.0, **kwargs: Any) -> DetectionResult:
    """使用频率派 Z-score 检测。"""
    # 纯 numpy 实现，无需 infrastructure 导入
    import numpy as np

    arr = np.array(values, dtype=float)
    if len(arr) < 3:
        return DetectionResult(method="zscore", description="数据点不足")

    # 最近值与前面窗口的比较
    window = values[:-1]
    current = values[-1]

    mu = float(np.mean(window))
    sigma = float(np.std(window, ddof=1)) or 1e-10
    z = (current - mu) / sigma

    is_anomaly = abs(z) >= threshold
    # Z-score → 置信度映射
    confidence = min(1.0, max(0.0, abs(z) / (threshold * 2)))

    return DetectionResult(
        is_anomaly=is_anomaly,
        confidence=round(confidence, 4),
        method="zscore",
        z_score=round(z, 4),
        deviation=round(current - mu, 4),
        description=f"{'异常' if is_anomaly else '正常'} (Z={z:.2f})",
        details={
            "baseline_mean": round(mu, 4),
            "baseline_std": round(sigma, 4),
            "current_value": current,
        },
    )


# ── 在线检测器 (状态保持) ────────────────────────────


class OnlineDetector:
    """在线流式变化检测器 — 保持窗口状态，逐点更新。

    Usage:
        det = OnlineDetector(method="bayesian", window=10)
        for value in data_stream:
            result = det.update(value)
            if result.is_anomaly:
                handle_anomaly(result)
    """

    def __init__(
        self,
        method: MethodType = "auto",
        window: int = 10,
        threshold: float = 3.0,
    ) -> None:
        self.method: MethodType = "auto" if method == "auto" else method
        self.window = max(3, window)
        self.threshold = threshold
        self._buffer: list[float] = []

    def update(self, value: float) -> DetectionResult:
        """输入一个新值，返回检测结果。"""
        self._buffer.append(value)
        if len(self._buffer) > self.window:
            self._buffer.pop(0)
        return detect_change(self._buffer, method=self.method, threshold=self.threshold)

    def reset(self) -> None:
        """清空缓冲区。"""
        self._buffer.clear()


# ── 辅助 ────────────────────────────────────────────


def np_mean(arr: list[float]) -> float:
    """纯 Python 均值（避免 numpy 依赖）。"""
    return sum(arr) / len(arr)


def np_std(arr: list[float]) -> float:
    """纯 Python 样本标准差。"""
    if len(arr) < 2:
        return 0.0
    mu = np_mean(arr)
    variance = sum((x - mu) ** 2 for x in arr) / (len(arr) - 1)
    return variance ** 0.5
