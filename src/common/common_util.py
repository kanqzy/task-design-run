# 公共模块
# 一些常用的公共函数, 方法，类

import os
import re
import time

import psutil
import win32gui
import win32process

import util


# str
def getIndent(indent: int = 2) -> str:
    """
    获取缩进的空格字符串
    """
    indentSpaceCount = indent * 2
    spaceStr = ""
    for i in range(indentSpaceCount):
        spaceStr += " "
    return spaceStr


def unicode_escape(unicode_string: str):
    """
    将unicode转换为字符串

    例如:
        '\u4f60\u597d' => 你好
    """
    if unicode_string and unicode_string.find(r"\u") != -1:
        encoded_string = unicode_string.encode("unicode_escape")
        decoded_string = encoded_string.decode("unicode_escape")
        return decoded_string
    return unicode_string


# list, tuple


def numberToIntList(numberList):
    """
    数字列表转为整形列表
    """
    if not isinstance(numberList, list) or len(numberList) == 0:
        return numberList
    for index in range(len(numberList)):
        numberElement = numberList[index]
        intValue = int(numberElement)
        numberList[index] = intValue


def numberListToString(numberList: list, separator=",", keepSpace=False) -> str:
    numberListLen = len(numberList)
    if numberListLen == 0:
        return "[]"
    strs = ""
    strs += "["
    i = 0
    while i < numberListLen:
        string = numberList[i]
        if i < numberListLen - 1:
            string += separator
            if keepSpace:
                string += " "
        strs += string
        i += 1
    strs += "]"
    return strs


def getIntTuple(numberTuple):
    """
    根据数字元组获取整形元组
    """
    if not isinstance(numberTuple, tuple) or len(tuple) == 0:
        return None

    numberList = list(numberTuple)
    for index in range(len(numberList)):
        numberElement = numberList[index]
        intValue = int(numberElement)
        numberList[index] = intValue
    return tuple(numberList)


def getIntList(numberTuple):
    """
    根据数字元组获取整形列表
    """
    if not isinstance(numberTuple, tuple) or len(tuple) == 0:
        return None

    numberList = list(numberTuple)
    for index in range(len(numberList)):
        numberElement = numberList[index]
        intValue = int(numberElement)
        numberList[index] = intValue
    return numberList


def parseAsNumberList(
    strs: str, wrappedWith=None, separator=",", strictParse=False
) -> list:
    """
    将字符串中解析为数字列表
        字符串必须是这种格式 `[(number1,...,numberN)]` 才能解析

    可选参数:
        wrappedWith (str): 要解析的字符串首尾被包裹的字符串.
            必须是长度为2的对称字符串, 例如: `()` 或 `[]`.
            默认为 `None` 表示首尾未被某个对称字符串包裹
        separator (str): 分隔符
        strictParse (bool): 是否按严格模式解析
            为 `True` 时, 会按照正常数字列表的字符串模式解析, 遇到不合法的字符直接返回 `None`;
            反之, 则会忽略不合法的字符, 继续向后解析

    返回:
        返回成功解析的数字列表, 解析失败返回 `None`
    """
    if not strs:
        return None
    strs = strs.strip()
    if not strs:
        return None

    if wrappedWith and len(wrappedWith) == 2:
        if not strs.startswith(wrappedWith[0]) or not strs.endswith(wrappedWith[1]):
            return None
        strs = strs[1, len(strs)]

    if not strs:
        return True, []
    separatorPattern = separator
    if separator == ",":
        separatorPattern = r"\,"
    strArray = re.split(r"\s*{0}\s*".format(separatorPattern), strs)
    numberList = []
    for strElement in strArray:
        if util.isInt(strElement):
            numberList.append(int(strElement))
        elif util.isFloat(strElement):
            numberList.append(float(strElement))
        else:
            if strictParse:
                return None
    return numberList


# dict


def getMatchElement(dictList, targetDict):
    """
    获取字典列表 `dictList` 中与 目标字典 `targetDict`匹配的元素
        匹配规则, 从前往后遍历`dictList, 如果 `targetDict` 中的所有键值对均与 遍历的字典相等, 则视为匹配
    """
    if not util.isNonEmptyDict(targetDict):
        return None
    if not isinstance(dictList, list):
        return None
    dictListLen = len(dictList)
    if dictListLen == 0:
        return None
    for dictElement in dictList:
        isMatch = True
        for key, value in targetDict.items():
            if dictElement.get(key) != value:
                isMatch = False
                break
        if isMatch:
            return dictElement
    return None


def getMatchElements(dictList, targetDict):
    """
    获取字典列表 `dictList` 中与 目标字典 `targetDict`匹配的所有元素
        匹配规则, 从前往后遍历`dictList, 如果 `targetDict` 中的所有键值对均与 遍历的字典相等, 则视为匹配
    """
    if not util.isNonEmptyDict(targetDict):
        return None
    if not isinstance(dictList, list):
        return None
    dictListLen = len(dictList)
    if dictListLen == 0:
        return None
    matchElements = []
    for dictElement in dictList:
        isMatch = True
        for key, value in targetDict.items():
            if dictElement.get(key) != value:
                isMatch = False
                break
        if isMatch:
            matchElements.append(dictElement)
    return matchElements


def copyDict(dictData, copyType=0, keys=[]):
    """
    将字典数据复制一份
        复制时, 会重新创建一个字典, 并将需要复制的键的值指向源键值

    参数:
        dictData        字典数据
        copyType        复制方式: 全部复制(0), 包含复制(1), 排除复制(2)
        keys            包含或排除的键
    """
    if not isinstance(dictData, dict):
        return None
    if len(dictData.keys()) == 0:
        return {}

    if not isinstance(keys, list):
        keys = []

    newDict = {}
    if copyType == 1:
        for key, value in dictData.items():
            if key in keys:
                newDict[key] = value

    elif copyType == 2:
        for key, value in dictData.items():
            if key not in keys:
                newDict[key] = value

    else:
        for key, value in dictData.items():
            newDict[key] = value

    return newDict


# windows


def waittingForegroundWindow(
    winTitle=None,
    winProcessId=None,
    winProcessName=None,
    winProcessExcutePath=None,
    waittingTime=3,
    detectInterval=3,
):
    """
    windows系统下等待指定的前置窗口

    参数:
        winTitle                    窗口标题(包含匹配)    例如: 记事本为 `无标题 - 记事本`
        winProcessId                窗口进程id
        winProcessName              窗口进程名(忽略大小写) 例如: 记事本为 `notepad.exe`
        winProcessExcutePath        窗口进程可执行文件路径 例如: 记事本为 `C:\Windows\system32\notepad.exe`
        waittingTime                等待时间(秒) 最高等待5分钟(5*60)
        detectInterval              检测间隔时间(秒)

    返回:
        返回等待到的指定窗口句柄, 等待失败或未等待到指定窗口出现返回 -1
    """
    is_winTitle_valid = isinstance(winTitle, str) and winTitle.strip() != ""
    is_winProcessId_valid = isinstance(winProcessId, int) and winProcessId >= 0
    is_winProcessName_valid = (
        isinstance(winProcessName, str) and winProcessName.strip() != ""
    )
    is_winProcessExcutePath_valid = (
        isinstance(winProcessExcutePath, str) and winProcessExcutePath.strip() != ""
    )

    if not (
        is_winTitle_valid
        or is_winProcessId_valid
        or is_winProcessName_valid
        or is_winProcessExcutePath_valid
    ):
        return -1

    if not isinstance(waittingTime, (int, float)):
        waittingTime = 3
    if waittingTime > 5 * 60:
        waittingTime = 5 * 60
    if not isinstance(detectInterval, (int, float)):
        detectInterval = 3

    while waittingTime > 0:
        # 前置窗口句柄
        foregroundWinHwnd = win32gui.GetForegroundWindow()
        if is_winTitle_valid:
            _winTitle = win32gui.GetWindowText(foregroundWinHwnd)
            if _winTitle.find(winTitle) == -1:
                time.sleep(detectInterval)
                waittingTime -= detectInterval
                continue

        if is_winProcessName_valid or is_winProcessExcutePath_valid:
            # 获取窗口句柄对应的PID
            _, _winProcessId = win32process.GetWindowThreadProcessId(foregroundWinHwnd)
            if is_winProcessId_valid:
                if _winProcessId != winProcessId:
                    time.sleep(detectInterval)
                    waittingTime -= detectInterval
                    continue

            winProcess = psutil.Process(_winProcessId)

            if is_winProcessName_valid:
                _winProcessName = winProcess.name()
                if _winProcessName != winProcessName:
                    time.sleep(detectInterval)
                    waittingTime -= detectInterval
                    continue

            if is_winProcessExcutePath_valid:
                _winProcessExcutePath = winProcess.exe()
                # print("_winProcessExcutePath: [{0}]".format(_winProcessExcutePath))
                # print("winProcessExcutePath: [{0}]".format(winProcessExcutePath))
                if _winProcessExcutePath != winProcessExcutePath:
                    time.sleep(detectInterval)
                    waittingTime -= detectInterval
                    continue

        return foregroundWinHwnd
    return -1


# command


def parseAsFileAbsPath(arg: str, *parentDir, fileType=None) -> str:
    """
    将参数解析为文件绝对路径

    参数:
        workingDir (str): 当前程序运行的工作目录
        arg (str): 当前程序启动时传入的某个命令行启动参数

    可选参数:
        parentDir (*tuple): 解析的参数所在父级目录
            按照给定的父级目录从前往后依次检测, 返回第一个匹配的文件
        fileType (int): 解析的文件类型  1|2(文件|文件夹)
            默认为 `None` 表示不限制解析文件类型

    返回:
        返回成功解析出的并实际存在的文件路径(绝对路径), 解析失败返回 `None`
    """
    arg = arg.strip()
    if os.path.isabs(arg):
        if fileType is None:
            if os.path.exists(arg):
                return os.path.abspath(arg)
        elif fileType == 1:
            if os.path.isfile(arg):
                return os.path.abspath(arg)
        elif fileType == 2:
            if os.path.isdir(arg):
                return os.path.abspath(arg)
        return None

    else:
        if len(parentDir) == 0:
            return None

        for pDir in parentDir:
            filepath = os.path.join(pDir, arg)
            if fileType is None:
                if os.path.exists(filepath):
                    return os.path.abspath(filepath)
            elif fileType == 1:
                if os.path.isfile(filepath):
                    return os.path.abspath(filepath)
            elif fileType == 2:
                if os.path.isdir(filepath):
                    return os.path.abspath(filepath)

        return None


# file


def removeAllChildFiles(dirPath, *excludeFileNames):
    """
    删除指定目录下的所有子文件

    返回:
        成功删除返回 `True`
    """
    if not util.isDir(dirPath):
        return False

    removed = False
    for subFileName in os.listdir(dirPath):
        subFilePath = os.path.join(dirPath, subFileName)
        if util.isFile(subFilePath):
            if subFileName not in excludeFileNames:
                if not removed:
                    removed = True
                os.remove(subFilePath)
    return removed
