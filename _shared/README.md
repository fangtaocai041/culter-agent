# _shared — 共享基础设施

类型系统 · 适配器协议 · 统一检测器 · 管线调度

---

## 定位

`_shared` 是 **fangtao_fishlab 体系的共享工具箱**，被所有三角核心和衍生智能体 import。

**包含 4 层能力**：

| 层 | 模块 | 依赖 |
|:--|:-----|:----:|
| 类型系统 | `types.py` | pydantic |
| 适配器协议 | `adapter_protocol.py` + `base_adapter.py` | 无 |
| 检测器 | `detectors/` | numpy (scipy 可选) |
| 管线调度 | `pipeline.py` | 无 |

---

## 类型系统 (`types.py`)

标准化的 Pydantic 模型，替代裸 dict：

```python
from _shared.types import AdapterState, SearchResult, CheckReport

# 适配器健康状态
state = AdapterState(
    status="HEALTHY",
    core_loaded=True,
    bayesian="READY",
    bayesian_confidence=0.85,
)

# 搜索结果标准格式
result = SearchResult(
    query="江豚", status="ok", papers_found=12, mode="fast"
)
```

---

## 适配器协议 (`adapter_protocol.py`)

所有项目统一实现的接口：

```python
from _shared.adapter_protocol import IProjectAdapter

class MyAdapter(IProjectAdapter):
    project_name = "my-project"

    def search(self, query, **kwargs):
        return {"status": "ok", "results": [...]}

    def health(self):
        return {"status": "HEALTHY", "core_loaded": True}

    def info(self):
        return {"project": "my-project", "version": "1.0"}
```

`BaseAdapter` 类自动提供 `self_check()`、`fast_search()`、`deep_analyze()`、`bayesian_health()` 方法。

---

## 统一检测器 (`detectors/`)

`_shared/detectors` 是 **emergence 检测的单一入口**，底层自动选择 Bayesian 或 Z-score：

```python
from _shared.detectors import detect_change, OnlineDetector
from _shared.detectors.bayesian_bridge import BayesianDetector
from _shared.detectors.zscore_bridge import ZScoreMonitor

# 一键检测（自动选算法）
result = detect_change([100, 105, 102, 98, 200, 210, 205])
# result.is_anomaly=True, result.confidence=0.80, result.method="bayesian"

# 流式在线监控
det = OnlineDetector(method="auto", window=10)
for value in stream:
    signal = det.update(value)
    if signal.is_anomaly:
        print(f"⚠ 异常: {signal.description}")

# 贝叶斯专有（带先验 + 可信区间）
bd = BayesianDetector(prior_mean=1249, prior_std=200)
for v in population_data:
    s = bd.update(v)
    print(s.ci_95)  # 95% 可信区间
```

---

## 管线调度 (`pipeline.py`)

预置的标准搜索管线：

```python
from _shared.pipeline import STANDARD_PIPELINE, DOMAIN_PIPELINES

# 标准管线：知识库 → 搜索验证
result = STANDARD_PIPELINE.run("鳤")

# 物种专研管线：知识库 → 搜索 → 智能体分析
result = DOMAIN_PIPELINES["porpoise"].run("江豚")
```

---

## 依赖

- **强制**：pydantic（类型系统）
- **可选**：numpy + scipy（检测器，不装则降级为纯 Python 实现）
- **零依赖**：adapter_protocol、pipeline、errors、path_init

---

## 测试

```bash
cd D:\Reasonix\fangtao_fishlab
python -c "from _shared.detectors import detect_change; print(detect_change([1,2,1,2,10]).is_anomaly)"
# → True（10 是异常值）
```
