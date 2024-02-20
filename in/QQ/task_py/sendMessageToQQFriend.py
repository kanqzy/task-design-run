# 任务: 给QQ好友发消息
# 作者: 张三
# id: QQ@sendMessageToQQFriend

import application
import common
import keyInput
import mouse
import qq

import qqLogin


def sendMessageToWeixinFriend(qqNumber: int, qqFriendRemarkName: str, message: str):
    """
    给指定QQ好友发消息
    """
    qqLogin.qqLogin(qqNumber)

    keyInput.inputChineseChars(qqFriendRemarkName)
    common.wait(1 * 1000)
    foucus_search_result = qq.foucus_search_text()
    if not foucus_search_result:
        common.printLog("fail foucus_search_text")
        return

    # 鼠标下移100, 悬浮后会显示 `打开回话窗口`
    mouse.mouse_relative_move([0, 100])
    common.wait(1 * 1000)

    # 搜索框输入好友昵称后, 鼠标移到 `查看资料` 点击
    OpenChatWindow_centerPos = qq.get_searchFirstOpenChatWindow_centerPos()
    if OpenChatWindow_centerPos is None:
        common.printLog("QQ好友 `" + qqFriendRemarkName + "` not found")
        return

    mouse.mouse_mousedown(OpenChatWindow_centerPos)
    common.wait(1 * 1000)

    sendResult = qq.foucus_chat_window_sendMessage(message)
    common.printLog("发送消息的结果: " + str(sendResult))

    if sendResult:
        common.printLog(
            "qqNumber `{0}` 向好友 `{1}` 成功发送了消息 `{2}`".format(
                qqNumber, qqFriendRemarkName, message
            )
        )
        common.capture_screen_region("../out/QQ/sendMessageToQQFriend/send_result.png")
    else:
        common.printLog(
            "qqNumber `{0}` 向好友 `{1}`发送消息 `{2}` 失败了".format(
                qqNumber, qqFriendRemarkName, message
            )
        )

    common.printLog("sendMessageToQQFriend task complete")
