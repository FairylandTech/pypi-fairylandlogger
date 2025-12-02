# coding: UTF-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2025-11-29 16:56:33 UTC+08:00
"""

import os
import threading
import typing as t
from pathlib import Path

from loguru import logger as _loguru_logger

from ._appenders import AbstractLoggerAppender, ConsoleLoggerAppender, FileLoggerAppender, JSONLoggerAppender
from ._enums import LogLevelEnum
from ._structure import LoggerConfigStructure, LoggerRecordStructure


class LoggerRegistry:
    _instance: t.Optional["LoggerRegistry"] = None
    _lock: threading.RLock = threading.RLock()

    def __init__(self):
        self._configured: bool = False
        self._appenders: t.List[AbstractLoggerAppender] = []
        self._level: t.Union[str, LogLevelEnum] = LogLevelEnum.INFO
        self._levels: t.Dict[str, t.Union[str, LogLevelEnum]] = {}

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: t.Union[str, LogLevelEnum]):
        self._level = value

    @classmethod
    def get_instance(cls) -> "LoggerRegistry":
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls):
        with cls._lock:
            cls._instance = None
            try:
                _loguru_logger.remove()
            except Exception as error:
                raise error

    def configure(self, config: LoggerConfigStructure):
        with self._lock:
            try:
                _loguru_logger.remove()
            except Exception as error:
                raise error

            self._appenders.clear()
            self._level = config.level

            if config.console:
                console = ConsoleLoggerAppender(level=self._level)
                console.add_sink()
                self._appenders.append(console)
            if config.file:
                path = config.dirname
                os.makedirs(path, exist_ok=True)
                if isinstance(path, Path):
                    path = path.joinpath(config.filename)
                elif isinstance(path, str):
                    path = os.path.join(path, config.filename)
                else:
                    raise TypeError("dirname must be str or Path")

                # Add regular file appender
                file_appender = FileLoggerAppender(
                    path=path,
                    level=self._level,
                    rotation=config.rotation,
                    retention=config.retention,
                    encoding=config.encoding,
                    pattern=config.pattern,
                )
                file_appender.add_sink()
                self._appenders.append(file_appender)

                if config.json:
                    json_path = str(path)
                    if json_path.endswith('.log'):
                        json_path = json_path[:-4] + "-json" + '.log'
                    else:
                        json_path = json_path + '.json'

                    json_appender = JSONLoggerAppender(
                        path=json_path,
                        level=self._level,
                        rotation=config.rotation,
                        retention=config.retention,
                        encoding=config.encoding,
                    )
                    json_appender.add_sink()
                    self._appenders.append(json_appender)

            self._configured = True

    def ensure_default(self):
        if not self._configured:
            self.configure(LoggerConfigStructure())

    @staticmethod
    def _should_log(msg_level: t.Union[str, LogLevelEnum], eff_level: t.Union[str, LogLevelEnum]) -> bool:
        order = ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        msg_level = msg_level.value if isinstance(msg_level, LogLevelEnum) else msg_level
        eff_level = eff_level.value if isinstance(eff_level, LogLevelEnum) else eff_level

        try:
            return order.index(msg_level) >= order.index(eff_level)
        except ValueError:
            return True

    def set_level(self, prefix: str, level: t.Union[str, LogLevelEnum]) -> None:
        with self._lock:
            self._levels[prefix] = level

    def _effective_level(self, logger_name: str) -> str:
        best = ("", self._level)
        for p, lvl in self._levels.items():
            if logger_name.startswith(p) and len(p) > len(best[0]):
                best = (p, lvl)

        return best[1]

    def route(self, record: LoggerRecordStructure) -> None:
        depth = 3
        if not self._should_log(record.level, self._effective_level(record.name)):
            return
        msg = f"[{record.name}] {record.message}"
        if record.level == LogLevelEnum.TRACE:
            _loguru_logger.opt(depth=depth).trace(msg)
        elif record.level == LogLevelEnum.DEBUG:
            _loguru_logger.opt(depth=depth).debug(msg)
        elif record.level == LogLevelEnum.INFO:
            _loguru_logger.opt(depth=depth).info(msg)
        elif record.level == LogLevelEnum.WARNING:
            _loguru_logger.opt(depth=depth).warning(msg)
        elif record.level == LogLevelEnum.ERROR:
            _loguru_logger.opt(depth=depth).error(msg)
        elif record.level == LogLevelEnum.SUCCESS:
            _loguru_logger.opt(depth=depth).success(msg)
        else:
            _loguru_logger.opt(depth=depth).critical(msg)
