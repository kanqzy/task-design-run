# 入口模块
# 这里的所有任务都以模拟的方式运行

import os
import sys

sys.path.append("./common")
sys.path.append("./task")
sys.path.append("./task/function/py_simulate")

from run_task import Task


def simulate_run_task_sendMessageToWeixinFriend():
    taskJsonPath = os.path.abspath("../in/task/sendMessageToWeixinFriend.json")
    Task(taskJsonPath, "张三", "吃饭了吗").run()


def simulate_run_task_addWeixinFriend():
    taskJsonPath = os.path.abspath("../in/task/addWeixinFriend.json")
    Task(taskJsonPath, "李四").run()


def simulate_run_task_show_while_if_else_usage():
    taskJsonPath = os.path.abspath("../in/task/show_while_if_else_usage.json")
    Task(taskJsonPath, 3).run()


def simulate_run_task_show_while_if_else_usage_2():
    taskJsonPath = os.path.abspath("../in/task/show_while_if_else_usage_2.json")
    Task(taskJsonPath, 3).run()


def simulate_run_task_show_while_if_else_usage_3():
    taskJsonPath = os.path.abspath("../in/task/show_while_if_else_usage_3.json")
    Task(taskJsonPath, 3).run()
    
def simulate_run_task_show_while_if_else_usage_4():
    taskJsonPath = os.path.abspath("../in/task/show_while_if_else_usage_4.json")
    Task(taskJsonPath, 6).run()


# run
# simulate_run_task_sendMessageToWeixinFriend()
# simulate_run_task_addWeixinFriend()
# simulate_run_task_show_while_if_else_usage()
# simulate_run_task_show_while_if_else_usage_2()
# simulate_run_task_show_while_if_else_usage_3()
# simulate_run_task_show_while_if_else_usage_4()
