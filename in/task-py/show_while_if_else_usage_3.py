# 任务: 实现whil loop  if else等
# 作者: John
# id: 1

import common
import mouse


def show_while_if_else(初始值: int = 10):
    dic = {
        "变量1": 1,
        "mouseGetText": "",
        "total_mouseGetText":""
    }

    变量1 = 1
    mouseGetText = ""
    total_mouseGetText = ""

    while 变量1 <= 初始值:
        变量1 = 变量1 + 1
        common.printLog(变量1)
        
        # 变量名 `mouseGetText` 为 `mouse.json` 下当前函数的返回变量名
        mouseGetText = mouse.mouse_get_text([300, 500], [50,80])
        total_mouseGetText = total_mouseGetText + mouseGetText + ","
        
    common.printLog("总共识别的文本为: " + total_mouseGetText)
    common.printLog("总共识别的文本长度为: " + str(len(total_mouseGetText)))

    if 变量1 == 10:
        变量1 = 变量1 + 1
        common.printLog(变量1)

    else:
        变量1 = 变量1 + 10
        common.printLog(变量1)
