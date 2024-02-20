# 任务: 添加微信
# 作者: John
# id: 1

import common
import mouse

import task_1


def addWeixinFriend(联系人: object):
    # 鼠标移到加微信的位置输入内容并回车
    mouse.mouse_move_input_enter({"x": 100, "y": 200}, str(联系人))

    # 等待3秒
    common.wait(3 * 1000)

    # 鼠标移到加网络好友产点击
    mouse.mouse_mousedown({"x": 100, "y": 200})

    # 等待10秒钟假设人加上了
    common.wait(10 * 1000)

    # 加上好友后，主动给对方发消息
    task_1.sendMessageToWeixinFriend(联系人, "你好啊，我是xxx,加你有事，收到请回复")

    common.printLog("好友已加上，并发送了消息")
