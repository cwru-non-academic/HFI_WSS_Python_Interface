from .log_sink import LogSink


class Logger:
    def __init__(self, sink: LogSink) -> None:
        self._sink = sink

    def info(self, message: str) -> None:
        self._sink.write("INFO", message)

    def warning(self, message: str) -> None:
        self._sink.write("WARN", message)

    def error(self, message: str) -> None:
        self._sink.write("ERROR", message)
