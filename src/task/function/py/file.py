# 文件操作函数库

import random
import time

import log
import logger
import util

Log_Formatter = {
    "formatter": log.Empty_Logging_Formatter,
    "msgFormat": "{asctime} function_library[file] => {message}",
}


# 设置
log_function_enter_exit = True

logRootDir = None
LOGGER = None
__logCount = 0


def log(type: str, logContent: str, *args, **kwargs):
    global __logCount, LOGGER
    __logCount += 1
    if __logCount == 1:
        LOGGER = logger.getLogger()

    enable = kwargs.get("enable")
    if enable is not None:
        if not enable:
            return
        else:
            del kwargs["enable"]

    if type == "debug":
        LOGGER.debug(logContent, *args, **kwargs)

    elif type == "info":
        LOGGER.info(logContent, *args, **kwargs)

    elif type == "warn":
        LOGGER.warn(logContent, *args, **kwargs)

    elif type == "err" or type == "error":
        LOGGER.error(logContent, *args, **kwargs)



def saveJsonData(jsonObj: object, outPath: str) -> bool:
    """
    将给定json数据保存到指定路径下

    返回:
        成功进行了保存返回 `True`
    """
    if log_function_enter_exit:
        log("info", "into saveJsonData ...")

    if jsonObj is None or not util.isValidFilePath(outPath):
        return False

    result = util.writeJson(outPath, jsonObj, indent=4)

    if log_function_enter_exit:
        log("info", "saveJsonData end")
        log("info", "\n", raw=True)

    return result
