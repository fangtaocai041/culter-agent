
import sys as _sys
from pathlib import Path as _Path
_PROJECT_ROOT = str(_Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in _sys.path:
    _sys.path.insert(0, _PROJECT_ROOT)

def _load_version():
    """Read version from VERSION.yaml — single source of truth."""
    try:
        import yaml
        from pathlib import Path as _VP
        _vpath = _VP(__file__).resolve().parent.parent.parent / "VERSION.yaml"
        with open(_vpath, encoding="utf-8") as _f:
            _data = yaml.safe_load(_f)
        _key = _VP(__file__).resolve().parent.parent.name
        return _data.get("projects", {}).get(_key, {}).get("version", "0.0.0")
    except Exception:
        return "0.0.0"

__version__ = _load_version()
