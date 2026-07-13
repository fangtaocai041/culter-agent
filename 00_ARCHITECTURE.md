# 🏗️ fangtao_fishlab 架构索引

> 方陶鱼类生态 — 多 Agent 协作系统 + 知识工程平台

---

## 层级总览

```
fangtao_fishlab/              ← 主入口 (__init__.py)
│
├── ◉ TIER 0: 三角核心 ────── 始终就绪
├── ◉ TIER 1: 共享服务 ────── import 即用
├── ◉ TIER 2: 衍生智能体 ──── 按物种激活
├── ◉ TIER 3: 工具/配置 ──── 辅助
```

---

## ◉ TIER 0: 三角核心（Triangle Core）

> 这三个项目构成系统的**骨架**，`import fangtao_fishlab` 时自动就绪。

| # | 项目 | 角色 | 职责 | 启动时机 |
|:-|:-----|:----:|------|---------|
| 00 | `_bayesian` | **数学引擎** | 信念量化：BetaBelief/NormalBelief + 6 应用模块 | import 时 |
| 01 | `fish-ecology-assistant` | **S/V0 知识供给** | 430 种长江鱼类 SQLite 知识库 + 21 MCP + 28 技能 | get_adapter() 首次 |
| 02 | `cognitive-search-engine` | **V/V1 搜索验证** | 7+ 搜索引擎 + BDI+ReAct 认知循环 + MemorySystem | get_adapter() 首次 |
| 03 | `eon-core` | **Coord 协调中枢** | EventBus / DAG / CAS / 管线编排 / RCCA 核心 | get_adapter() 首次 |

---

## ◉ TIER 1: 共享服务（Shared Services）

> 被所有其他项目 import 的能力层，**零或轻量依赖**。

| # | 项目 | 定位 | 关键能力 | 依赖 |
|:-|:-----|:----:|---------|:----:|
| 04 | `_shared` | **类型 + 协议 + 检测器** | Pydantic 模型、IProjectAdapter、Pipeline、detect_change() | 无 |
| 05 | `infrastructure` | **感知 + ML** | 涌现检测、鱼类分类、中文 NLP、YOLO 检测 | torch (可选) |

---

## ◉ TIER 2: 衍生智能体（Derived Agents）

> 按物种激活，收到用户问题才加载。共享三角核心的基础能力。

| # | 项目 | 角色 | 物种 | 核心分析能力 |
|:-|:-----|:----:|:----:|-------------|
| 06 | `porpoise-agent` | **P₁** | 🐬 江豚 | NBHF 声学、栖息地建模、种群生存力 |
| 07 | `coilia-agent` | **P₂** | 🐟 刀鲚 | 耳石微化学、洄游路线重建、资源评估 |
| 08 | `culter-agent` | **P₃** | 🐟 鲌类（6种） | 基因组学、稳定同位素、von Bertalanffy 生长 |
| 09 | `conflict-arbiter` | **C** | 多源 | 4 级冲突检测、加权投票、熔断器 |

---

## ◉ TIER 3: 工具/配置（Tools & Config）

| # | 目录 | 用途 |
|:-|:-----|------|
| 10 | `scripts/` | 健康检查、测试、迁移脚本 |
| 11 | `config/` | YAML 配置文件（agent、bayesian priors） |
| 12 | `logs/` | 运行日志 |
| 13 | `data/` | 数据持久化（若不存在则由各项目自行创建） |

---

## 🔄 调用流程

```
用户提问："江豚种群现状"
    │
    ▼
[01] fish-ecology-assistant    查本地知识库 → 江豚已知数据
    │
    ▼
[02] cognitive-search-engine   并行搜索 PubMed/CNKI/Crossref...
    │   └── [00] _bayesian     搜索可信度评分
    │   └── [03] eon-core      协调管线（可选）
    │
    ▼
[06] porpoise-agent            江豚专属分析（按物种路由）
    │   └── [04] _shared       类型 + 检测器
    │   └── [05] infrastructure 涌现监控（可选）
    │
    ▼
[09] conflict-arbiter          多源数据冲突仲裁（如需）
```

---

## 📦 import 速查

```python
# TIER 0 — 三角核心
from _bayesian import BetaBelief, NormalBelief          # 信念量化
from _bayesian.applications import SearchCredibility    # 搜索可信度
from _bayesian.applications import ChangePointDetector  # 变点检测
from _shared.detectors import detect_change             # 统一检测接口

# TIER 1 — 共享服务
from _shared.types import AdapterState, CheckReport      # 标准类型
from _shared.detectors.bayesian_bridge import BayesianDetector  # 贝叶斯检测器

# TIER 2 — 智能体（通过 fangtao_fishlab.get_adapter）
from fangtao_fishlab import get_adapter
porpoise = get_adapter("porpoise-agent")
coilia = get_adapter("coilia-agent")
culter = get_adapter("culter-agent")
arbiter = get_adapter("conflict-arbiter")
```

---

## 📜 设计原则

1. **Tier 0 无环依赖** — 三角核心不依赖 Tier 1/2
2. **Tier 1 纯能力** — 不依赖 Tier 2
3. **Tier 2 按需加载** — 用 `get_adapter()` 延迟初始化，不占内存
4. **序号即层级** — 00-03 核心、04-05 共享、06-09 智能体、10+ 工具
