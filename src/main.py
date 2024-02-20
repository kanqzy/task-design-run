# 入口模块
# 这里的所有任务都以真实的方式运行

import os
import sys
import time

import uiautomation as auto

sys.path.append("./common")
sys.path.append("./task")
sys.path.append("./task/function/py")

from debug import tprint
import log
import logger
import util

from run_task import Task


def run_task_qqLogin():
    time.sleep(3)
    taskJsonPath = os.path.abspath("../in/QQ/task/qqLogin.json")

    # 1|2|3
    run = 2
    if run == 1:
        try:
            Task(taskJsonPath, 2413750622).run()
        except Exception as e:
            tprint("task run err")

    elif run == 2:
        try:
            Task(taskJsonPath, 203299362).run()
        except Exception as e:
            tprint("task run err")

    elif run == 3:
        try:
            Task(taskJsonPath, 1624803880).run()
        except Exception as e:
            tprint("task run err")

    # 重新激活聚焦控制台窗口
    consoleWindow = auto.GetConsoleWindow()
    consoleWindow.SetActive()
    print("run complete")


# run
run_task_qqLogin()
