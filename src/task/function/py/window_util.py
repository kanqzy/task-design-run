# 窗口工具

import os
import time

from PIL import Image, ImageGrab
import psutil
import pyautogui
import win32con
import win32gui
import win32process
import uiautomation as auto

import util


def getRuningWindowHwnd(**winInfo) -> int:
    """
    获取正在运行的窗口句柄

    动态字典参数:
        winInfo {
            processId (int): 窗口进程ID
            processName (str): 窗口进程名 可打开任务管理器, 找到正在运行的目标窗体应用, 右键转到 详细信息栏, 名称列 即为目标进程名(忽略大小写)
                    例如记事本: `notpad.exe`
            processExePath (str): 进程可执行文件路径
            title (str): 窗口标题(包含匹配)
            className (str): 窗口类名
            isIconic (bool): 窗口是否图标化(窗口缩小到windows的任务栏上)
        }

    返回:
        返回成功查找到的窗口句柄(查找不到返回 `-1`)
    """
    win_processId = winInfo.get("processId")
    win_processName = winInfo.get("processName")
    win_processExePath = winInfo.get("processExePath")
    win_title = winInfo.get("title")
    win_className = winInfo.get("className")
    win_isIconic = winInfo.get("isIconic")

    targetWinHwnd = -1

    def visitWins(hwnd, nouse):
        isWindow = win32gui.IsWindow(hwnd)
        isWindowEnabled = win32gui.IsWindowEnabled(hwnd)
        # 对应windows 任务管理器上的 应用|后台进程(True|False)
        isWindowVisible = win32gui.IsWindowVisible(hwnd)
        # 窗口是否最小化
        isIconic = win32gui.IsIconic(hwnd)

        nonlocal targetWinHwnd
        if targetWinHwnd != -1:
            return
        if not isWindow or not isWindowEnabled or not isWindowVisible:
            return
        if isinstance(win_isIconic, int):
            if isIconic != win_isIconic:
                return

        # 获取窗口句柄对应的PID
        _, winProcessId = win32process.GetWindowThreadProcessId(hwnd)
        if isinstance(win_processId, int):
            if winProcessId != win_processId:
                return

        if isinstance(win_processName, str):
            winProcess = psutil.Process(winProcessId)
            winProcessName = winProcess.name()
            if winProcessName.lower() != win_processName.lower():
                return

        if isinstance(win_processExePath, str):
            winProcess = psutil.Process(winProcessId)
            winProcessExePath = winProcess.exe()
            if not os.path.samefile(winProcessExePath, win_processExePath):
                return

        if isinstance(win_title, str):
            winTitle = win32gui.GetWindowText(hwnd)
            if winTitle.find(win_title) == -1:
                return

        if isinstance(win_className, str):
            winClassName = win32gui.GetClassName(hwnd)
            if winClassName != win_className:
                return

        targetWinHwnd = hwnd

    win32gui.EnumWindows(visitWins, 0)
    return targetWinHwnd


def getRuningWindowInfo(**winInfo) -> dict:
    """
    获取正在运行的窗口信息

    枚举所有窗口, 返回第一个匹配的窗口信息

    动态字典参数:
        winInfo {
            processId (int): 窗口进程ID
            processName (str): 窗口进程名 可打开任务管理器, 找到正在运行的目标窗体应用, 右键转到 详细信息栏, 名称列 即为目标进程名(忽略大小写)
                    例如记事本: `notpad.exe`
            processExePath (str): 进程可执行文件路径
            title (str): 窗口标题(包含匹配)
            className (str): 窗口类名
            isIconic (bool): 窗口是否图标化(窗口缩小到windows的任务栏上)
        }

    返回:
        返回成功查找到的第一个匹配的窗口信息
    """
    win_processId = winInfo.get("processId")
    win_processName = winInfo.get("processName")
    win_processExePath = winInfo.get("processExePath")
    win_title = winInfo.get("title")
    win_className = winInfo.get("className")
    win_isIconic = winInfo.get("isIconic")

    targetWinHwnd = -1
    targetWinInfo = None

    def visitWins(hwnd, nouse):
        isWindow = win32gui.IsWindow(hwnd)
        isWindowEnabled = win32gui.IsWindowEnabled(hwnd)
        # 对应windows 任务管理器上的 应用|后台进程(True|False)
        isWindowVisible = win32gui.IsWindowVisible(hwnd)
        # 窗口是否最小化
        isIconic = win32gui.IsIconic(hwnd)

        nonlocal targetWinHwnd
        if targetWinHwnd != -1:
            return
        if not isWindow or not isWindowEnabled or not isWindowVisible:
            return
        if isinstance(win_isIconic, int):
            if isIconic != win_isIconic:
                return

        # 获取窗口句柄对应的PID
        _, winProcessId = win32process.GetWindowThreadProcessId(hwnd)
        if isinstance(win_processId, int):
            if winProcessId != win_processId:
                return

        winProcess = None
        winProcessName = None
        if isinstance(win_processName, str):
            winProcess = psutil.Process(winProcessId)
            winProcessName = winProcess.name()
            if winProcessName.lower() != win_processName.lower():
                return

        winProcessExePath = None
        if isinstance(win_processExePath, str):
            if winProcess is None:
                winProcess = psutil.Process(winProcessId)
            winProcessExePath = winProcess.exe()
            if not os.path.samefile(winProcessExePath, win_processExePath):
                return

        winTitle = None
        if isinstance(win_title, str):
            winTitle = win32gui.GetWindowText(hwnd)
            if winTitle.find(win_title) == -1:
                return

        winClassName = None
        if isinstance(win_className, str):
            winClassName = win32gui.GetClassName(hwnd)
            if winClassName != win_className:
                return

        targetWinHwnd = hwnd

        if winProcess is None:
            winProcess = psutil.Process(winProcessId)
        if winProcessName is None:
            winProcessName = winProcess.name()
        if winProcessExePath is None:
            winProcessExePath = os.path.abspath(winProcess.exe())
        if winTitle is None:
            winTitle = win32gui.GetWindowText(hwnd)
        if winClassName is None:
            winClassName = win32gui.GetClassName(hwnd)

        targetWinInfo = {
            "processId": winProcessId,
            "processName": winProcessName,
            "processExePath": winProcessExePath,
            "title": winTitle,
            "className": winClassName,
            "isIconic": isIconic,
        }

    win32gui.EnumWindows(visitWins, 0)
    return targetWinInfo


def getAllRuningWindowInfos(**winInfo) -> list[dict]:
    """
    获取正在运行的所有匹配的窗口信息

    枚举所有窗口, 返回所有匹配的窗口信息

    动态字典参数:
        winInfo {
            processId (int): 窗口进程ID
            processName (str): 窗口进程名 可打开任务管理器, 找到正在运行的目标窗体应用, 右键转到 详细信息栏, 名称列 即为目标进程名(忽略大小写)
                    例如记事本: `notpad.exe`
            processExePath (str): 进程可执行文件路径
            title (str): 窗口标题(包含匹配)
            className (str): 窗口类名
            isWindowVisible (int): 窗口是否可见 (0|1)
            isIconic (int): 窗口是否图标化(窗口缩小到windows的任务栏上) (0|1)
            winRect (list[int]): 窗口矩形 [x1,y1,x2,y2]
        }

    返回:
        返回成功查找到的第一个匹配的窗口信息
    """
    win_processId = winInfo.get("processId")
    win_processName = winInfo.get("processName")
    win_processExePath = winInfo.get("processExePath")
    win_title = winInfo.get("title")
    win_className = winInfo.get("className")
    win_isWindowVisible = winInfo.get("isWindowVisible")
    win_isIconic = winInfo.get("isIconic")

    targetWinHwnds = []
    targetWinInfos = []

    def visitWins(hwnd, nouse):
        isWindow = win32gui.IsWindow(hwnd)
        isWindowEnabled = win32gui.IsWindowEnabled(hwnd)
        # print("isWindow: ", isWindow)
        # print("isWindowEnabled: ", isWindowEnabled)
        # 对应windows 任务管理器上的 应用|后台进程(True|False)
        isWindowVisible = win32gui.IsWindowVisible(hwnd)
        # 窗口是否最小化
        isIconic = win32gui.IsIconic(hwnd)

        nonlocal targetWinHwnds
        if hwnd in targetWinHwnds:
            return
        if isWindow != 1 or isWindowEnabled != 1:
            return

        if win_isWindowVisible:
            if isWindowVisible != win_isWindowVisible:
                return
        else:
            # 默认情况下, 只获取窗口可见的句柄
            if isWindowVisible != 1:
                return

        if isinstance(win_isIconic, int):
            if isIconic != win_isIconic:
                return

        # 获取窗口句柄对应的PID
        _, winProcessId = win32process.GetWindowThreadProcessId(hwnd)
        if isinstance(win_processId, int):
            if winProcessId != win_processId:
                return

        winProcess = None
        winProcessName = None
        if isinstance(win_processName, str):
            winProcess = psutil.Process(winProcessId)
            winProcessName = winProcess.name()
            if winProcessName.lower() != win_processName.lower():
                return

        winProcessExePath = None
        if isinstance(win_processExePath, str):
            if winProcess is None:
                winProcess = psutil.Process(winProcessId)
            winProcessExePath = winProcess.exe()
            if not os.path.samefile(winProcessExePath, win_processExePath):
                return

        winTitle = None
        if isinstance(win_title, str):
            winTitle = win32gui.GetWindowText(hwnd)
            if winTitle.find(win_title) == -1:
                return

        winClassName = None
        if isinstance(win_className, str):
            winClassName = win32gui.GetClassName(hwnd)
            if winClassName != win_className:
                return

        targetWinHwnds.append(hwnd)

        if winProcess is None:
            winProcess = psutil.Process(winProcessId)
        if winProcessName is None:
            winProcessName = winProcess.name()
        if winProcessExePath is None:
            winProcessExePath = os.path.abspath(winProcess.exe())
        if winTitle is None:
            winTitle = win32gui.GetWindowText(hwnd)
        if winClassName is None:
            winClassName = win32gui.GetClassName(hwnd)

        winRect = win32gui.GetWindowRect(hwnd)
        winRectSize = [winRect[2] - winRect[0], winRect[3] - winRect[1]]
        targetWinInfo = {
            "hwnd": hwnd,
            "processId": winProcessId,
            "processName": winProcessName,
            "processExePath": winProcessExePath,
            "title": winTitle,
            "className": winClassName,
            "winRect": winRect,
            "winRectSize": winRectSize,
            "isIconic": isIconic,
        }
        targetWinInfos.append(targetWinInfo)

    win32gui.EnumWindows(visitWins, 0)
    return targetWinInfos


def getActiveWindowInfo() -> dict:
    """
    获取当前活动窗口信息
    """
    foregroundWinHwnd = win32gui.GetForegroundWindow()
    # 获取前置窗口矩形区域坐标(左上右下坐标)
    foregroundWinRect = win32gui.GetWindowRect(foregroundWinHwnd)

    isWindow = win32gui.IsWindow(foregroundWinHwnd)
    isWindowEnabled = win32gui.IsWindowEnabled(foregroundWinHwnd)
    # print("isWindow: ", isWindow)
    # print("isWindowEnabled: ", isWindowEnabled)
    # 对应windows 任务管理器上的 应用|后台进程(True|False)
    isWindowVisible = win32gui.IsWindowVisible(foregroundWinHwnd)
    # 窗口是否最小化
    isIconic = win32gui.IsIconic(foregroundWinHwnd)

    _, winProcessId = win32process.GetWindowThreadProcessId(foregroundWinHwnd)
    winProcess = psutil.Process(winProcessId)
    winProcessName = winProcess.name()
    winProcessExePath = winProcess.exe()
    winTitle = win32gui.GetWindowText(foregroundWinHwnd)
    winClassName = win32gui.GetClassName(foregroundWinHwnd)
    winRect = foregroundWinRect
    winRectSize = [winRect[2] - winRect[0], winRect[3] - winRect[1]]

    return {
        "hwnd": foregroundWinHwnd,
        "isWindow": isWindow,
        "isWindowEnabled": isWindowEnabled,
        "isWindowVisible": isWindowVisible,
        "isIconic": isIconic,
        "processId": winProcessId,
        "processName": winProcessName,
        "processExePath": winProcessExePath,
        "title": winTitle,
        "className": winClassName,
        "winRect": winRect,
        "winRectSize": winRectSize,
    }


def waittingForWin(winTitle, winProcessName, waittingTime=3, detectInterval=3):
    """
    等待指定的窗口

    参数:
        winTitle                    窗口标题
        winProcessName              窗口进程名(忽略大小写)
        waittingTime                等待时间(秒) 最高等待5分钟(5*60)
        detectInterval              检测间隔时间(秒)

    返回:
        返回成功等待到的窗口句柄(指定时间内未检测到返回 `-1`)
    """
    if not isinstance(winTitle, str) or winTitle.strip() == "":
        return False
    if not isinstance(winProcessName, str) or winProcessName.strip() == "":
        return False
    if not isinstance(waittingTime, (int, float)):
        waittingTime = 3
    if waittingTime > 5 * 60:
        waittingTime = 5 * 60
    if not isinstance(detectInterval, (int, float)):
        detectInterval = 3

    while waittingTime > 0:
        installWindow = win32gui.FindWindow(None, winTitle)
        if installWindow > 0:
            # 获取窗口句柄对应的PID
            _, winProcessId = win32process.GetWindowThreadProcessId(installWindow)
            winProcess = psutil.Process(winProcessId)
            _winProcessName = winProcess.name()
            if _winProcessName.lower() == winProcessName.lower():
                return installWindow
        time.sleep(detectInterval)
        waittingTime -= detectInterval
    return -1


def waittingTillForegroundWinAppear(
    foregroundWinProcessName, waittingTime=3, detectInterval=3
):
    """
    等待直到指定的前置窗口出现

    参数:
        foregroundWinProcessName    前置窗口进程名(忽略大小写)
        waittingTime                等待时间(秒) 最高等待5分钟(5*60)
        detectInterval              检测间隔时间(秒)

    返回:
        成功等待到指定前置窗口出现返回 `True`
    """
    if (
        not isinstance(foregroundWinProcessName, str)
        or foregroundWinProcessName.strip() == ""
    ):
        return False

    if not isinstance(waittingTime, (int, float)):
        waittingTime = 3
    if waittingTime > 5 * 60:
        waittingTime = 5 * 60
    if not isinstance(detectInterval, (int, float)):
        detectInterval = 3

    while waittingTime > 0:
        foregroundWinHwnd = win32gui.GetForegroundWindow()
        _, winProcessId = win32process.GetWindowThreadProcessId(foregroundWinHwnd)
        winProcess = psutil.Process(winProcessId)
        winProcessName = winProcess.name()
        if winProcessName.lower() == foregroundWinProcessName.lower():
            return True
        time.sleep(detectInterval)
        waittingTime -= detectInterval
    return False


def capture_screen_region(screen_region: list[int] | tuple[int], outPath: str) -> bool:
    if not util.isValidFilePath(outPath):
        return False

    x1, y1, x2, y2 = screen_region
    screenshot_region = (x1, y1, x2 - x1, y2 - y1)
    screenshot_image = pyautogui.screenshot(region=screenshot_region)

    screenshot_image.save(outPath)

    if util.isFile(outPath):
        return True

    return False


def capture_full_screen(outPath: str) -> bool:
    if not util.isValidFilePath(outPath):
        return False

    screenshot_image = pyautogui.screenshot()

    screenshot_image.save(outPath)

    if util.isFile(outPath):
        return True

    return False


def capture_active_window(outPath: str, foregroundWinHwnd: int = None) -> bool:
    """
    活动窗口可以是肉眼可见的窗口也可以是该窗口下的子控件, 调用前, 请结合具体使用场景, 谨慎调用.
    通常点击某个快捷方式或者任务栏底部按钮, 弹出一个窗口后, 调用当前方法是合理的。
    然而一些特殊场景, 截屏的活动窗口可能不是你想要的图像, 比如, 你点击 桌面 `腾讯QQ` 快捷方式,
    会弹出QQ登录窗口, 同时鼠标光标会聚焦 密码输入框, 此时截屏的活动窗口, 可能是密码框所在的控件区域, 该区域
    是由QQ桌面应用程序的开发者所定义的, 它一定不是你所看见的整个QQ登录窗口区域.
    此时, 你要想截屏整个QQ登录窗口区域, 你需要将鼠标移到 窗口的 `QQ` logo图标上点击一下, 然后在调用当前方法,
    其截屏才会符合你的预期。
    """
    if not isinstance(foregroundWinHwnd, int):
        foregroundWinHwnd = win32gui.GetForegroundWindow()
    # 获取前置窗口矩形区域坐标(左上右下坐标)
    foregroundWinRect = win32gui.GetWindowRect(foregroundWinHwnd)
    print("foregroundWinRect: ", foregroundWinRect)

    return capture_screen_region(foregroundWinRect, outPath)


def capture_active_window_by_altPrintScreen(outPath: str) -> bool:
    """
    通过截屏快捷键 `alt+printscreen` 捕获活动窗口图像
    """
    if not util.isValidFilePath(outPath):
        return False

    pyautogui.hotkey("alt", "printscreen")
    time.sleep(0.5)
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        im.save(outPath)
        return util.isFile(outPath)

    else:
        print("clipboard has no img")
        return False


def minimize_active_window():
    """
    最小化活动窗口
    """
    foregroundWinHwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(foregroundWinHwnd, win32con.SW_MINIMIZE)
