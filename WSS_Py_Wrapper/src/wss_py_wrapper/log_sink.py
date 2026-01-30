from __future__ import annotations

from datetime import datetime
from pathlib import Path
import threading
from typing import Callable


class LogSink:
    def write(self, level: str, message: str) -> None:
        raise NotImplementedError("Provide a sink implementation.")


class FileLogSink(LogSink):
    def __init__(self, path: Path) -> None:
        self._path = Path(path)
        self._lock = threading.Lock()

    @property
    def path(self) -> Path:
        return self._path

    def write(self, level: str, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {level}: {message}"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock:
            with self._path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")


def install_csharp_log_sink(log_type, sink: LogSink) -> Callable[[], None]:
    """
    Bind a Python sink to the C# Log.SetSink(Action<LogLevel,string>) API.
    Returns a reset callback to restore the default C# sink.
    """
    from System import Action  # type: ignore

    def handler(level, message) -> None:
        try:
            level_text = level.ToString()
        except Exception:
            level_text = str(level)
        sink.write(level_text.upper(), str(message))

    delegate = Action[log_type.LogLevel, str](handler)
    log_type.SetSink(delegate)

    def reset() -> None:
        log_type.ResetSink()

    return reset
