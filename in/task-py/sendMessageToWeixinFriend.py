# 任务: 给某人发消息
# 作者: John
# id: 1

import common
import mouse


def sendMessageToWeixinFriend(联系人: object, 消息: str):
    # 鼠标移到加微信的位置输入内容并回车
    mouse.mouse_move_input_enter({"x": 100, "y": 200}, str(联系人))

    # 等待3秒
    common.wait(3 * 1000)

    # 鼠标点击好友
    mouse.mouse_mousedown({"x": 100, "y": 200})

    # 鼠标移到右侧的聊天窗口并输入内容回车
    mouse.mouse_move_input_enter({"x": 100, "y": 200}, "我将要发送的消息:" + 消息)
