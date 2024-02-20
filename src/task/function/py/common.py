# 公共函数库

from datetime import datetime
import time

import pyautogui

import log
import util


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


def capture_screen_region(outPath: str, screen_region: list[int] = None) -> bool:
    """
    截屏屏幕区域

    可选参数:
        screen_region (list[int]): 屏幕截屏区域 [x1,y1,x2,y2]
            为 `None` 时表示截全屏

    返回:
        成功截屏并保存到本地返回 `True`
    """
    if not util.isValidFilePath(outPath):
        return False

    screenshot_image = None
    if screen_region:
        x1, y1, x2, y2 = screen_region
        screenshot_region = (x1, y1, x2 - x1, y2 - y1)
        screenshot_image = pyautogui.screenshot(region=screenshot_region)
    else:
        screenshot_image = pyautogui.screenshot()

    screenshot_image.save(outPath)

    if util.isFile(outPath):
        return True

    return False


def doNothing():
    """
    不做任何操作

    在python里, 这相当于 `pass` 语句
    """
    if log_function_enter_exit:
        log("info", "into doNothing ...")

    pass

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

    if log_function_enter_exit:
        log("info", "interrupt end")
        log("info", "\n", raw=True)


def getFormatNowTime(format: str = "yyyy-MM-dd HH:mm:ss:ms") -> str:
    """
    获取格式化的当前时间
    """
    nowTime = datetime.now()

    if format == "yyyy-MM-dd HH:mm:ss:ms":
        nowTimeFormat = nowTime.strftime("%Y-%m-%d %H:%M:%S")
        nowTimeFormat += ":" + str(nowTime.microsecond // 1000)
        return nowTimeFormat

    elif format == "yyyy-MM-dd HH-mm-ss":
        nowTimeFormat = nowTime.strftime("%Y-%m-%d %H-%M-%S")
        return nowTimeFormat

    nowTimeFormat = nowTime.strftime("%Y-%m-%d %H:%M:%S")
    return nowTimeFormat
