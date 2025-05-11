import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Literal


class Log:
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    def __init__(self, name="", path=""):
        self.name = name
        self.path = path
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

    def _has_handleroftype(self, handler_type: type):
        """
        检查logger是否已经包含了一个特定类型的handler。

        参数:
        - handler_type: 要检查的日志处理器类型。

        返回:
        - 如果已经存在一个特定类型的handler，则返回True；否则返回False。
        """

        return any(
            isinstance(handler, handler_type) for handler in self.logger.handlers
        )

    def _getpath(self, file_path):
        file_path = str(file_path).strip()
        if file_path is None or file_path == "":
            return self.path
        return file_path

    def _sethander(self, h: logging.Handler, level=logging.DEBUG):
        h.setFormatter(Log.formatter)
        h.setLevel(level)
        self.logger.addHandler(h)

    def addCMDloging(self, level=logging.DEBUG):
        if self._has_handleroftype(logging.StreamHandler):
            return self
        h = logging.StreamHandler()
        self._sethander(h, level)
        return self

    def addRotatingFilelogging(
        self,
        path: str|Path ,
        maxBytes: int = 0,
        backupCount: int = 0,
        
        level=logging.DEBUG,
    ):
        """
        Open the specified file and use it as the stream for logging.

        By default, the file grows indefinitely. You can specify particular
        values of maxBytes and backupCount to allow the file to rollover at
        a predetermined size.

        Rollover occurs whenever the current log file is nearly maxBytes in
        length. If backupCount is >= 1, the system will successively create
        new files with the same pathname as the base file, but with extensions
        ".1", ".2" etc. appended to it. For example, with a backupCount of 5
        and a base file name of "app.log", you would get "app.log",
        "app.log.1", "app.log.2", ... through to "app.log.5". The file being
        written to is always "app.log" - when it gets filled up, it is closed
        and renamed to "app.log.1", and if files "app.log.1", "app.log.2" etc.
        exist, then they are renamed to "app.log.2", "app.log.3" etc.
        respectively.

        If maxBytes is zero, rollover never occurs.
        """
        if self._has_handleroftype(RotatingFileHandler):
            return self
        path = self._getpath(file_path=path)
        h = RotatingFileHandler(
            filename=path, maxBytes=maxBytes, backupCount=backupCount
        )
        self._sethander(h, level)
        return self

    def addTimedRotatingFilelogging(
        self,
        path: str | Path,
        when: Literal[
            "D", "S", "M", "H", "midnight", "w0", "w1", "w2", "w3", "w4", "w5", "w6"
        ] = "D",
        interval=1,
        backupCount=7,
        
        level=logging.DEBUG,
    ):
        # Calculate the real rollover interval, which is just the number of
        # seconds between rollovers.  Also set the filename suffix used when
        # a rollover occurs.  Current 'when' events supported:
        # S - Seconds
        # M - Minutes
        # H - Hours
        # D - Days
        # midnight - roll over at midnight
        # W{0-6} - roll over on a certain day; 0 - Monday
        #
        # Case of the 'when' specifier is not important; lower or upper case
        # will work.
        if self._has_handleroftype(TimedRotatingFileHandler):
            return self
        path = self._getpath(path)
        h = TimedRotatingFileHandler(
            filename=path, when=when, interval=interval, backupCount=backupCount
        )
        self._sethander(h, level)
        return self

    def info(self, msg, *args, stack_info: bool = False, stacklevel: int = 1):
        self.logger.info(msg=msg, *args, stack_info=stack_info, stacklevel=stacklevel)

    def debug(self, msg, *args, stack_info: bool = False, stacklevel: int = 1):
        self.logger.debug(msg=msg, *args, stack_info=stack_info, stacklevel=stacklevel)

    def warning(self, msg, *args, stack_info: bool = False, stacklevel: int = 1):
        self.logger.warning(msg=msg, *args, stack_info=stack_info, stacklevel=stacklevel)

    def error(self, msg, *args, stack_info: bool = False, stacklevel: int = 1):
        self.logger.error(msg=msg, *args, stack_info=stack_info, stacklevel=stacklevel)

    def critical(self, msg, *args, stack_info: bool = False, stacklevel: int = 1):
        self.logger.critical(
            msg=msg, *args, stack_info=stack_info, stacklevel=stacklevel
        )


logger = Log()
logger.addCMDloging()  # .addTimedRotatingFilelogging(when='D')


def info(msg, *args, stack_info: bool = False, stacklevel: int = 1):
    logger.info(msg=msg, *args, stack_info=stack_info, stacklevel=stacklevel)


def debug(msg, *args, stack_info: bool = False, stacklevel: int = 1):
    logger.debug(msg=msg, *args, stack_info=stack_info, stacklevel=stacklevel)


def warning(msg, *args, stack_info: bool = False, stacklevel: int = 1):
    logger.warning(msg=msg, *args, stack_info=stack_info, stacklevel=stacklevel)


def error(msg, *args, stack_info: bool = False, stacklevel: int = 1):
    logger.error(msg=msg, *args, stack_info=stack_info, stacklevel=stacklevel)


def critical(msg, *args, stack_info: bool = False, stacklevel: int = 1):
    logger.critical(msg=msg, *args, stack_info=stack_info, stacklevel=stacklevel)
