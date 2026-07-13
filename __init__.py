"""fangtao_fishlab — main system entry point."""
from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path

_BASE = _Path(__file__).resolve().parent
_REASONIX = _BASE.parent
for _p in [_REASONIX, _BASE] + [_BASE / d for d in [
    'cognitive-search-engine', 'fish-ecology-assistant', 'eon-core',
    'conflict-arbiter', 'porpoise-agent', 'coilia-agent', 'culter-agent',
    'infrastructure', '_bayesian', '_shared']]:
    _s = str(_p)
    if _s not in _sys.path:
        _sys.path.insert(0, _s)

from _bayesian import BetaBelief, NormalBelief, DirichletBelief, SelfCheckReport, SelfCheckMixin
from _bayesian.applications import SearchCredibility, KnowledgeUpdater, ConflictResolver, ChangePointDetector, AgentBelief, MetaBayesian
from _shared.types import AdapterState, SearchResult, CheckReport

__version__ = "v8.0.0"

def health_check_all() -> dict:
    from .scripts.health_check_all import check_all as _check
    return _check()

def get_adapter(project_name: str):
    from importlib import import_module
    adapters = {
        "cognitive-search-engine": "cognitive-search-engine.src.adapter.CognitiveSearchAdapter",
        "fish-ecology-assistant": "fish-ecology-assistant.src.adapter.FishEcologyAdapter",
        "eon-core": "eon-core.src.adapter.EonCoreAdapter",
        "conflict-arbiter": "conflict-arbiter.src.adapter.ConflictArbiterAdapter",
        "porpoise-agent": "porpoise-agent.src.adapter.PorpoiseAdapter",
        "coilia-agent": "coilia-agent.src.adapter.CoiliaAdapter",
        "culter-agent": "culter-agent.src.adapter.CulterAdapter",
        "infrastructure": "infrastructure.src.adapter.InfrastructureAdapter",
        "san-sheng-wanwu-core": "san-sheng-wanwu-core.src",
    }
    if project_name not in adapters:
        raise ValueError(f"Unknown: {project_name} (available: {list(adapters.keys())})")
    path = adapters[project_name]
    try:
        if "." in path:
            mod_path, cls_name = path.rsplit(".", 1)
            if "-" in mod_path:
                import importlib.util
                proj_name = mod_path.split(".")[0]
                _candidates = [
                    f"D:/Reasonix/fangtao_fishlab/{proj_name}/src/adapter.py",
                    f"D:/Reasonix/{proj_name}/src/adapter.py",
                ]
                _p = next((p for p in _candidates if __import__('os').path.exists(p)), None)
                if _p is None:
                    raise FileNotFoundError(f"adapter.py not found for '{proj_name}'")
                _proj_root = str(_Path(_p).resolve().parent.parent)
                if _proj_root not in _sys.path:
                    _sys.path.insert(0, _proj_root)
                spec = importlib.util.spec_from_file_location(cls_name, _p)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return getattr(mod, cls_name)()
            else:
                mod = import_module(mod_path)
            return getattr(mod, cls_name)()
        else:
            mod = import_module(path.replace("-", "_"))
            return mod
    except Exception as e:
        raise ImportError(f"Cannot load adapter '{project_name}': {e}") from e

def query_library(keyword: str, category: str = "species") -> list:
    from pathlib import Path
    _lib = Path(__file__).resolve().parent.parent / "fangtao_library"
    if not _lib.exists():
        return []
    target = {
        "species": _lib / "species",
        "theories": _lib / "fangtao_library" / "02-basic_theory",
        "notes": _lib / "fangtao_library" / "01-research_notes",
        "papers": _lib / "fangtao_library" / "04-literature_review",
    }.get(category)
    if target is None or not target.exists():
        return []
    results = []
    for f in target.rglob("*"):
        if f.is_file() and keyword.lower() in f.name.lower():
            results.append(str(f.relative_to(_lib)))
    return results
