# 鼠标操作函数库(模拟)

import random
import time

import log
import logger

Log_Formatter = {
    "formatter": log.Empty_Logging_Formatter,
    "msgFormat": "{asctime} function_library[mouse] => {message}",
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


def mouse_move(pos: list | dict):
    """
    鼠标移到某位置
    """
    if log_function_enter_exit:
        log("info", "into mouse_move ...")
    if isinstance(pos, list) and len(pos) == 2:
        xPos, yPos = pos
        time.sleep(1)
        log("info", "鼠标已成功移到 `({0}, {1})`".format(xPos, yPos))

    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")
        time.sleep(1)
        log("info", "鼠标已成功移到 `({0}, {1})`".format(xPos, yPos))

    if log_function_enter_exit:
        log("info", "mouse_move end")
        log("info", "\n", raw=True)


def mouse_move_input(pos: list | dict, content: str):
    """
    鼠标移到某位置输入内容
    """
    if log_function_enter_exit:
        log("info", "into mouse_move_input ...")

    if isinstance(pos, list) and len(pos) == 2:
        xPos, yPos = pos
        time.sleep(2)
        log("info", "鼠标已移到 `({0}, {1})`, 并成功输入了 `{2}`".format(xPos, yPos, content))

    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")
        time.sleep(2)
        log("info", "鼠标已移到 `({0}, {1})`, 并成功输入了 `{2}`".format(xPos, yPos, content))

    if log_function_enter_exit:
        log("info", "mouse_move_input end")
        log("info", "\n", raw=True)


def mouse_move_input_enter(pos: list | dict, content: str):
    """
    鼠标移到某位置输入内容并回车
    """
    if log_function_enter_exit:
        log("info", "into mouse_move_input ...")
    if isinstance(pos, list) and len(pos) == 2:
        xPos, yPos = pos
        time.sleep(2)
        log(
            "info",
            "鼠标已移到 `({0}, {1})`, 输入了 `{2}`, 并成功进行了回车".format(xPos, yPos, content),
        )

    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")
        time.sleep(2)
        log(
            "info",
            "鼠标已移到 `({0}, {1})`, 输入了 `{2}`, 并成功进行了回车".format(xPos, yPos, content),
        )

    if log_function_enter_exit:
        log("info", "mouse_move_input end")
        log("info", "\n", raw=True)


def mouse_mousedown(pos: list | dict):
    """
    鼠标移到某位置点击
    """
    if log_function_enter_exit:
        log("info", "into mouse_mousedown ...")

    if isinstance(pos, list) and len(pos) == 2:
        xPos, yPos = pos
        time.sleep(1)
        log("info", "鼠标已移到 `({0}, {1}), 并成功进行了点击`".format(xPos, yPos))

    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")
        time.sleep(1)
        log("info", "鼠标已移到 `({0}, {1}), 并成功进行了点击`".format(xPos, yPos))

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
        time.sleep(1)
        log("info", "鼠标已移到 `({0}, {1}), 并成功进行了双击`".format(xPos, yPos))

    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")
        time.sleep(1)
        log("info", "鼠标已移到 `({0}, {1}), 并成功进行了双击`".format(xPos, yPos))

    if log_function_enter_exit:
        log("info", "mouse_doubleclick end")
        log("info", "\n", raw=True)


def mouse_get_text(
    pos: list | dict, recognize_rect_region_size: list = [60, 30]
) -> str:
    """
    鼠标移到某位置获取文本

    参数:
        pos (list, dict): 鼠标移动的坐标位置

    可选参数:
        recognize_rect_region_size (list): 识别的矩形区域大小 [w, h]
            以鼠标位置作为识别区域的中心点, 以当前参数作为识别的矩形区域大小

    返回:
        返回鼠标所在位置经过识别后得到的文本
    """
    if log_function_enter_exit:
        log("info", "into mouse_get_text ...")

    xPos = None
    yPos = None

    if isinstance(pos, list) and len(pos) == 2:
        xPos = pos[0]
        yPos = pos[1]
    elif isinstance(pos, dict):
        xPos = pos.get("x")
        yPos = pos.get("y")

    if xPos is None or yPos is None:
        log("err", "xPos|yPos is None")
        return None

    time.sleep(1)
    w, h = recognize_rect_region_size
    x1 = xPos - w // 2
    x2 = xPos + w // 2
    y1 = yPos - h // 2
    y2 = yPos + h // 2

    kwargs = {
        "xPos": xPos,
        "yPos": yPos,
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "w": w,
        "h": h,
    }
    log(
        "info",
        "鼠标已移到 `({xPos}, {yPos})`, 开始对屏幕矩形(区域: [{x1},{y1},{x2},{y2}], 大小: [{w}, {h}])进行识别 ...".format(
            **kwargs
        ),
    )

    time.sleep(1)
    texts = "我是中国人出生在信阳"
    random_index = random.randrange(0, len(texts))
    recognize_text = texts[random_index]

    log("info", "成功进行了识别, 识别到的文本为 `{0}`".format(recognize_text))

    if log_function_enter_exit:
        log("info", "mouse_get_text end\n")

    return recognize_text
