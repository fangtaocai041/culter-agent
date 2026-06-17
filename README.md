<p align="center">
  🇨🇳 <a href="README.zh.md">中文</a>
</p>

# 🐟 Culter Agent — 鲌类专研 (P₃)

> **Species**: *Culter* genus — *C. alburnus* (topmouth culter), *C. mongolicus* (Mongolian redfin), *C. oxycephalus*, *C. dabryi*, *C. oxycephaloides*, *C. recurviceps*
> **Domain**: Culter genomics · Trophic Ecology · Growth Analysis
> **Role**: P₃ — S-T-V-P₁-P₂ six-body architecture

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v1.0.1-8b5cf6)]()
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB)]()
[![Domain](https://img.shields.io/badge/Domain-Culter_Genomics-9cf)]()
[![Triangle](https://img.shields.io/badge/Triangle-Powered-EC4899)]()
[![DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/fangtaocai041/culter-agent)

---

## 🔺 S-T-V-P₁-P₂ Architecture Role: **P₃ (Culter Domain)**

> S-T-V-P₁-P₂ six-body architecture: `fish(S) → cognitive(V) → eon-core(Coord)`, derived: `porpoise(P₁)` + `coilia(P₂)` + `culter(P₃)` + `conflict-arbiter(C)`.
> **P₃** is the Culter domain expert — inherits knowledge from S, verification from V, coordination from Coord.

## 📊 Self-Assessment

| Dimension | Rating | Notes |
|-----------|:-----:|-------|
| 🐟 Domain Depth | ⭐⭐⭐⭐☆ | 6 *Culter* species with genomics/trophic profiles |
| 🔬 Analysis Scripts | ⭐⭐⭐⭐☆ | 2 core scripts: growth_analysis + trophic_analysis |
| 📡 Triangle Integration | ⭐⭐⭐⭐⭐ | Direct fish-ecology KB read via triangle bridge |
| 🧠 Cognitive Architecture | ⭐⭐⭐⭐☆ | ReAct loop + CulterOrchestrator v2.10 |
| 🧪 Test Coverage | ⭐⭐⭐☆☆ | Script-level tests, expanding |
| 🚀 Extensibility | ⭐⭐⭐⭐⭐ | Add new *Culter* species = new section in config |

---

## 📋 Version History

| Version | Date | Changes |
|---------|------|---------|
| **v1.0.1** | 2026-06-20 | README Restoration — full documentation from historical sessions |
| **v1.0.0** | 2026-06-17 | Initial release — 2 analysis scripts, 6 species, ReAct orchestrator |

> **Latest**: v1.0.1 · 2026-06-20

---

## 🧩 What This Is

**Culter Agent** is a specialized AI research agent for *Culter* genus fish — primarily the topmouth culter (*Culter alburnus*), an economically important freshwater fish in East Asian lakes and reservoirs. Built on the Triangle Core (V0 knowledge + V1 search + Coord orchestration), it provides:

- **Species profiles** for 6 *Culter* species
- **2 core analysis scripts**: growth parameter analysis (von Bertalanffy) and trophic niche analysis (stable isotopes/gut contents)
- **ReAct cognitive loop** with CulterOrchestrator v2.10 for iterative analysis
- **9-phase pipeline** configuration in agent.yaml v2.1.0
- **Triangle-powered**: direct read from fish-ecology-assistant knowledge base

---

## 🏛️ Philosophy

> 🌊 Everything flows. The river shapes the fish, and the fish shape the river.

**🌊 The River Flows** — *Culter* populations respond to hydrological changes, eutrophication, and fishing pressure. Their growth rates and trophic positions shift with environmental conditions. We track this dynamism.

**🍂 Knowledge Drifts** — Genomic tools reveal cryptic diversity within *Culter*. Today's species boundaries may shift with tomorrow's RAD-seq data.

**🌟 Emergence Patterns** — When growth analysis, stable isotopes, and gut content analysis converge on the same trophic shift, that's emergence.

---

## 🚀 Quick Start

```bash
git clone https://github.com/fangtaocai041/culter-agent.git
cd culter-agent
pip install -e .

# Run trophic analysis
python -m culter_agent run "trophic ecology"

# Growth analysis for specific species
python scripts/growth_analysis.py --species "Culter alburnus"
python scripts/trophic_analysis.py --species "Culter mongolicus"
```

---

## 🏗️ Architecture

```
S-T-V-P₁-P₂ Architecture (coordinated by eon-core):

  S/V0  fish-ecology-assistant    → Knowledge Supply
  V/V1  cognitive-search-engine   → Search Verification
  Coord  eon-core                  → Coordination Hub

  P₁    porpoise-agent            → Porpoise Expert
  P₂    coilia-agent              → Coilia Expert
  P₃    🐟 culter-agent           → Culter Expert ← this project
  C     conflict-arbiter          → Conflict Arbitration
```

### Internal Architecture

```
culter-agent/
  src/
  ├── main.py                   CLI entry point
  ├── adapter.py                IProjectAdapter — triangle bridge
  └── agent/
      ├── orchestrator.py       CulterOrchestrator v2.10 — task decomposition
      └── react_loop.py         Think→Act→Observe→Reflect cognitive loop
  scripts/
  ├── growth_analysis.py        von Bertalanffy growth parameters
  ├── trophic_analysis.py       Stable isotopes + gut content analysis
  └── shared_types.py           Canonical ecosystem types
  config/
  ├── agent.yaml                v2.1.0 — 9-phase pipeline + 6 target species
  └── tao.yaml                  TAO-inspired reasoning config
  tests/
  ├── test_growth.py             Growth analysis tests
  └── test_trophic.py            Trophic analysis tests
```

---

## ✨ Features

| Feature | Status | Description |
|---------|:------:|-------------|
| 🔬 Domain Analysis | ✅ | Species-specific *Culter* research pipeline |
| 📡 Triangle Powered | ✅ | V0 knowledge + V1 search + Coord orchestration |
| 🧠 Cognitive Loop | ✅ | ReAct pattern for iterative ecological analysis |
| 📈 Growth Analysis | ✅ | von Bertalanffy growth parameters + length-weight relationships |
| 🍽️ Trophic Analysis | ✅ | Stable isotopes (δ¹³C, δ¹⁵N) + gut content analysis |
| 🎛️ Orchestrator v2.10 | ✅ | CulterOrchestrator calling real Python scripts (not stubs) |
| ⚙️ 9-Phase Pipeline | ✅ | agent.yaml v2.1.0 with 6 target *Culter* species |
| 🔄 Cross-Project | ✅ | Triangle bridge for fish-ecology KB access |
| 🗂️ 6 Species | ✅ | *C. alburnus, C. mongolicus, C. oxycephalus, C. dabryi, C. oxycephaloides, C. recurviceps* |

---

## 📊 Analysis Scripts

| Script | Domain | Key Methods |
|--------|--------|-------------|
| `growth_analysis.py` | Growth Ecology | von Bertalanffy growth function, length-weight relationship (W = aLᵇ), growth performance index (φ') |
| `trophic_analysis.py` | Trophic Ecology | Stable isotope biplots (δ¹³C vs δ¹⁵N), SIBER niche metrics, gut content IRI% |

---

## 🔗 Ecosystem

This project is the **Culter Domain Expert (P₃)** in the SanShengWanWu ecosystem.

```
Triangle Core (sealed 3):
  📦 fish-ecology-assistant    → Knowledge Supply (V0)
  🔍 cognitive-search-engine   → Search Verification (V1)
  ⚙️ eon-core                  → Coordination Hub (Coord)

Derived Projects (open N):
  🐬 porpoise-agent    → P₁ Porpoise Expert
  🐟 coilia-agent      → P₂ Coilia Expert
  🐟 culter-agent      → P₃ Culter Expert ← this project
  🔥 conflict-arbiter  → C  Conflict Arbitration
```

> 🔥 Together infinite power, apart top expert engines.

---

## 🗺️ Roadmap

- [ ] Expand to all ~12 *Culter* species with complete YAML profiles
- [ ] Add population genetics pipeline (RAD-seq, microsatellite)
- [ ] Integrate otolith microchemistry for age validation
- [ ] Lake/reservoir ecosystem trophic modeling (Ecopath)

---

## 📋 README Changelog

| Version | Date | Theme | What Changed |
|:--------|:-----|:------|:-------------|
| **v8.0** | 2026-06-20 | README Restoration | Expanded from stub: full philosophy, architecture, features table, analysis scripts, self-assessment, README Changelog, DeepWiki badge |
| **v1.0.0** | 2026-06-17 | Initial | Stub README — basic project description |

---

## 📜 License

MIT © 2026 fangtaocai041

---

🌱 **Everything Flows · Panta Rhei**

> Heraclitus said: No man ever steps in the same river twice.
>
> We say: You cannot analyze today's ecological data with last month's code.

*Last updated: 2026-06-20　|　Environment: Reasonix Code · DeepSeek Powered*
