# coding: UTF-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2025-11-29 16:58:56 UTC+08:00
"""

import typing as t

from ._structure import LoggerConfigStructure, LoggerRecordStructure
from ._registry import LoggerRegistry
from ._enums import LogLevelEnum


class Logger:

    def __init__(self, name: str):
        self._name = name

    def _emit(self, level: LogLevelEnum, msg: str, **kwargs) -> None:
        record = LoggerRecordStructure(name=self._name, level=level.upper(), message=msg, extra=kwargs or {})
        LoggerRegistry.get_instance().route(record)

    def trace(self, msg: str, **kwargs) -> None:
        self._emit(LogLevelEnum.TRACE, msg, **kwargs)

    def debug(self, msg: str, **kwargs) -> None:
        self._emit(LogLevelEnum.DEBUG, msg, **kwargs)

    def info(self, msg: str, **kwargs) -> None:
        self._emit(LogLevelEnum.INFO, msg, **kwargs)

    def success(self, msg: str, **kwargs) -> None:
        self._emit(LogLevelEnum.SUCCESS, msg, **kwargs)

    def warning(self, msg: str, **kwargs) -> None:
        self._emit(LogLevelEnum.WARNING, msg, **kwargs)

    def error(self, msg: str, **kwargs) -> None:
        self._emit(LogLevelEnum.ERROR, msg, **kwargs)

    def critical(self, msg: str, **kwargs) -> None:
        self._emit(LogLevelEnum.CRITICAL, msg, **kwargs)


class LogManager:
    _configured: bool = False
    _loggers: t.Dict[str, Logger] = {}

    @classmethod
    def configure(cls, config: LoggerConfigStructure) -> None:
        LoggerRegistry.get_instance().configure(config)
        cls._configured = True

    @classmethod
    def get_logger(cls, name: str = "default") -> Logger:
        if not cls._configured:
            LoggerRegistry.get_instance().ensure_default()
            cls._configured = True
        if name not in cls._loggers:
            cls._loggers[name] = Logger(name)
            if name != "default":
                LoggerRegistry.get_instance().add_file_sink(name)
        return cls._loggers[name]

    @classmethod
    def reset(cls) -> None:
        LoggerRegistry.reset()
        cls._configured = False
        cls._loggers.clear()

    @classmethod
    def set_level(cls, prefix: str, level: str) -> None:
        LoggerRegistry.get_instance().set_level(prefix, level)

    @classmethod
    def get_registry(cls):
        for appender in LoggerRegistry.get_instance()._appenders:
            print(appender)
