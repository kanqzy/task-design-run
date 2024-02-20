# 公共函数库(模拟)

import time

import log
import logger

Log_Formatter = {
    "formatter": log.Empty_Logging_Formatter,
    "msgFormat": "{asctime} function_library[common] => {message}",
}

# 设置
log_function_enter_exit = True

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
        LOGGER = logger.getLogger()

    kwargs["logConsoleFormatter"] = logConsoleFormatter
    kwargs["logFileFormatter"] = logFileFormatter

    if type == "info":
        LOGGER.info(logContent, **kwargs)


def printLog(logContent: str):
    """
    打印日志
    """
    if log_function_enter_exit:
        log("info", "into printLog ...")

    time.sleep(0.5)
    log("info", "已成功打印日志 `{0}`".format(logContent))

    if log_function_enter_exit:
        log("info", "printLog end")
        log("info", "\n", raw=True)


def wait(waitTime: int):
    """
    等待一段时间

    参数:
        waitTime (int): 等待时间(毫秒)
    """
    log("info", "等待 {0} 毫秒 ...".format(waitTime))
    time.sleep(waitTime / 1000)
    log("info", "\n", raw=True)


def doNothing():
    """
    不做任何操作

    在python里, 这相当于 `pass` 语句
    """
    if log_function_enter_exit:
        log("info", "into doNothing ...")

    pass
    log("info", "已成功执行完")

    if log_function_enter_exit:
        log("info", "doNothing end")
        log("info", "\n", raw=True)

def interrupt():
    """
    中断程序, 从主任务及其所有子任务中退出

    在python里, 这相当于在所有方法中 `return`
    """
    if log_function_enter_exit:
        log("info", "into interrupt ...")

    pass
    log("info", "已成功中断程序")

    if log_function_enter_exit:
        log("info", "interrupt end")
        log("info", "\n", raw=True)