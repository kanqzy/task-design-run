# 应用程序函数库(模拟)
# 应用程序的相关操作(启动, 窗口最大化/最小化/关闭/宽高缩到最小/拖拽移动, 关闭等)

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


def startApp(startExeName: str):
    """
    启动windows系统上的指定App应用程序

    参数:
        startExeName (str): 启动的可执行文件名称(.exe)
    """
    if log_function_enter_exit:
        log("info", "into startApp ...")

    time.sleep(1)
    log("info", "已成功启动 `{0}`".format(startExeName))

    if log_function_enter_exit:
        log("info", "startApp end")
        log("info", "\n", raw=True)


def activateWindow(winInfo: dict):
    """
    根据给定的窗口信息, 激活该窗口

    参数:
        winInfo (dict): 窗口信息
            数据结构: {
                processId: int,
                processExeName: str,
                processExePath: str,
                title: str
            }
    """
    if log_function_enter_exit:
        log("info", "into activateWindow ...")

    time.sleep(1)
    log("info", "已成功激活 `{0}` 所代表的窗口".format(winInfo))

    if log_function_enter_exit:
        log("info", "activateWindow end")
        log("info", "\n", raw=True)


def exitApp(exeName: str):
    """
    根据可执行文件名称, 退出windows系统对应的App应用程序

    参数:
        exeName (str): 可执行文件名称(.exe)
    """
    if log_function_enter_exit:
        log("info", "into exitApp ...")

    time.sleep(1)
    log("info", "已成功启动 `{0}`".format(exeName))

    if log_function_enter_exit:
        log("info", "exitApp end")
        log("info", "\n", raw=True)
