# 鼠标操作函数库

import random
import time

import pyautogui

import log
import util

import log
import logger

Log_Formatter = {
    "formatter": log.Empty_Logging_Formatter,
    "msgFormat": "{asctime} function_library[mouse] => {message}",
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


def mouse_move(pos: list | dict):
    """
    鼠标移到某位置
    """
    if log_function_enter_exit:
        log("info", "into mouse_move ...")

    if isinstance(pos, list) and len(pos) == 2:
        xPos, yPos = pos
        pyautogui.moveTo(xPos, yPos)

    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")
        pyautogui.moveTo(xPos, yPos)

    if log_function_enter_exit:
        log("info", "mouse_move end")
        log("info", "\n", raw=True)


def mouse_relative_move(pos: list | dict):
    """
    鼠标相对移到某位置

    参数:
        pos (list, dict): 相对移动位置(相对当前坐标)
    """
    if log_function_enter_exit:
        log("info", "into mouse_relative_move ...")

    if isinstance(pos, list) and len(pos) == 2:
        xPos, yPos = pos
        pyautogui.move(xPos, yPos)

    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")
        pyautogui.move(xPos, yPos)

    if log_function_enter_exit:
        log("info", "mouse_relative_move end")
        log("info", "\n", raw=True)


def mouse_move_input(pos: list | dict, content: str):
    """
    鼠标移到某位置输入内容
    """
    if log_function_enter_exit:
        log("info", "into mouse_move_input ...")

    if isinstance(pos, list) and len(pos) == 2:
        xPos, yPos = pos
        pyautogui.moveTo(xPos, yPos)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.typewrite(content)

    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")
        pyautogui.moveTo(xPos, yPos)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.typewrite(content)

    if log_function_enter_exit:
        log("info", "mouse_move_input end")
        log("info", "\n", raw=True)


def mouse_move_input_enter(pos: list | dict, content: str):
    """
    鼠标移到某位置输入内容并回车
    """
    if log_function_enter_exit:
        log("info", "into mouse_move_input_enter ...")

    if isinstance(pos, list) and len(pos) == 2:
        xPos, yPos = pos
        pyautogui.moveTo(xPos, yPos)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.typewrite(content)
        time.sleep(0.5)
        pyautogui.hotkey("enter")

    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")
        pyautogui.moveTo(xPos, yPos)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.typewrite(content)
        time.sleep(0.5)
        pyautogui.hotkey("enter")

    if log_function_enter_exit:
        log("info", "mouse_move_input_enter end")
        log("info", "\n", raw=True)


def mouse_mousedown(pos: list | dict):
    """
    鼠标移到某位置点击
    """
    if log_function_enter_exit:
        log("info", "into mouse_mousedown ...")

    if isinstance(pos, list) and len(pos) == 2:
        xPos, yPos = pos
        pyautogui.moveTo(xPos, yPos)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)

    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")
        pyautogui.moveTo(xPos, yPos)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)

    if log_function_enter_exit:
        log("info", "mouse_mousedown end")
        log("info", "\n", raw=True)


def mouse_doubleclick(pos: list | dict):
    """
    鼠标移到某位置双击
    """
    if log_function_enter_exit:
        log("info", "into mouse_doubleclick ...")

    if isinstance(pos, list) and len(pos) == 2:
        xPos, yPos = pos
        pyautogui.moveTo(xPos, yPos)
        time.sleep(0.5)
        pyautogui.doubleClick()
        time.sleep(0.5)

    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")
        pyautogui.moveTo(xPos, yPos)
        time.sleep(0.5)
        pyautogui.doubleClick()
        time.sleep(0.5)

    if log_function_enter_exit:
        log("info", "mouse_doubleclick end")
        log("info", "\n", raw=True)


def mouse_get_text(pos: list | dict):
    """
    鼠标移到某位置获取文本

    接口暂未开放, 当前方法仅做模拟示范
    """
    if log_function_enter_exit:
        log("info", "into mouse_get_text ...")

    if isinstance(pos, list) and len(pos) == 2:
        xPos, yPos = pos
        texts = "我是中国人".split("")
        random_index = random.randrange(0, 4)
        recognize_text = texts[random_index]
        time.sleep(1)
        log(
            "info",
            "鼠标已移到 `({0}, {1})`, 并成功获取到文本 `{2}`".format(xPos, yPos, recognize_text),
        )
        return recognize_text

    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")
        texts = "我是中国人".split("")
        random_index = random.randrange(0, 4)
        recognize_text = texts[random_index]
        time.sleep(1)
        log(
            "info",
            "鼠标已移到 `({0}, {1})`, 并成功获取到文本 `{2}`".format(xPos, yPos, recognize_text),
        )
        return recognize_text

    if log_function_enter_exit:
        log("info", "mouse_get_text end")
        log("info", "\n", raw=True)

    return None
