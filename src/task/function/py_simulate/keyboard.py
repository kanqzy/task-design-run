# 键盘操作函数库(模拟)

import random
import time

import log
import logger

Log_Formatter = {
    "formatter": log.Empty_Logging_Formatter,
    "msgFormat": "{asctime} function_library[keyboard] => {message}",
}


# 设置
log_function_enter_exit = True

logRootDir = None
LOGGER = None
__logCount = 0


def log(
    type: str,
    logContent: str,
    logConsoleFormatter=Log_Formatter,
    logFileFormatter=Log_Formatter,
    **kwargs
):
    global __logCount, LOGGER
    __logCount += 1
    if __logCount == 1:
        LOGGER = logger.getLogger(logRootDir=logRootDir)

    kwargs["logConsoleFormatter"] = logConsoleFormatter
    kwargs["logFileFormatter"] = logFileFormatter

    if type == "info":
        LOGGER.info(logContent, **kwargs)
    if type == "err":
        LOGGER.error(logContent, **kwargs)


def pressKey(key: str):
    """
    键盘按下指定的键
    """
    if log_function_enter_exit:
        log("info", "into pressKey ...")

    pass
    log("info", "已成功按下 `{0}` 键".format(key))

    if log_function_enter_exit:
        log("info", "pressKey end")
        log("info", "\n", raw=True)


def pressHotKey(hotKey: str):
    """
    键盘按下指定的热键(如: `Enter`, `Esc`等)
    """
    if log_function_enter_exit:
        log("info", "into pressHotKey ...")

    pass
    log("info", "已成功按下 `{0}` 热键".format(hotKey))

    if log_function_enter_exit:
        log("info", "pressHotKey end")
        log("info", "\n", raw=True)


def inputChineseChars(chineseChars: str):
    """
    输入中文字符
    
    参数:
        chineseChars (str): 一串字符(包含中文字符)
    """
    if log_function_enter_exit:
        log("info", "into inputChineseChars ...")

    pass
    log("info", "已成功输入 `{0}` 热键".format(chineseChars))

    if log_function_enter_exit:
        log("info", "inputChineseChars end")
        log("info", "\n", raw=True)
