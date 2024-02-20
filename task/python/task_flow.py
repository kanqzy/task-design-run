# 任务: 实现whil loop  if else等
# 作者: John
# id: 1

import common


def show_while_if_else(初始值: int = 10):
    变量1 = 1

    while 变量1 <= 初始值:
        变量1 = 变量1 + 1
        common.printLog(变量1)

    if 变量1 == 10:
        变量1 = 变量1 + 1
        common.printLog(变量1)

    else:
        变量1 = 变量1 + 10
        common.printLog(变量1)
