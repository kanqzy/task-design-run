# QQ应用程序上操作函数库

import os
import shutil
import time

import psutil
import pyautogui
import uiautomation as auto
import win32gui
import win32process

import log
import logger

import common
import image_util
import window_util

import common_util
from debug import tprint
import log
import logger


Log_Formatter = {
    "formatter": log.Empty_Logging_Formatter,
    "msgFormat": "{asctime} function_library[qq] => {message}",
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


# 截屏图像比对设置
# compare_img_dir = os.path.abspath("../in/images/QQ")
compare_img_dir = os.path.abspath(
    r"D:\holiday\suck\Agent\examples\task-design-demo\in\images\QQ"
)

# capture_img_path = os.path.abspath("../out/temp/qq_win_capture.png")
capture_img_path = os.path.abspath(
    r"D:\holiday\suck\Agent\examples\task-design-demo\out\temp\qq_win_capture.png"
)


def __detect_screen_qq_window(compare_img_path: str, winInfo: dict = None) -> dict:
    """
    探测屏幕特定的QQ窗口

    探测过程:
        调用 `win32gui` 枚举当前电脑上所有匹配参数 `winInfo`的窗口,
        并截屏窗口, 然后若检测该截屏包含子图像 `compare_img_path`, 则直接返回窗口信息.
        枚举不到匹配的窗口返回 `None`

    返回:
        {
            hwnd (int): 窗口句柄
            processId (int): 窗口进程ID
            processName (str): 窗口进程名 可打开任务管理器, 找到正在运行的目标窗体应用, 右键转到 详细信息栏, 名称列 即为目标进程名(忽略大小写)
                    例如记事本: `notpad.exe`
            processExePath (str): 进程可执行文件路径
            title (str): 窗口标题(包含匹配)
            className (str): 窗口类名
            isIconic (bool): 窗口是否图标化(窗口缩小到windows的任务栏上)
            winRect (list[int]): 窗口矩形区域 [x1,y1,x2,y2]
            winRectSize (list[int]): 窗口矩形大小 [w,h]
        }
    """
    if not isinstance(winInfo, dict):
        winInfo = {"processName": "QQ.exe"}
    elif "processName" not in winInfo.keys():
        winInfo["processName"] = "QQ.exe"

    runingWindowInfos = window_util.getAllRuningWindowInfos(**winInfo)
    for runingWindowInfo in runingWindowInfos:
        isAllMatch = True
        for key, value in winInfo.items():
            if runingWindowInfo[key] != value:
                isAllMatch = False
                break

        if isAllMatch:
            winRect = runingWindowInfo["winRect"]
            window_util.capture_screen_region(winRect, capture_img_path)
            check_result = image_util.check_isSubImage(
                compare_img_path, capture_img_path
            )
            if check_result["isSubImage"]:
                log(
                    "info",
                    "success detected runingWindowInfo `{0}` for compare_img_path `{1}` and winInfo `{2}`".format(
                        runingWindowInfo, compare_img_path, winInfo
                    ),
                )
                return runingWindowInfo

    return None


def __detect_screen_qq_window_subImage_locations(
    *compare_img_paths, winInfo: dict = None
) -> dict:
    """
    探测屏幕特定的QQ窗口子标记图像位置

    探测过程:
        调用 `win32gui` 枚举当前电脑上所有匹配参数 `winInfo`的窗口,
        并截屏窗口, 然后若检测该截屏包含子图像 `compare_img_path`, 则直接返回窗口信息.
        枚举不到匹配的窗口返回 `None`

    返回:
        {
            // 是否检测到含有这些子图像的QQ窗口
            detected: bool,
            detected_winInfo: {
                hwnd (int): 窗口句柄
                processId (int): 窗口进程ID
                processName (str): 窗口进程名 可打开任务管理器, 找到正在运行的目标窗体应用, 右键转到 详细信息栏, 名称列 即为目标进程名(忽略大小写)
                        例如记事本: `notpad.exe`
                processExePath (str): 进程可执行文件路径
                title (str): 窗口标题(包含匹配)
                className (str): 窗口类名
                isIconic (bool): 窗口是否图标化(窗口缩小到windows的任务栏上)
                winRect (list[int]): 窗口矩形区域 [x1,y1,x2,y2]
                winRectSize (list[int]): 窗口矩形大小 [w,h]
            },
            // 探测的子图像位置, 与传入的比较图像的顺序一致
            detected_subImage_locations: [x1,y1,x2,y2][]
        }
    """
    if len(compare_img_paths) < 0:
        return {"detected": False}
    if not isinstance(winInfo, dict):
        winInfo = {"processName": "QQ.exe"}
    elif "processName" not in winInfo.keys():
        winInfo["processName"] = "QQ.exe"

    runingWindowInfos = window_util.getAllRuningWindowInfos(**winInfo)
    for runingWindowInfo in runingWindowInfos:
        isAllMatch = True
        for key, value in winInfo.items():
            if runingWindowInfo[key] != value:
                isAllMatch = False
                break

        if isAllMatch:
            winRect = runingWindowInfo["winRect"]
            tprint("")
            window_util.capture_screen_region(winRect, capture_img_path)
            subImageLocations = []
            for compare_img_path in compare_img_paths:
                subImageLocation = image_util.findSubImageLocation(
                    capture_img_path, compare_img_path
                )
                if subImageLocation is None:
                    break
                else:
                    a, b, c, d = winRect
                    x1, y1, x2, y2 = subImageLocation
                    subImage_fullscreen_location = [x1 + a, y1 + b, x2 + a, y2 + b]
                    subImageLocations.append(subImage_fullscreen_location)

            if len(subImageLocations) > 0:
                return {
                    "detected": True,
                    "detected_winInfo": runingWindowInfo,
                    "detected_subImage_locations": subImageLocations,
                }

    return {"detected": False}


def __check_is_foreground_qq_window(
    compare_img_path: str, winInfo: dict = None
) -> dict:
    """
    检测前置窗口是否是QQ窗口

    检测过程:
        调用 `win32gui` 枚举当前电脑上所有匹配参数 `winInfo`的窗口,
        并截屏窗口, 然后若检测该截屏包含子图像 `compare_img_path`, 则直接返回窗口信息.
        枚举不到匹配的窗口返回 `None`

    返回:
        {
            // 前置窗口是否是QQ窗口
            isQQForegroundWin: bool,
            // 窗口信息
            winInfo: {
                hwnd (int): 窗口句柄
                processId (int): 窗口进程ID
                processName (str): 窗口进程名 可打开任务管理器, 找到正在运行的目标窗体应用, 右键转到 详细信息栏, 名称列 即为目标进程名(忽略大小写)
                        例如记事本: `notpad.exe`
                processExePath (str): 进程可执行文件路径
                title (str): 窗口标题(包含匹配)
                className (str): 窗口类名
                isIconic (bool): 窗口是否图标化(窗口缩小到windows的任务栏上)
                winRect (list[int]): 窗口矩形区域 [x1,y1,x2,y2]
                winRectSize (list[int]): 窗口矩形大小 [w,h]
            }
        }
    """
    if not isinstance(winInfo, dict):
        winInfo = {"processName": "QQ.exe"}
    elif "processName" not in winInfo.keys():
        winInfo["processName"] = "QQ.exe"

    activeWindowInfo = window_util.getActiveWindowInfo()
    isAllMatch = True
    for key, value in winInfo.items():
        if activeWindowInfo[key] != value:
            isAllMatch = False
            break

    if not isAllMatch:
        return {"isQQForegroundWin": False}

    window_util.capture_screen_region(activeWindowInfo["winRect"], capture_img_path)
    check_result = image_util.check_isSubImage(compare_img_path, capture_img_path)
    if check_result["isSubImage"]:
        # os.remove(capture_img_path)
        return {"isQQForegroundWin": True, "winInfo": activeWindowInfo}

    return {"isQQForegroundWin": False}


def __find_marked_pos_info(compare_img_marked_path: str) -> dict:
    """
    在全屏幕中找到与给定标记图像匹配的坐标位置信息

    返回:
        {
            "located": bool,
            "locate_rect": [x1,y1,x2,y2],
            "locate_rect_size": [w, h],
            "locate_centerPos": [xCenterPos, yCenterPos],
        }
    """
    window_util.capture_full_screen(capture_img_path)
    subImageLocation = image_util.findSubImageLocation(
        capture_img_path, compare_img_marked_path
    )
    if subImageLocation:
        x1, y1, x2, y2 = subImageLocation
        w, h = x2 - x1, y2 - y1
        xCenterPos = x1 + w // 2
        yCenterPos = y1 + h // 2

        return {
            "located": True,
            "locate_rect": subImageLocation,
            "locate_rect_size": [w, h],
            "locate_centerPos": [xCenterPos, yCenterPos],
        }

    return {"located": False}


def waittingForLoginAppear(waittingTimeLimit: int = 8) -> dict:
    """
    等待QQ登录窗口出现

    可选参数:
        waittingTimeLimit (int): 等待时间限制(秒)

    返回:
        {
            // 是否在指定时间内等到到登录窗口出现
            appear: bool,
            // 窗口矩形
            winRect: [x1,y1,x2,y2]
        }
    """
    compare_img_path = os.path.join(compare_img_dir, "login_qrcode_mark.png")

    count = 1
    while count < waittingTimeLimit:
        if count <= 3:
            time.sleep(1)
        else:
            time.sleep(0.5)
            detected_win = __detect_screen_qq_window(
                compare_img_path, {"title": "QQ", "className": "TXGuiFoundation"}
            )
            if detected_win:
                return {"appear": True, "winRect": detected_win["winRect"]}
            else:
                time.sleep(0.4)
        count += 1

    return {"appear": False}


def select_qq_number_input(loginWinRect: list[int], qqNumber: int) -> bool:
    """
    选择指定QQ账号输入

    参数:
        loginWinRect (list[int]): QQ登录窗口矩形区域 [x1,y1,x2,y2]
        qqNumber (int): 输入的QQ号

    选择输入过程:
        不断的点击输入框右侧的下拉箭头, 在下拉项中一个个尝试是否与给定的QQ号匹配

    返回:
        成功选择指定QQ账号进行了输入, 返回 `True`
    """
    tprint("into select_qq_number_input ...")
    time.sleep(0.5)
    compare_img_path = os.path.join(
        compare_img_dir, "login_account_{0}.png".format(qqNumber)
    )
    if image_util.check_screen_window_match(loginWinRect, compare_img_path):
        log("info", "current account is right, not need for click select input")
        return True
    tprint("compare_img_path: ", compare_img_path)

    # 找到账号输入框右侧的 `向下箭头`位置
    loginInputSelect_mark_img_path = os.path.join(
        compare_img_dir, "login_input_select_mark.png"
    )
    loginInputSelect_posInfo = __find_marked_pos_info(loginInputSelect_mark_img_path)
    if not loginInputSelect_posInfo["located"]:
        log("err", "failed find loginInputSelect pos")
        return False

    x1, y1, x2, y2 = loginInputSelect_posInfo["locate_rect"]
    x = x1 + (x2 - x1) // 2
    y = y1 + 20
    log("info", "locate login_input_select pos: [{0}, {1}]", x, y)

    count = 1
    while count <= 5:
        # 鼠标移到账号输入框右侧的 `向下箭头`点击
        pyautogui.moveTo(x, y)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)

        # 发送 `down` 下移下拉选项后截屏
        pyautogui.press("down")
        time.sleep(0.5)
        pyautogui.hotkey("enter")
        time.sleep(0.5)

        if image_util.check_screen_window_match(loginWinRect, compare_img_path):
            return True

        time.sleep(0.5)
        count += 1

    log("warn", "failed select right qq_number for input in 5 times")

    return False


def __loopDeepExtractTaskbarQQButtonData(
    control: auto.Control, extractControlDatas: list[dict]
):
    """
    循环深度递归抽取任务栏上QQ按钮数据
    """
    if control.Name.startswith("QQ") and control.LocalizedControlType == "按钮":
        boundingRectangle = control.GetPropertyValue(
            auto.PropertyId.BoundingRectangleProperty
        )
        boundingRectangle_list = list(boundingRectangle)
        common_util.numberToIntList(boundingRectangle_list)

        # 绑定的矩形区域[x1,y1,x2,y2]
        boundingRect = [
            boundingRectangle_list[0],
            boundingRectangle_list[1],
            boundingRectangle_list[0] + boundingRectangle_list[2],
            boundingRectangle_list[1] + boundingRectangle_list[3],
        ]
        boundingRectSize = [boundingRectangle_list[2], boundingRectangle_list[3]]

        extractControlData = {
            "name": control.Name,
            "localizedControlType": control.LocalizedControlType,
            "boundingRect": boundingRect,
            "boundingRectSize": boundingRectSize,
        }
        extractControlDatas.append(extractControlData)

    children = control.GetChildren()
    hasChildren = isinstance(children, list) and len(children) > 0

    if hasChildren:
        for index in range(len(children)):
            child_control = children[index]
            __loopDeepExtractTaskbarQQButtonData(child_control, extractControlDatas)


def recognize_taskbar_qq_button_datas() -> list[dict]:
    """
    识别windows任务栏上QQ按钮数据

    在实际识别过程中会调用 `UIAutomation` 库识别windows gui中的组件元素,
    实际识别过程中, 若识别的数据不符合数据格式, 直接返回 `[]`

    返回:
        [
            {
                "name": control.Name,
                "localizedControlType": control.LocalizedControlType,
                "boundingRect": boundingRect,
                "boundingRectSize": boundingRectSize,
            },
            ...
        ]
    """
    if log_function_enter_exit:
        log("info", "into recognize_taskbar_qq_button_data ...")

    taskbar_paneControl = auto.PaneControl(
        searchDepth=1,
        ControlType=auto.ControlType.PaneControl,
        Name="任务栏",
    )

    qq_button_datas = []
    __loopDeepExtractTaskbarQQButtonData(taskbar_paneControl, qq_button_datas)

    log("info", "以成功识别任务栏上QQ按钮数据 => `{0}`".format(qq_button_datas))

    if log_function_enter_exit:
        log("info", "recognize_taskbar_qq_button_data end")
        log("info", "\n", raw=True)

    return qq_button_datas


def check_qq_logined(qqNumber: int) -> bool:
    """
    检测指定的QQ号是否已登录

    检测过程:
        首先, 检测当前桌面窗口, 若匹配该QQ联系人主窗口, 则聚焦然后返回 `True`;
        接着, 检测依次点击电脑底部任务栏QQ图标按钮, 每次点击后检测弹出的窗口是否与该QQ号匹配,
            若不匹配, 则将其最小化,然后继续下一个QQ图标按钮检测,...,直到检测完所有, 返回检测结果

    注意:
        以上检测不会检测QQ图标隐藏在任务栏里

    返回:
        该QQ号是否已登录
    """
    # 首先, 检测可见窗口是否有该QQ号的窗口
    compare_img_path = os.path.join(
        compare_img_dir, "contanct_home_top_{0}.png".format(qqNumber)
    )
    detected_win = __detect_screen_qq_window(compare_img_path)
    if detected_win:
        log("info", "detected contact home window directly on the screen")
        return True

    # 接着, 依次检测任务栏QQ按钮
    taskbar_qq_button_datas = recognize_taskbar_qq_button_datas()
    for taskbar_qq_button_data in taskbar_qq_button_datas:
        x1, y1, x2, y2 = taskbar_qq_button_data["boundingRect"]
        xCenterPos = x1 + (x2 - x1) // 2
        yCenterPos = y1 + (y2 - y1) // 2
        pyautogui.moveTo(xCenterPos, yCenterPos)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(1)

        window_util.capture_active_window(capture_img_path)
        check_result = image_util.check_isSubImage(compare_img_path, capture_img_path)
        if check_result["isSubImage"]:
            # os.remove(capture_img_path)
            return True
        else:
            window_util.minimize_active_window()
            time.sleep(1)

    log("info", "not detected qqNumber `{0}` logined", qqNumber)

    return False


def waittingForContactHomeAppear(qqNumber: int, waittingTimeLimit=10) -> dict:
    """
    等待直到QQ联系人主窗口出现

    通常会在登录窗口点击 `登录` 后调用当前方法, 等待联系人主窗口出现, 出现后表明登录成功

    参数:
        qqNumber (int): 点击 `登录` 时的QQ号

    可选参数:
        waittingTimeLimit (int): 等待时间限制(秒)

    返回:
        {
            // 是否在指定时间内等到联系人主窗口出现
            appear: bool,
            // 窗口矩形
            winRect: [x1,y1,x2,y2]
        }
    """
    if not isinstance(waittingTimeLimit, int) or waittingTimeLimit < 1:
        waittingTimeLimit = 10

    compare_img_path = os.path.join(
        compare_img_dir, "contanct_home_top_{0}.png".format(qqNumber)
    )
    count = 1
    while count < waittingTimeLimit:
        if count <= 3:
            time.sleep(1)
        else:
            time.sleep(0.5)
            checkResult = __check_is_foreground_qq_window(
                compare_img_path,
            )
            if checkResult["isQQForegroundWin"]:
                return {"appear": True, "winRect": checkResult["winInfo"]["winRect"]}
            else:
                time.sleep(0.4)

        count += 1

    log("warn", "fail detected QQ `{0}` contactHome window appear".format(qqNumber))
    return {"appear": False}


def get_searchPrompt_centerPos() -> list[int]:
    """
    获取搜索框中的 `搜索` 提示 中心位置坐标

    常见于联系人主窗口搜索框输入文字

    返回:
        返回成功获取的位置, 获取失败返回 `None`
    """
    compare_img_path = os.path.join(compare_img_dir, "search_mark.png")
    marked_pos_info = __find_marked_pos_info(compare_img_path)
    if marked_pos_info["located"]:
        return marked_pos_info["locate_centerPos"]
    return None


def get_searchIcon_centerPos() -> list[int]:
    """
    获取搜索框中的 `搜索` 图标 中心位置坐标

    常见于联系人主窗口搜索框输入文字

    返回:
        返回成功获取的位置, 获取失败返回 `None`
    """
    compare_img_path = os.path.join(compare_img_dir, "search_icon_mark.png")
    marked_pos_info = __find_marked_pos_info(compare_img_path)
    if marked_pos_info["located"]:
        return marked_pos_info["locate_centerPos"]
    return None


def get_searchFirstViewInfo_centerPos() -> list[int]:
    """
    获取搜索的第一个联系人 `查看资料`  中心位置坐标

    常见于联系人主窗口所属指定联系人定位

    返回:
        返回成功获取的位置, 获取失败返回 `None`
    """
    compare_img_path = os.path.join(compare_img_dir, "search_first_view info_mark.png")
    marked_pos_info = __find_marked_pos_info(compare_img_path)
    if marked_pos_info["located"]:
        return marked_pos_info["locate_centerPos"]
    return None


def get_searchFirstOpenChatWindow_centerPos() -> list[int]:
    """
    获取搜索的第一个联系人 `打开回话窗口`  中心位置坐标

    常见于联系人主窗口所属指定联系人定位

    返回:
        返回成功获取的位置, 获取失败返回 `None`
    """
    compare_img_path = os.path.join(compare_img_dir, "open_chat_window.png")
    marked_pos_info = __find_marked_pos_info(compare_img_path)
    if marked_pos_info["located"]:
        return marked_pos_info["locate_centerPos"]
    return None


def foucus_search_text() -> bool:
    """
    聚焦联系人主页搜索文本

    通过点击联系人主页 `清除搜索输入框` 按钮左侧20px空白处, 聚焦搜索文本

    返回:
        成功找到 `清除搜索输入框` 按钮位置, 点击聚焦, 返回 `True`
    """
    compare_img_path = os.path.join(compare_img_dir, "search_clear_mark.png")
    tprint("compare_img_path: ", compare_img_path)
    marked_pos_info = __find_marked_pos_info(compare_img_path)
    tprint("marked_pos_info: ", marked_pos_info)
    if marked_pos_info["located"]:
        x1, y1, x2, y2 = marked_pos_info["locate_rect"]
        w, h = marked_pos_info["locate_rect_size"]
        target_xPos = x1 - 20
        target_yPos = y1 + h // 2
        time.sleep(1)
        pyautogui.moveTo(target_xPos, target_yPos)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)

        return True

    return False


def foucus_chat_window_sendMessage(message: str) -> bool:
    """
    将鼠标光标聚焦聊天窗口, 并发送消息

    聚焦发送消息过程:
        首先, 在当前电脑屏幕上找到所有的QQ窗口, 找到其中包含 输入框 `微笑` 表情,  `发送` 按钮图像的那个窗口,
        接着, 若检测该窗口上面是否悬浮有 `消息漫游安全验证` 模态框, 如果有, 则将其关闭
        然后, 在 `微笑` 表情下面 20px像素处, 点击一下, 开始输入消息内容
        最后, 点击 `发送`, 并截屏当前屏幕, 记录发送结果

    返回:
        成功聚焦并发送消息, 返回 `True`
    """
    compare_img_path_send = os.path.join(compare_img_dir, "chat_send.png")
    compare_img_path_emoji = os.path.join(compare_img_dir, "chat_chat_emoji.png")
    compare_img_path_roam = os.path.join(
        compare_img_dir, "message_roam_security_auth_mark.png"
    )

    detect_result = __detect_screen_qq_window_subImage_locations(
        compare_img_path_send, compare_img_path_emoji
    )
    if not detect_result["detected"]:
        log("warn", "failed detect screen chat window")
        return False
    detected_subImage_locations = detect_result["detected_subImage_locations"]
    tprint("detected_subImage_locations: ", detected_subImage_locations)

    # 如果聊天窗口有 "漫游" 窗口悬浮遮挡, 则点击 `x` 取消遮挡悬浮框
    location_roam = image_util.findScreenSubImageLocation(compare_img_path_roam)
    if location_roam:
        x1, y1, x2, y2 = location_roam
        w, h = x2 - x1, y2 - y1
        target_xPos = x2 - 20
        target_yPos = y2 - w // 2

        time.sleep(0.5)
        pyautogui.moveTo(target_xPos, target_yPos)

    else:
        location_emoji = detected_subImage_locations[1]
        x1, y1, x2, y2 = location_emoji
        w, h = x2 - x1, y2 - y1
        target_xPos = x1 + w // 2
        target_yPos = y2 + 20

        time.sleep(0.5)
        pyautogui.moveTo(target_xPos, target_yPos)
        time.sleep(0.5)
        pyautogui.click()

    pyautogui.typewrite(message)
    time.sleep(1)

    location_send = detected_subImage_locations[0]
    x1, y1, x2, y2 = location_send
    w, h = x2 - x1, y2 - y1
    target_xPos = x1 + w // 2
    target_yPos = y1 + h // 2

    time.sleep(0.5)
    pyautogui.moveTo(target_xPos, target_yPos)
    time.sleep(0.5)
    pyautogui.click()

    return True


def foucus_friendInfo_window_and_draw_left() -> bool:
    """
    将鼠标光标聚焦好友资料窗口并将其向左拖拽

    在实际聚焦中, 会在当前电脑屏幕上找到所有的QQ窗口, 找到其中包含 `备注` 按钮图像的那个窗口,
    认定为好友信息窗口, 然后点击窗口顶部中间位置不释放向左拖拽50-100px保证当前窗口不被主窗口遮盖,
    """
    compare_img_path = os.path.join(compare_img_dir, "friendInfo_nickname.png")
    detected_qq_win = __detect_screen_qq_window(compare_img_path)
    if detected_qq_win:
        hwnd = detected_qq_win["hwnd"]
        winRect = detected_qq_win["winRect"]
        x1, y1, x2, y2 = winRect
        w, h = x2 - x1, y2 - y1
        win32gui.SetActiveWindow(hwnd)
        win32gui.MoveWindow(hwnd, 60, 60, w, h, True)
        time.sleep(1)

        return True

    log("warn", "fail detected friendInfo_window")
    return False


def __loopDeepExtractQQFriendControlData(
    control: auto.Control, extractControlData: dict
):
    """
    循环深度递归抽取QQ好友控件信息数据
    """
    # 抽取窗口上的QQ账号, 昵称, 备注等
    if control.Name == "帐号":
        qqNumber: str = control.GetPropertyValue(
            auto.PropertyId.LegacyIAccessibleValueProperty
        )
        extractControlData["qqNumber"] = int(qqNumber)

    elif control.Name == "昵称" and control.LocalizedControlType == "编辑":
        nickname: str = control.GetPropertyValue(
            auto.PropertyId.LegacyIAccessibleValueProperty
        )
        extractControlData["nickname"] = nickname

    elif control.Name == "备注" and control.LocalizedControlType == "编辑":
        remarkName: str = control.GetPropertyValue(
            auto.PropertyId.LegacyIAccessibleValueProperty
        )
        extractControlData["remarkName"] = remarkName

    elif control.Name == "分组" and control.LocalizedControlType == "文本":
        nextSiblingControl: auto.Control = control.GetNextSiblingControl()
        if nextSiblingControl.LocalizedControlType == "按钮":
            groupName = nextSiblingControl.Name
            extractControlData["groupName"] = groupName

    elif control.Name == "性别":
        sex: str = control.GetPropertyValue(
            auto.PropertyId.LegacyIAccessibleValueProperty
        )
        extractControlData["sex"] = sex

    elif control.Name == "年龄":
        age: str = control.GetPropertyValue(
            auto.PropertyId.LegacyIAccessibleValueProperty
        )
        extractControlData["age"] = age

    elif control.Name == "所在地" and control.LocalizedControlType == "编辑":
        location: str = control.GetPropertyValue(
            auto.PropertyId.LegacyIAccessibleValueProperty
        )
        extractControlData["location"] = location

    elif control.Name == "Q龄":
        qqAge: str = control.GetPropertyValue(
            auto.PropertyId.LegacyIAccessibleValueProperty
        )
        extractControlData["qqAge"] = qqAge

    children = control.GetChildren()
    hasChildren = isinstance(children, list) and len(children) > 0

    if hasChildren:
        for index in range(len(children)):
            child_control = children[index]
            __loopDeepExtractQQFriendControlData(child_control, extractControlData)


def recognize_friendInfo_window_data() -> dict:
    """
    识别好友信息窗口数据

    在实际识别过程中会调用 `UIAutomation` 库识别windows gui中的组件元素,
    实际识别过程中, 若识别的数据不符合 好友信息窗口数据的数据格式, 直接返回 `None`
    """
    if log_function_enter_exit:
        log("info", "into recognize_friendInfo_window_data ...")

    qq_friendInfo_winControl = auto.WindowControl(
        searchDepth=1,
        ControlType=auto.ControlType.WindowControl,
        ClassName="TXGuiFoundation",
        RegexName=r".*的资料.*",
    )

    qq_friendInfo_data = {}
    __loopDeepExtractQQFriendControlData(qq_friendInfo_winControl, qq_friendInfo_data)

    log("info", "以成功识别好友信息窗口数据 => `{0}`".format(qq_friendInfo_data))

    if log_function_enter_exit:
        log("info", "recognize_friendInfo_window_data end")
        log("info", "\n", raw=True)

    return qq_friendInfo_data
