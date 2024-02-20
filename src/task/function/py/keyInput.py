# 键盘输入函数库

import re
import time

import pyautogui
from pypinyin import pinyin, lazy_pinyin

import log
import logger

Log_Formatter = {
    "formatter": log.Empty_Logging_Formatter,
    "msgFormat": "{asctime} function_library[keyInput] => {message}",
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


def pressKey(key: str):
    """
    键盘按下指定的一个键

    可支持如 方向键('up','down','left','right')等的常用按键
    """
    if log_function_enter_exit:
        log("info", "into pressKey ...")

    pyautogui.press(key)
    time.sleep(0.5)

    if log_function_enter_exit:
        log("info", "pressKey end")
        log("info", "\n", raw=True)


def pressHotKey(hotKey: str):
    """
    键盘按下指定的热键(如: `Enter`, `Esc`等)
    """
    if log_function_enter_exit:
        log("info", "into pressHotKey ...")

    pyautogui.hotkey(hotKey)

    if log_function_enter_exit:
        log("info", "pressHotKey end")
        log("info", "\n", raw=True)


def inputChineseChars(chineseChars: str, mouseReturnBack=True) -> bool:
    """
    输入中文字符

    参数:
        chineseChars (str): 一串字符(全部为中文字符)
        mouseReturnBack (bool): 鼠标是否回到输入中文前的位置
    """
    if log_function_enter_exit:
        log("info", "into inputChineseChars ...")

    if not re.match(r"^[\u4e00-\u9fa5]+$", chineseChars):
        log("err", "chineseChars `{0}` not all is chinse char".format(chineseChars))
        if log_function_enter_exit:
            log("info", "inputChineseChars end")
            log("info", "\n", raw=True)
        return False

    # 记录当前鼠标坐标
    xPos, yPos = pyautogui.position()
    log("info", "current pos: [{0}, {1}]", xPos, yPos)

    # 鼠标移到电脑底部任务栏的 `搜狗输入法` 图标点击
    pyautogui.moveTo(1745, 1058)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.5)

    # 在弹出的菜单栏中鼠标移到 `中文(简体, 中国)` 菜单项, 点击
    pyautogui.moveRel(0, -365)
    time.sleep(0.5)
    pyautogui.click()

    pinyin = lazy_pinyin(chineseChars)
    pinyinStr = "".join(pinyin)
    pyautogui.typewrite(pinyinStr)
    time.sleep(0.3)
    pyautogui.press("space")
    log("info", "已成功输入中文字符 `{0}`".format(chineseChars))

    # 最后按 `ctrl+shift`输入法且为美式键盘英语(ENG)
    time.sleep(1)
    pyautogui.hotkey("ctrl", "shift")
    time.sleep(0.5)

    # 回到最开始鼠标位置
    if mouseReturnBack:
        pyautogui.moveTo(xPos, yPos)
        time.sleep(0.5)

    if log_function_enter_exit:
        log("info", "inputChineseChars end")
        log("info", "\n", raw=True)

    return True


def group_mark_chinese_char(chineseCharsWithLetter: str) -> list[dict]:
    """
    对给定的带有字母的汉字字符串进行汉字分组标记

    返回:
        [
            {
               isWholeChinse: bool,
               span: [startIndex, endIndex]
            },
            ...
        ]
    """
    chinseCharSpanInfos = [
        substr.span()
        for substr in re.finditer(r"[\u4e00-\u9fa5]+", chineseCharsWithLetter)
    ]

    group_infos = []
    chinseCharSpanInfos_len = len(chinseCharSpanInfos)
    i = 0
    while i < chinseCharSpanInfos_len:
        chinseCharSpanInfo = chinseCharSpanInfos[i]
        chinse_char_start_index = chinseCharSpanInfo[0]

        last_chinseCharSpanInfo = chinseCharSpanInfos[i - 1] if i > 0 else None

        if last_chinseCharSpanInfo is None:
            if chinse_char_start_index > 0:
                last_group_info = {
                    "isWholeChinse": False,
                    "span": (0, chinse_char_start_index),
                }
                group_infos.append(last_group_info)

            else:
                pass

        else:
            last_group_info = {
                "isWholeChinse": False,
                "span": (last_chinseCharSpanInfo[1], chinse_char_start_index),
            }
            group_infos.append(last_group_info)

        current_group_info = {"isWholeChinse": True, "span": chinseCharSpanInfo}
        group_infos.append(current_group_info)

        i += 1

    # 如果最后一个 `chinseCharSpanInfos` 的结束索引不是字符串的长度, 则将将剩余的补充填为非汉字的字符
    chineseCharsWithLetter_len = len(chineseCharsWithLetter)
    if chinseCharSpanInfos[-1][1] != chineseCharsWithLetter_len:
        group_info = {
            "isWholeChinse": False,
            "span": (chinseCharSpanInfos[-1][1], chineseCharsWithLetter_len),
        }
        group_infos.append(group_info)

    return group_infos


def inputChineseCharsWithLetters(chineseChars: str,mouseReturnBack=True) -> bool:
    """
    输入中文字符(带有英文字母)

    参数:
        chineseChars (str): 一串字符(带有英文字母)
    """
    if log_function_enter_exit:
        log("info", "into inputChineseCharsWithLetters ...")

    if not re.match(r"^.*[\u4e00-\u9fa5].*$", chineseChars):
        # 不包含中文字符串, 直接输入
        pyautogui.typewrite(chineseChars)
        time.sleep(0.5)

        log("info", "已成功输入字符(不带中文) `{0}`".format(chineseChars))

        if log_function_enter_exit:
            log("info", "inputChineseCharsWithLetters end")
            log("info", "\n", raw=True)
        return True

    # 记录当前鼠标坐标
    xPos, yPos = pyautogui.position()
    log("info", "current pos: [{0}, {1}]", xPos, yPos)

    # 鼠标移到电脑底部任务栏的 `搜狗输入法` 图标点击
    pyautogui.moveTo(1745, 1058)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.5)

    # 在弹出的菜单栏中鼠标移到 `中文(简体, 中国)` 菜单项, 点击
    pyautogui.moveRel(0, -365)
    time.sleep(0.5)
    pyautogui.click()

    # 然后按 `shift` 切回为英文
    time.sleep(1)
    pyautogui.press("shift")
    time.sleep(0.5)

    chineseChars_groups = group_mark_chinese_char(chineseChars)
    for group in chineseChars_groups:
        group_span = group["span"]
        group_content = chineseChars[group_span[0] : group_span[1]]
        if group["isWholeChinse"]:
            # 按 `Shift` 输入法切回中文
            pyautogui.hotkey("shift")
            time.sleep(1)

            pinyin = lazy_pinyin(group_content)
            pinyinStr = "".join(pinyin)
            pyautogui.typewrite(pinyinStr)
            time.sleep(0.5)
            pyautogui.press("space")
            time.sleep(0.5)

            # 按 `Shift` 输入法切回英文
            pyautogui.hotkey("shift")
            time.sleep(1)

        else:
            pyautogui.typewrite(group_content)
            time.sleep(0.5)

    log("info", "已成功输入中文字符 `{0}`".format(chineseChars))

    # 最后按 `ctrl+shift`输入法且为美式键盘英语(ENG)
    time.sleep(1)
    pyautogui.hotkey("ctrl", "shift")
    time.sleep(0.5)

    # 回到最开始鼠标位置
    if mouseReturnBack:
        pyautogui.moveTo(xPos, yPos)
        time.sleep(0.5)

    if log_function_enter_exit:
        log("info", "inputChineseCharsWithLetters end")
        log("info", "\n", raw=True)

    return True


def switchToChineseInput() -> bool:
    """
    切换到中文输入法
    """
    # 鼠标移到电脑底部任务栏的 `搜狗输入法` 图标点击
    pyautogui.moveTo(1745, 1058)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.5)

    # 在弹出的菜单栏中鼠标移到 `中文(简体, 中国)` 菜单项, 点击
    pyautogui.moveRel(0, -365)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(1)


def switchToEngInput() -> bool:
    """
    切换到英文输入法
    """
    # 鼠标移到电脑底部任务栏的 `搜狗输入法` 图标点击
    pyautogui.moveTo(1745, 1058)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.5)

    # 在弹出的菜单栏中鼠标移到 `英语(美国)` 菜单项, 点击
    pyautogui.moveRel(0, -165)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(1)
