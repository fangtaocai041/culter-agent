<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║   🐟  CULTER AGENT  ·  P₃ 鲌类专研  ·  v1.5.0                ║
║  ─────────────────────────────────────────────────────────  ║
║    鲌类生长 · 营养生态 · 栖息地建模 · 贝叶斯趋势分析              ║
║        6 种鲌属 · 长江流域 · BaseAdapter 继承                    ║
╚══════════════════════════════════════════════════════════════╝
```

<p align="center">
  🇬🇧 <a href="README.md">English</a>
</p>

![Python 3.13+](https://img.shields.io/badge/Python%203.13%2B-3776AB?style=flat-square)
![v1.5.0](https://img.shields.io/badge/v1.5.0-8A4FCE?style=flat-square)
![6 species](https://img.shields.io/badge/6%20%E9%B3%8C%E5%B1%9E-007EC6?style=flat-square)
![Bayesian](https://img.shields.io/badge/%E8%B4%9D%E5%8F%B6%E6%96%AF-EC4899?style=flat-square)
![BaseAdapter](https://img.shields.io/badge/BaseAdapter-22c55e?style=flat-square)
![seed=42](https://img.shields.io/badge/%E5%8F%AF%E9%87%8D%E5%A4%8D%20seed%3D42-8b5cf6?style=flat-square)

<p align="center">
  <a href="https://github.com/fangtaocai041/culter-agent/stargazers"><img src="https://img.shields.io/github/stars/fangtaocai041/culter-agent?style=social" alt="Stars"></a>
  <a href="https://github.com/fangtaocai041/culter-agent/network/members"><img src="https://img.shields.io/github/forks/fangtaocai041/culter-agent?style=social" alt="Forks"></a>
</p>

<div align="center"><h3>🌊 万物皆流 · Panta Rhei</h3></div>

</div>

---

## 📑 目录

- [🧬 这是什么](#-这是什么)
- [🚀 快速开始](#-快速开始)
- [🧠 贝叶斯能力](#-贝叶斯能力)
- [📡 API](#-api)
- [✅ 验证](#-验证)

---

## 🧬 这是什么

**Culter Agent** 是长江鲌类（Culter spp.）专研智能体，继承 `fangtao_fishlab` 的 `BaseAdapter`，自动获得贝叶斯模板方法。

| 能力 | 说明 |
|:-----|:------|
| 🐟 生长模型 | von Bertalanffy 生长方程 · 年龄鉴定 |
| 🌿 营养生态 | 稳定同位素 · 食性分析 |
| 🏞️ 栖息地建模 | 栖息地适宜性 · 空间分布 |
| 🧬 基因组学 | 群体遗传学 · 系统发育 |
| 🧠 贝叶斯分析 | 趋势分析 · 两群比较 · 样本量规划 |

---

## 🚀 快速开始

```bash
pip install -e .
```

```python
from fangtao_fishlab import get_adapter
agent = get_adapter("culter-agent")

# 健康检查（含贝叶斯置信度）
agent.health()

# 种群趋势分析（自动 seed=42 可重复）
agent.bayesian_trend_analysis([
    (2015, 50, 120), (2016, 48, 120), (2017, 52, 120),
    (2018, 55, 120), (2019, 58, 120), (2020, 60, 120),
])

# 两群比较（如湖泊 vs 河流）
agent.bayesian_ab_compare("湖泊", 65, 100, "河流", 42, 100)
```

---

## 🧠 贝叶斯能力

通过继承 `BaseAdapter` 自动获得（由 `fangtao_fishlab._bayesian` 驱动）：

| 方法 | 说明 | 底层引擎 |
|:-----|:------|:---------|
| `bayesian_trend_analysis(data)` | 种群趋势分析 | TrendModel |
| `bayesian_ab_compare(...)` | 两群比较 | ABTest |
| `bayesian_sample_size_plan(e)` | 样本量规划 | ABTest.plan |
| `health()` | 含 `bayesian_confidence` | BaseAdapter hook |

> 🎯 所有方法默认 `seed=42`，相同输入永远相同输出。

---

## 📡 API

| 方法 | 说明 |
|:-----|:------|
| `search(query)` | 物种文献搜索 |
| `health()` | 系统健康检查（含贝叶斯置信度） |
| `bayesian_trend_analysis(data)` | 贝叶斯种群趋势 |
| `bayesian_ab_compare(n,s,t,n,s,t)` | 贝叶斯两群比较 |
| `bayesian_sample_size_plan(e)` | 样本量规划 |
| `bayesian_habitat_compare(lake, river)` | 栖息地对比 |

---

## ✅ 验证

```bash
python -m pytest tests/ -v
```

---

## 📜 版本历史

| 版本 | 日期 | 亮点 |
|:-----|:-----|:------|
| **v1.5.0** | 2026-07-20 | 继承 BaseAdapter · 3 贝叶斯模板方法 · 可重复 seed=42 |
| v1.4.0 | 2026-06 | 鲌类专研智能体 |

---

## 📄 许可证

MIT (c) 2026 fangtaocai041

---

<div align="center">
<p><em>「道生一，一生二，二生三，三生万物。」</em><br>
<em>——《道德经》第四十二章</em></p>
<br>
<p><strong>🌊 万物皆流 · Panta Rhei</strong></p>
</div>
