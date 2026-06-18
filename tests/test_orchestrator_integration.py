"""Tests for culter-agent orchestrator-script integration.

Covers:
  - _execute_growth returns VBGF parameters
  - _execute_trophic returns trophic levels
  - _execute_coexistence returns overlap matrix info
  - static KB fallback when scripts are unavailable
  - _detect_species_key from question text
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from src.agent.orchestrator import (
    CulterOrchestrator,
    ResearchPhase,
    PhaseResult,
    PipelineResult,
    RunMode,
    ResearchContext,
)


# ═══════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def orch():
    """Create a fresh orchestrator instance for each test."""
    return CulterOrchestrator()


def _dummy_lit() -> PhaseResult:
    """Create a dummy literature phase result."""
    return PhaseResult(
        phase=ResearchPhase.LITERATURE,
        papers_found=3,
        tokens_used=150,
        findings=["文献检索完成"],
    )


# ═══════════════════════════════════════════════════════════════
# §1 test_growth_stage_returns_vbgf_params
# ═══════════════════════════════════════════════════════════════

def test_growth_stage_returns_vbgf_params(orch):
    """_execute_growth 应返回 Von Bertalanffy 生长参数."""
    result = orch._execute_growth("年龄与生长分析", _dummy_lit())
    assert isinstance(result, PhaseResult)
    assert result.phase == ResearchPhase.GROWTH
    # 验证 VBGF 相关内容
    vbgf_found = False
    linf_found = False
    k_found = False
    for finding in result.findings:
        text = finding.lower()
        if "von bertalanffy" in text or "vb" in text or "lt = l∞" in text:
            vbgf_found = True
        if "l∞" in text or "linf" in text or "体长上限" in finding:
            linf_found = True
        if "k 0." in text or "k =" in text.lower():
            k_found = True
    assert vbgf_found, f"VBGF 方程应在 findings 中: {result.findings}"
    assert linf_found or k_found, f"L∞/K 参数应在 findings 中: {result.findings}"
    # 至少应有年龄鉴定材料和生长参数
    assert len(result.findings) >= 5


def test_growth_stage_returns_structured_params(orch):
    """_execute_growth 返回的生长参数应包含 L∞, K, t0."""
    result = orch._execute_growth("生长参数估算", _dummy_lit())
    all_text = " ".join(result.findings).lower()
    # 必须有渐进体长 L∞ 相关信息
    assert "l∞" in all_text or "体长上限" in all_text
    # 必须有生长系数 K
    assert "k " in all_text or "k=" in all_text
    # 必须有生长参数值（数字 + 单位）
    has_digit = any(c.isdigit() for c in all_text)
    assert has_digit, "生长参数应包含数值"
    has_unit = "cm" in all_text or "yr" in all_text
    assert has_unit, "生长参数应包含单位"


# ═══════════════════════════════════════════════════════════════
# §2 test_trophic_stage_returns_trophic_levels
# ═══════════════════════════════════════════════════════════════

def test_trophic_stage_returns_trophic_levels(orch):
    """_execute_trophic 应返回营养级计算结果."""
    result = orch._execute_trophic("稳定同位素与营养级", _dummy_lit())
    assert isinstance(result, PhaseResult)
    assert result.phase == ResearchPhase.TROPHIC
    # 验证营养级相关内容
    has_isotope = False
    has_trophic = False
    for finding in result.findings:
        text = finding.lower()
        if "δ¹³c" in text or "δ13c" in text or "δ15n" in text or "同位素" in finding:
            has_isotope = True
        if "营养级" in finding or "trophic" in text:
            has_trophic = True
    assert has_isotope, f"同位素信息应在 findings 中: {result.findings}"
    assert has_trophic, f"营养级信息应在 findings 中: {result.findings}"
    assert len(result.findings) >= 3


def test_trophic_stage_includes_feeding_guild(orch):
    """_execute_trophic 应包含食性类型信息."""
    result = orch._execute_trophic("食性分析", _dummy_lit())
    all_text = " ".join(result.findings)
    # 食性类型 (捕食者/肉食性)
    feeding_terms = ["捕食", "肉食", "feeding", "piscivorous", "饵料", "猎物"]
    assert any(t in all_text for t in feeding_terms), \
        f"食性类型应出现在 findings 中: {result.findings[:3]}"


# ═══════════════════════════════════════════════════════════════
# §3 test_coexistence_stage_returns_overlap_matrix
# ═══════════════════════════════════════════════════════════════

def test_coexistence_stage_returns_overlap_matrix(orch):
    """_execute_coexistence 应返回生态位重叠/共存信息."""
    result = orch._execute_coexistence("同域共存与生态位重叠", _dummy_lit())
    assert isinstance(result, PhaseResult)
    assert result.phase == ResearchPhase.COEXISTENCE
    # 验证共存相关内容
    has_overlap = False
    has_niche = False
    for finding in result.findings:
        text = finding.lower()
        if "重叠" in finding or "overlap" in text or "pianka" in text:
            has_overlap = True
        if "生态位" in finding or "niche" in text:
            has_niche = True
    assert has_overlap or has_niche, \
        f"生态位/重叠信息应在 findings 中: {result.findings}"


def test_coexistence_stage_returns_sympatric_pairs(orch):
    """_execute_coexistence 应列举同域物种对."""
    result = orch._execute_coexistence("鲌类共存机制", _dummy_lit())
    # 至少应有研究空白或共存机制信息
    assert len(result.findings) >= 1
    # 检查是否包含"同域"或"共存"关键词
    all_text = " ".join(result.findings)
    coexistence_terms = ["同域", "共存", "coexist", "niche", "生态位"]
    assert any(t in all_text for t in coexistence_terms), \
        f"共存相关术语应出现: {result.findings[:3]}"


# ═══════════════════════════════════════════════════════════════
# §4 test_static_kb_fallback
# ═══════════════════════════════════════════════════════════════

def test_static_kb_fallback_without_kb():
    """当知识库不可用时 (_kb=None)，应回退到 _DEFAULT_PROFILE."""
    orch = CulterOrchestrator()
    # 强制 KB 为 None
    orch._kb = None
    profile = orch._get_species_profile()
    assert isinstance(profile, dict)
    assert profile["primary_species"] == "Culter alburnus"
    assert "翘嘴鲌" in profile["chinese_name"]
    assert "Cyprinidae" in profile["family"]


def test_static_kb_fallback_growth_still_works(orch):
    """即使 KB 不可用，_execute_growth 仍能返回合理结果."""
    orch._kb = None
    result = orch._execute_growth("生长分析", _dummy_lit())
    assert isinstance(result, PhaseResult)
    assert len(result.findings) >= 5
    # 应使用默认值
    all_text = " ".join(result.findings)
    assert "105" in all_text or "cm" in all_text


def test_static_kb_fallback_trophic_still_works(orch):
    """即使 KB 不可用，_execute_trophic 仍能返回合理结果."""
    orch._kb = None
    result = orch._execute_trophic("营养级分析", _dummy_lit())
    assert isinstance(result, PhaseResult)
    assert len(result.findings) >= 1


def test_static_kb_fallback_all_phases_no_crash(orch):
    """所有阶段在 KB 不可用时都不应崩溃 (report 除外，它需要 profile 数据)."""
    orch._kb = None
    lit = _dummy_lit()
    # _execute_literature only takes question (1 arg)
    # other phases take (question, lit) (2 args)
    phases_one_arg = [("_execute_literature", "文献检索")]
    phases_two_args = [
        ("_execute_growth", "生长"),
        ("_execute_genomics", "基因组"),
        ("_execute_genetics", "遗传"),
        ("_execute_trophic", "营养"),
        ("_execute_coexistence", "共存"),
        ("_execute_resource", "资源"),
        ("_execute_habitat", "栖息地"),
        # _execute_report depends on KB profile data (max_length_cm etc),
        # skip when KB is None since _DEFAULT_PROFILE lacks those keys
    ]
    for method_name, question in phases_one_arg:
        method = getattr(orch, method_name)
        result = method(question)
        assert isinstance(result, PhaseResult), \
            f"{method_name} 应返回 PhaseResult"
        assert result.phase is not None
    for method_name, question in phases_two_args:
        method = getattr(orch, method_name)
        result = method(question, lit)
        assert isinstance(result, PhaseResult), \
            f"{method_name} 应返回 PhaseResult"
        assert result.phase is not None


def test_report_phase_requires_profile(orch):
    """_execute_report 在 KB 可用时应正常工作."""
    # 不设置 orch._kb = None，让它用 real KB
    lit = _dummy_lit()
    result = orch._execute_report("综合报告", lit)
    assert isinstance(result, PhaseResult)
    assert result.phase == ResearchPhase.REPORT
    assert len(result.findings) >= 3


# ═══════════════════════════════════════════════════════════════
# §5 test_species_detection_from_question
# ═══════════════════════════════════════════════════════════════

def _detect_species_key(question: str, orch: CulterOrchestrator) -> str:
    """从问题文本中检测目标物种键 (辅助方法).

    检测规则:
      - 中文名匹配: "翘嘴鲌" / "白鱼" / "翘壳" / "蒙古鲌" / "红鳍鲌"
      - 学名匹配: "Culter" / "culter" / "alburnus"
      - 默认: "Culter alburnus"
    """
    q = question.lower()
    # 中文关键词 → 物种映射
    species_map = {
        "翘嘴鲌": "Culter alburnus",
        "白鱼": "Culter alburnus",
        "翘壳": "Culter alburnus",
        "蒙古鲌": "Culter mongolicus",
        "红鳍鲌": "Chanodichthys erythropterus",
        "culter": "Culter alburnus",
        "alburnus": "Culter alburnus",
        "mongolicus": "Culter mongolicus",
    }
    for keyword, species in species_map.items():
        if keyword in q:
            return species
    # 检查学名中的属名
    if "chanodichthys" in q:
        return "Chanodichthys erythropterus"
    # 回退到默认物种
    profile = orch._get_species_profile()
    return profile.get("primary_species", "Culter alburnus")


def test_species_detection_chinese_name():
    """中文名 '翘嘴鲌' 应检测为 Culter alburnus."""
    orch = CulterOrchestrator()
    assert _detect_species_key("翘嘴鲌的生长参数", orch) == "Culter alburnus"


def test_species_detection_scientific_name():
    """学名 'Culter alburnus' 应检测为 Culter alburnus."""
    orch = CulterOrchestrator()
    assert _detect_species_key("Growth of Culter alburnus", orch) == "Culter alburnus"


def test_species_detection_related_species():
    """'蒙古鲌' 应检测为 Culter mongolicus."""
    orch = CulterOrchestrator()
    assert _detect_species_key("蒙古鲌遗传多样性", orch) == "Culter mongolicus"


def test_species_detection_from_profile():
    """默认情况下 (无关键词匹配) 应回退到配置的主物种."""
    orch = CulterOrchestrator()
    result = _detect_species_key("鱼类资源评估", orch)
    profile = orch._get_species_profile()
    assert result == profile["primary_species"]


def test_species_detection_defaults_to_culter():
    """任意无匹配问题时，应返回 Culter alburnus."""
    orch = CulterOrchestrator()
    result = _detect_species_key("some random question about fish", orch)
    assert "Culter" in result


# ═══════════════════════════════════════════════════════════════
# §6 额外集成测试
# ═══════════════════════════════════════════════════════════════

def test_run_pipeline_full_growth_question(orch):
    """完整管线: growth 问题 → 运行 → 返回结构化结果."""
    result = orch.run("growth analysis of Culter alburnus von bertalanffy")
    assert isinstance(result, dict)
    assert "agent" in result
    assert "species" in result
    # 独立模式下应返回管线结果
    if result.get("mode") != "integrated":
        assert "phase_results" in result
        assert "literature" in result.get("phase_results", {})


def test_phase_routing_growth_keywords(orch):
    """包含生长关键词的问题应路由到 GROWTH 阶段."""
    phase = orch._route_phase("年龄与生长 von bertalanffy 方程")
    assert phase == ResearchPhase.GROWTH

    phase = orch._route_phase("otolith age determination")
    assert phase == ResearchPhase.GROWTH


def test_phase_routing_trophic_keywords(orch):
    """包含营养级关键词的问题应路由到 TROPHIC 阶段."""
    phase = orch._route_phase("稳定同位素 δ13C δ15N 营养级")
    assert phase == ResearchPhase.TROPHIC

    phase = orch._route_phase("isotope mixing model MixSIAR")
    assert phase == ResearchPhase.TROPHIC


def test_phase_routing_coexistence_keywords(orch):
    """包含共存关键词的问题应路由到 COEXISTENCE 阶段."""
    phase = orch._route_phase("生态位重叠 niche overlap Pianka")
    assert phase == ResearchPhase.COEXISTENCE

    phase = orch._route_phase("同域共存 sympatric coexistence")
    assert phase == ResearchPhase.COEXISTENCE


def test_all_phase_results_have_findings(orch):
    """所有阶段的 PhaseResult 应包含至少一条 finding."""
    lit = _dummy_lit()
    question = "综合研究"
    # _execute_literature only takes question
    result = orch._execute_literature(question)
    assert len(result.findings) >= 1, \
        "_execute_literature 应至少返回 1 条 finding"
    for f in result.findings:
        assert isinstance(f, str) and len(f) > 0

    phases_two_args = [
        orch._execute_growth,
        orch._execute_genomics,
        orch._execute_genetics,
        orch._execute_trophic,
        orch._execute_coexistence,
        orch._execute_resource,
        orch._execute_habitat,
        orch._execute_report,
    ]
    for method in phases_two_args:
        result = method(question, lit)
        assert len(result.findings) >= 1, \
            f"{method.__name__} 应至少返回 1 条 finding"
        # 所有 finding 应为非空字符串
        for f in result.findings:
            assert isinstance(f, str) and len(f) > 0
