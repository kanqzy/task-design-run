# QQ应用程序上操作函数库(模拟)

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


def get_qq_processId(qqNumber: int) -> int:
    """
    检测指定QQ号的窗口进程Id, 如果该QQ号未登录返回 `-1`

    在实际获取中会激活当前已登录的所有QQ号, 在主界面顶部查找对应的QQ号的头像,
    若, 找到, 则认为当前窗口就是该QQ号;反之则继续检查一个窗口,...;直到检查完毕
    """
    if log_function_enter_exit:
        log("info", "into get_qq_processId ...")

    time.sleep(2)
    random_processId = random.randrange(0, 65566)
    log("info", "已成功获取进程id `{0}` for qqNumber `{1}`".format(random_processId, qqNumber))

    if log_function_enter_exit:
        log("info", "get_qq_processId end")
        log("info", "\n", raw=True)

    return random_processId


def foucus_chat_window_input() -> list[int]:
    """
    将鼠标光标聚焦聊天窗口输入框

    在实际聚焦中, 会在当前电脑屏幕上找到所有的QQ窗口, 找到其中包含 `发送`按钮图像的那个窗口,
    首先点击 锁屏探测 `x`按钮, 接着点击 `发送` 上面的50-100px像素处

    返回:
        发送按钮位置
    """
    if log_function_enter_exit:
        log("info", "into foucus_chat_window_input ...")

    time.sleep(2)
    random_pos_x = random.randrange(0, 300)
    random_pos_y = random.randrange(0, 300)
    send_pos = [random_pos_x, random_pos_y]
    log("info", "检测到 `发送` 按钮坐标 `{0}`, 并成功聚焦聊天窗口输入框".format(send_pos))

    if log_function_enter_exit:
        log("info", "foucus_chat_window_input end")
        log("info", "\n", raw=True)

    return send_pos


def foucus_friendInfo_window_and_draw_right():
    """
    将鼠标光标聚焦好友资料窗口并将其向右拖拽

    在实际聚焦中, 会在当前电脑屏幕上找到所有的QQ窗口, 找到其中包含 `备注` 按钮图像的那个窗口,
    认定为好友信息窗口, 然后点击窗口顶部中间位置不释放向右拖拽50-100px保证当前窗口不被主窗口遮盖,
    """
    if log_function_enter_exit:
        log("info", "into foucus_friendInfo_window_and_draw_right ...")

    time.sleep(2)

    log("info", "以成功聚焦好友信息窗口, 并向右拖拽到不被主窗口遮挡的位置")

    if log_function_enter_exit:
        log("info", "foucus_friendInfo_window_and_draw_right end")
        log("info", "\n", raw=True)

def recognize_friendInfo_window_data() -> dict:
    """
    识别好友信息窗口数据
    
    在实际识别过程中会调用 `UIAutomation` 库识别windows gui中的组件元素
    """
    if log_function_enter_exit:
        log("info", "into foucus_friendInfo_window_and_draw_right ...")

    time.sleep(2)
    qqNumbers = [111111,222222,33333333,4444444]
    random_qqNumber_index = random.randrange(0, 3)
    qqNumber = qqNumbers[random_qqNumber_index]
    qqData = {
        "qqNumber": qqNumber,
        "remarkName": "一路走来"
    }
    log("info", "以成功识别好友信息窗口数据 => `{0}`".format(qqData))

    if log_function_enter_exit:
        log("info", "foucus_friendInfo_window_and_draw_right end")
        log("info", "\n", raw=True)
        
    return qqData