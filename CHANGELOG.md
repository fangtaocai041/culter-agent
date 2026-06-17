# Changelog — culter-agent

> 版本变更记录。参见 ROADMAP.md 了解技术改进路线图。

## v2.1.0 — 2026-06-27

### 📈 真实分析脚本 + Orchestrator 集成

- 📈 **growth_analysis.py**: 生长参数分析 (von Bertalanffy 生长方程 / 体重-体长关系 / 生长速率)
- 🍽️ **trophic_analysis.py**: 营养生态位分析 (稳定同位素 δ¹³C/δ¹⁵N / 胃含物 / 营养级)
- 🎛️ **Orchestrator 调用真实脚本**: CulterOrchestrator 从 stub 升级为调用真实 Python 分析脚本
- ⚙️ **agent.yaml v2.1.0**: 9 阶段管线配置更新 + 6 目标物种参数

---

## v2.0.0 — 2026-06-08
- 初始发布 — 8 Skills · 9 阶段管线 · 6 目标物种
