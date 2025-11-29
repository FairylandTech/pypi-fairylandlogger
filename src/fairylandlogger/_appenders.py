# coding: UTF-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2025-11-29 16:50:50 UTC+08:00
"""

import abc
import typing as t
from pathlib import Path

from loguru import logger as _loguru_logger

from ._enums import LogLevelEnum, EncodingEnum
from ._structure import LoggerRecordStructure


class AbstractLoggerAppender(abc.ABC):

    @abc.abstractmethod
    def add_sink(self):
        pass

    @abc.abstractmethod
    def emit(self, record: LoggerRecordStructure):
        pass


class EmitLoggerMixin:

    @staticmethod
    def _emit_by_level(level: t.Optional[t.Union[str, LogLevelEnum]], msg: str) -> None:
        if level == LogLevelEnum.TRACE:
            _loguru_logger.opt(depth=1).trace(msg)
        elif level == LogLevelEnum.DEBUG:
            _loguru_logger.opt(depth=1).debug(msg)
        elif level == LogLevelEnum.INFO:
            _loguru_logger.opt(depth=1).info(msg)
        elif level == LogLevelEnum.WARNING:
            _loguru_logger.opt(depth=1).warning(msg)
        elif level == LogLevelEnum.ERROR:
            _loguru_logger.opt(depth=1).error(msg)
        elif level == LogLevelEnum.SUCCESS:
            _loguru_logger.opt(depth=1).success(msg)
        else:
            _loguru_logger.opt(depth=1).critical(msg)


class ConsoleLoggerAppender(AbstractLoggerAppender, EmitLoggerMixin):
    _DEFAULT_PATTERN = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> | <level>{message}</level>"

    def __init__(self, level: t.Union[str, LogLevelEnum] = LogLevelEnum.INFO, pattern: t.Optional[str] = None):
        self._level = level
        self.pattern = pattern or self._DEFAULT_PATTERN

    @property
    def level(self):
        return self._level.value if isinstance(self._level, LogLevelEnum) else self._level

    @level.setter
    def level(self, value: t.Union[str, LogLevelEnum]):
        self._level = value

    def add_sink(self):
        _loguru_logger.add(
            sink=lambda x: print(x),
            level=self.level,
            format=self.pattern,
            colorize=True,
        )

    def emit(self, record: LoggerRecordStructure):
        self._emit_by_level(record.level, f"[{record.name}] {record.message}")


class FileLoggerAppender(AbstractLoggerAppender, EmitLoggerMixin):

    def __init__(
            self,
            path: t.Union[str, Path],
            level: t.Union[str, LogLevelEnum] = LogLevelEnum.INFO,
            retention: str = "180 days",
            rotation: str = "5 MB",
            encoding: t.Union[str, EncodingEnum] = EncodingEnum.UTF8,
    ):
        self.path = path
        self._level = level
        self.rotation = rotation
        self.retention = retention
        self._encoding = encoding

    @property
    def level(self):
        return self._level.value if isinstance(self._level, LogLevelEnum) else self._level

    @level.setter
    def level(self, value: t.Union[str, LogLevelEnum]):
        self._level = value

    @property
    def encoding(self):
        return self._encoding.value if isinstance(self._encoding, EncodingEnum) else self._encoding

    @encoding.setter
    def encoding(self, value: t.Union[str, EncodingEnum]):
        self._encoding = value

    def add_sink(self):
        _loguru_logger.add(
            sink=self.path,
            rotation=self.rotation,
            retention=self.retention,
            encoding=self.encoding,
            level=self.level,
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )

    def emit(self, record: LoggerRecordStructure):
        self._emit_by_level(record.level, f"[{record.name}] {record.message}")


class JSONLoggerAppender(AbstractLoggerAppender, EmitLoggerMixin):

    def __init__(
            self,
            path: t.Union[str, Path],
            level: t.Union[str, LogLevelEnum] = LogLevelEnum.INFO,
            retention: str = "180 days",
            rotation: str = "5 MB",
            encoding: t.Union[str, EncodingEnum] = EncodingEnum.UTF8,
    ):
        self.path = path
        self._level = level
        self.rotation = rotation
        self.retention = retention
        self._encoding = encoding

    @property
    def level(self):
        return self._level.value if isinstance(self._level, LogLevelEnum) else self._level

    @level.setter
    def level(self, value: t.Union[str, LogLevelEnum]):
        self._level = value

    @property
    def encoding(self):
        return self._encoding.value if isinstance(self._encoding, EncodingEnum) else self._encoding

    @encoding.setter
    def encoding(self, value: t.Union[str, EncodingEnum]):
        self._encoding = value

    def add_sink(self):
        _loguru_logger.add(
            sink=self.path,
            rotation=self.rotation,
            retention=self.retention,
            encoding=self.encoding,
            level=self.level,
            enqueue=True,
            backtrace=True,
            diagnose=True,
            serialize=True,
        )

    def emit(self, record: LoggerRecordStructure):
        self._emit_by_level(record.level, f"[{record.name}] {record.message}")
