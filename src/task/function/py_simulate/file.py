# 文件操作函数库(模拟)

import random
import time

import log
import logger

Log_Formatter = {
    "formatter": log.Empty_Logging_Formatter,
    "msgFormat": "{asctime} function_library[file] => {message}",
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


def saveJsonData(jsonObj: object, outPath: str) -> bool:
    """
    将给定json数据保存到指定路径下

    返回:
        成功进行了保存返回 `True`
    """
    if log_function_enter_exit:
        log("info", "into saveJsonData ...")

    time.sleep(2)

    log("info", "以成功将JSON数据 `{0}` 保存到 路径 `{1}` 下".format(jsonObj, outPath))

    if log_function_enter_exit:
        log("info", "saveJsonData end")
        log("info", "\n", raw=True)

    return True
