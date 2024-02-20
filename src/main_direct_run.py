# 入口模块
# 这里的所有任务都是在引用基础函数的基础上, 直接调用运行任务模块
# 主要是检测任务模块文件是否可运行

import sys
import time

import uiautomation as auto

sys.path.append("./common")
sys.path.append("./task/function/py")
sys.path.append("../in/QQ/task_py")

from debug import tprint
import log
import logger
import util

import qqLogin
import lookQQFriendInfo
import sendMessageToQQFriend

ExcuteFilePath = util.getEntryExePath()

# 应用程序根目录(可执行文件位于根目录下的 `bin` 目录下)
AppRootDir = util.getParentDir(ExcuteFilePath, 3)
LOGGER = logger.getCustomLogger(
    AppRootDir + "\\logs", logInConsole=True, logConsoleFormatter=log.Formatter_Default
)

Err_Log_Formatter = {
    "formatter": log.Empty_Logging_Formatter,
    "msgFormat": "{asctime} - [Task Error]: {message}",
}


def run_QQ_qqLogin():
    """
    启动后, 休眠3s, 在这3s内, 切到桌面, 等待程序进行后续操作
    """
    time.sleep(3)
    # 1|2|3
    run = 3
    if run == 1:
        try:
            qqLogin.qqLogin(2413750622)
        except Exception as e:
            LOGGER.error("qqLogin err", errorType=e)

    elif run == 2:
        try:
            qqLogin.qqLogin(203299362)
        except Exception as e:
            LOGGER.error("qqLogin err", errorType=e)

    elif run == 3:
        try:
            qqLogin.qqLogin(1624803880)
        except Exception as e:
            LOGGER.error("qqLogin err", errorType=e)

    # 重新激活聚焦控制台窗口
    consoleWindow = auto.GetConsoleWindow()
    consoleWindow.SetActive()
    print("run complete")


def run_QQ_lookQQFriendInfo():
    """
    启动后, 休眠3s, 在这3s内, 切到桌面, 等待程序进行后续操作
    """
    time.sleep(3)
    # 1|2|3|4
    run = 4
    if run == 1:
        try:
            lookQQFriendInfo.lookQQFriendInfo(2413750622, "一路走来")
        except Exception as e:
            LOGGER.error("lookQQFriendInfo err", errorType=e)

    elif run == 2:
        try:
            lookQQFriendInfo.lookQQFriendInfo(2413750622, "东京光芒")
        except Exception as e:
            LOGGER.error("lookQQFriendInfo err", errorType=e)

    elif run == 3:
        try:
            lookQQFriendInfo.lookQQFriendInfo(203299362, "青青河边草")
        except Exception as e:
            LOGGER.error("qqLogin err", errorType=e)

    elif run == 4:
        try:
            lookQQFriendInfo.lookQQFriendInfo(203299362, "2413750622")
        except Exception as e:
            LOGGER.error("qqLogin err", errorType=e)

    # 重新激活聚焦控制台窗口
    consoleWindow = auto.GetConsoleWindow()
    consoleWindow.SetActive()
    print("run complete")


def run_QQ_sendMessageToQQFriend():
    """
    启动后, 休眠3s, 在这3s内, 切到桌面, 等待程序进行后续操作
    """
    time.sleep(3)
    # 1
    run = 1
    if run == 1:
        try:
            sendMessageToQQFriend.sendMessageToWeixinFriend(
                2413750622, "一路走来", "hello , I am kanq"
            )
        except Exception as e:
            LOGGER.error("sendMessageToWeixinFriend err", errorType=e)

    # 重新激活聚焦控制台窗口
    consoleWindow = auto.GetConsoleWindow()
    consoleWindow.SetActive()
    print("run complete")


# run
# run_QQ_qqLogin()
# run_QQ_lookQQFriendInfo()
run_QQ_sendMessageToQQFriend()
