# coding: UTF-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2025-11-29 17:41:08 UTC+08:00
"""

import unittest

from fairylandlogger import LogManager, LoggerConfigStructure, LogLevelEnum


class TestFairylandLogger(unittest.TestCase):

    def setUp(self):
        """Reset the LogManager before each test."""
        LogManager.reset()

    def tearDown(self):
        """Reset the LogManager after each test to ensure clean state."""
        LogManager.reset()

    def test_logger(self):
        config = LoggerConfigStructure(
            level=LogLevelEnum.DEBUG,
            file=True,
            json=False,
        )

        print(config)

        LogManager.configure(config)
        logger = LogManager.get_logger(__name__)

        logger.info("Info message")
        logger.debug("Debug message")
        logger.error("Error message")
        logger.warning("Warning message")
        logger.success("Success message")
        logger.critical("Critical message")


if __name__ == "__main__":
    unittest.main()
