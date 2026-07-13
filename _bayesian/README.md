# _bayesian — 贝叶斯信念工程化核心

信念有强弱，且随证据改变。

---

## 定位

`_bayesian` 是 **fangtao_fishlab 体系的数学引擎**，将贝叶斯推理从数学公式转化为工程化 Python 对象。它是三角核心和所有衍生智能体的**共享信念管理基础设施**。

**关键特征**：
- ✅ **全共轭** — 无需 MCMC，解析解
- ✅ **自检** — 每个信念对象可自我验证
- ✅ **轻量** — 仅依赖 numpy + scipy（~50MB）
- ✅ **即插即用** — `from _bayesian import BetaBelief`

---

## 核心 API

```python
from _bayesian import BetaBelief, NormalBelief, DirichletBelief
from _bayesian.applications import (
    SearchCredibility,       # 搜索验证层
    KnowledgeUpdater,        # 知识供给层
    ConflictResolver,        # 冲突仲裁
    ChangePointDetector,     # 变点检测
    AgentBelief,             # 智能体信念
    MetaBayesian,            # 元认知
)
```

### BetaBelief — 二元结果信念

```python
# 先验：对搜索结果持谨慎态度
belief = BetaBelief(alpha=2, beta=2)

# 证据：6 次检索 5 次成功
belief.update(successes=5, trials=6)

print(belief.mean())                    # 后验均值: 0.583
print(belief.credible_interval(0.95))   # 95% 可信区间: (0.29, 0.84)
print(belief.weight())                  # 证据权重: 9
report = belief.self_check()            # 自检
```

### NormalBelief — 连续量信念

```python
# 先验：江豚种群 1249±200
population = NormalBelief(mu=1249, sigma=200)

# 新证据：2026 年调查 1426 头
population.update(observations=[1426])

print(f"最新估算: {population.mean():.0f} ± {population.sigma:.0f}")
# → "最新估算: 1376 ± 112"（不确定性缩小）
```

### DirichletBelief — 多类别信念

```python
# 三个来源的可信度
sources = DirichletBelief(alphas=[1, 1, 1])
sources.update(observations=[0, 1, 0, 1, 0, 2, 0])  # 0=PubMed, 1=CNKI, 2=Google
print(sources.mean())  # [0.5, 0.3, 0.2] ← 各源后验可信度
```

---

## 应用模块

| 模块 | 类/函数 | 输入 | 输出 |
|------|---------|------|------|
| `SearchCredibility` | `engine_reliability("pubmed")` | 引擎名 | `BetaBelief` 可信度 |
| `KnowledgeUpdater` | `validate_with_bayes(claim, ...)` | 声明 + 正反证据 | 裁决 + 置信度 |
| `ConflictResolver` | `arbitrate(claim, sources)` | 多源声明 | 加权估计 + 冲突等级 |
| `ChangePointDetector` | `emergence_score(current, baseline)` | 当前值 + 基线 | 涌现信号 |
| `AgentBelief` | `SpeciesStatusBelief(pop, trend, threat)` | 3 维状态 | 复合信念 |
| `MetaBayesian` | `calibrate_prior(history)` | 历史表现 | 校准后的先验 |

---

## 运行自检

```bash
cd D:\Reasonix\fangtao_fishlab
python -m _bayesian.run_self_check
```

应输出所有模块通过。

---

## 设计原则

1. **全共轭** — Beta-Binomial、Normal-Normal、Dirichlet-Categorical，解析解无 MCMC
2. **自检** — `self_check()` 验证后验更新、可信区间、信息量、稳定性、校准度
3. **无状态副作用** — 信念对象是纯数据，可序列化、可合并
4. **零基础设施依赖** — 不依赖任何其他 fangtao_fishlab 项目
