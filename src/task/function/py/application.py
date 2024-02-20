# 应用程序函数库
# 应用程序的相关操作(启动, 窗口最大化/最小化/关闭/宽高缩到最小/拖拽移动, 关闭等)

import time

import psutil
import pyautogui
import win32gui

import log
import logger

import keyInput
import window_util

Log_Formatter = {
    "formatter": log.Empty_Logging_Formatter,
    "msgFormat": "{asctime} function_library[application] => {message}",
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


def quickStartApp(shortcutName: str):
    """
    按 `Win` 键在搜索框输入应用程序快捷方式名称, 然后按 `Enter` 键启动应用程序

    参数:
        shortcutName (str): 应用程序快捷方式名称
    """
    if log_function_enter_exit:
        log("info", "into quickStartApp ...")

    pyautogui.hotkey("win")
    time.sleep(0.5)
    keyInput.inputChineseCharsWithLetters(shortcutName)
    time.sleep(0.5)
    pyautogui.hotkey("enter")
    time.sleep(1.5)

    log("info", "已成功启动 `{0}`".format(shortcutName))

    if log_function_enter_exit:
        log("info", "quickStartApp end")
        log("info", "\n", raw=True)


def activateWindow(winInfo: dict) -> bool:
    """
    根据给定的窗口信息, 激活该窗口

    参数:
        winInfo (dict): 窗口信息
            数据结构: {
                processId (int): 窗口进程ID
                processName (str): 窗口进程名 可打开任务管理器, 找到正在运行的目标窗体应用, 右键转到 详细信息栏, 名称列 即为目标进程名(忽略大小写)
                        例如记事本: `notpad.exe`
                processExePath (str): 进程可执行文件路径
                title (str): 窗口标题(包含匹配)
                className (str): 窗口类名
                isIconic (bool): 窗口是否图标化(窗口缩小到windows的任务栏上)
            }
    """
    if log_function_enter_exit:
        log("info", "into activateWindow ...")

    runingWindowHwnd = window_util.getRuningWindowHwnd(**winInfo)
    if runingWindowHwnd == -1:
        log("err", "fail found runingWindowHwnd for winInfo `{0}`".format(winInfo))
        return False

    win32gui.SetActiveWindow(runingWindowHwnd)

    if log_function_enter_exit:
        log("info", "activateWindow end")
        log("info", "\n", raw=True)

    return True


def exitApp(exeName: str) -> int:
    """
    根据可执行文件名称, 退出windows系统对应的App应用程序

    参数:
        exeName (str): 可执行文件名称(.exe)

    返回:
        返回成功退出的app进程数,
    """
    if log_function_enter_exit:
        log("info", "into exitApp ...")

    exitCount = 0
    for proc in psutil.process_iter():
        if proc.name().lower() == exeName:
            proc.terminate()
            exitCount += 1

    if log_function_enter_exit:
        log("info", "exitApp end")
        log("info", "\n", raw=True)

    return exitCount
