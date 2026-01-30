from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def _find_cs_libraries_dir(start: Path) -> Path:
    for base in (start, *start.parents):
        candidate = base / "Cs_Libraries"
        if candidate.is_dir():
            return candidate
    return start / "Cs_Libraries"


def _default_log_path(main_file: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return main_file.with_name(f"wss_{timestamp}.log")


@dataclass(frozen=True)
class WssConfig:
    config_path: Path
    log_path: Path
    cs_lib_dir: Path
    serial_port: str | None = None
    test_mode: bool = False
    max_setup_tries: int = 5
    tick_interval_ms: int = 10

    @classmethod
    def default(cls, main_file: Path) -> "WssConfig":
        cs_lib_dir = _find_cs_libraries_dir(main_file.parent)
        return cls(
            config_path=Path.cwd() / "Config",
            log_path=_default_log_path(main_file),
            cs_lib_dir=cs_lib_dir,
        )
