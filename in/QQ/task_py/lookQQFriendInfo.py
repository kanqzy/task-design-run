# 任务: 查看QQ好友信息
# 作者: 张三
# id: QQ@lookQQFriendInfo

import application
import common
import file
import keyInput
import mouse
import qq

import qqLogin


def lookQQFriendInfo(qqNumber: int, qqFriendNameOrNumber: str):
    """
    查看QQ好友信息

    参数:
        qqFriendNameOrNumber (str): QQ好友名称(备注名称或昵称)或QQ号
            该名称必须确保在当前QQ号下只有一个, 因为在搜索匹配的会默认取第1个匹配
    """
    qqLogin.qqLogin(qqNumber)

    searchPrompt_centerPos = qq.get_searchPrompt_centerPos()
    print("searchPrompt_centerPos: ", searchPrompt_centerPos)
    mouse.mouse_mousedown(searchPrompt_centerPos)
    keyInput.inputChineseCharsWithLetters(qqFriendNameOrNumber)

    # 鼠标下移100, 悬浮后会显示 `查看资料`
    mouse.mouse_relative_move([0, 100])
    common.wait(1 * 1000)

    # 搜索框输入好友昵称后, 鼠标移到 `查看资料` 点击
    searchFirstViewInfo_centerPos = qq.get_searchFirstViewInfo_centerPos()
    if searchFirstViewInfo_centerPos is None:
        common.printLog("QQ好友 `" + qqFriendNameOrNumber + "` not found")
        return

    mouse.mouse_mousedown(searchFirstViewInfo_centerPos)
    common.wait(1 * 1000)

    qq.foucus_friendInfo_window_and_draw_left()
    common.wait(1 * 1000)

    qqFriendData = qq.recognize_friendInfo_window_data()

    common.printLog("QQ好友 `" + qqFriendNameOrNumber + "`, 信息资料: " + str(qqFriendData))

    saveResult = file.saveJsonData(
        qqFriendData, "/QQ_好友_{0}_信息.json".format(qqFriendNameOrNumber)
    )

    common.printLog("QQ好友资料信息保存结果: " + str(saveResult))
    common.printLog("lookQQFriendInfo task complete")
