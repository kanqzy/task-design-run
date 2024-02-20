# 任务: QQ登录
# 作者: 张三
# id: QQ@qqLogin

import application
import common
import keyInput
import mouse
import qq


def qqLogin(qqNumber: int):
    """
    qq登录

    只支持如下QQ号:
        1. 主号(默认号): 2413750622
        2. 第2个号(下拉第2个): 203299362
        3. 第3个号(下拉第3个): 1624803880
    """
    logined = qq.check_qq_logined(qqNumber)
    if logined:
        common.printLog("qqNumber `{0}` 已经登录了".format(qqNumber))
        formatNowTime = common.getFormatNowTime("yyyy-MM-dd HH-mm-ss")
        common.capture_screen_region(
            "../out/QQ/qqLogin/" + formatNowTime + "/login_result.png"
        )
        common.printLog("qqLogin task complete")
        return

    # 启动本地QQ应用程序(QQ.exe)
    application.quickStartApp("腾讯QQ")

    # 等待QQ登录窗口出现
    waittingResult = qq.waittingForLoginAppear(8)
    if not waittingResult["appear"]:
        common.printLog("failed waitting for ContactHomeAppear in 8 seconds")
        return
    loginWinRect = waittingResult["winRect"]

    select_input_result = qq.select_qq_number_input(loginWinRect, qqNumber)
    if not select_input_result:
        common.printLog("select_input_result failed")
        common.printLog(
            "qqNumber `"
            + str(qqNumber)
            + "` is not supported, only support for [2413750622, 203299362, 1624803880]"
        )
        common.interrupt()
        return

    # 鼠标移到"登录"按钮点击
    mouse.mouse_mousedown([965, 731])

    waittingResult = qq.waittingForContactHomeAppear(qqNumber, 8)
    if waittingResult["appear"]:
        common.printLog("qqNumber `{0}` 登录成功了".format(qqNumber))
        common.capture_screen_region("../out/QQ/qqLogin/login_result.png")
    else:
        common.printLog("qqNumber `{0}` 登录失败了".format(qqNumber))

    common.printLog("qqLogin task complete")
