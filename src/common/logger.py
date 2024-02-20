import log


_Logger = None


def getLogger(logRootDir: str = None, logInConsole=True):
    """
    获取日志记录器
    """
    global _Logger
    if _Logger is None:
        if logRootDir:
            _Logger = log.Logger(logRootDir=logRootDir, logInConsole=logInConsole)
        else:
            _Logger = log.Logger(logInConsole=logInConsole)
    return _Logger


def getCustomLogger(
    logRootDir, logInConsole=True, logConsoleFormatter=log.Formatter_Raw
):
    """
    获取自定义日志记录器
    """
    global _Logger
    if _Logger is None:
        _Logger = log.Logger(
            logRootDir=logRootDir,
            logInConsole=logInConsole,
            logConsoleFormatter=logConsoleFormatter,
        )
    return _Logger
