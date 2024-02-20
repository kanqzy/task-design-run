# 调试模块

import util

# 是否启用测试模块
# 启用后, 当前模块下的所有函数均执行, 反之, 则直接跳转
Enable = True

#  调用 `tprint` 时, 是否处于 开始和结束范围
__in_start_end_range = False
# 开始调用时, `enable` 参数值
__start_enable = True


def tprint(*values, enable=True):
    if not Enable:
        return

    if len(values) > 0:
        firstValue = values[0]
        global __in_start_end_range
        global __start_enable
        # 在原函数的开始的第一次调用处注册
        if firstValue == "/start":
            __in_start_end_range = True
            __start_enable = enable
            return

        # 在原函数的结束返回退出时注册
        elif firstValue == "/end":
            __in_start_end_range = False
            return

    if not enable or (__in_start_end_range and not __start_enable):
        return
    print(*values)


def twrite(outPath, content, jsonWrite=True, jsonFormat=True, enable=True):
    """
    将调试的内容写入文件中

    参数:
        outPath (str): 输出的文件路径
        content (str|object): 写入内容 对象类型会转为字符串
        jsonWrite (bool): 是否以JSON方式写入. 当且仅当 `content` 为 对象类型时有效
        jsonFormat (bool): JSON是否格式化. 当且仅当 `jsonWrite` 为 `True` 时有效

    返回:
        成功写入返回 `True`
    """
    if not Enable or not enable:
        return False

    if not util.isValidFilePath(outPath):
        return False

    if isinstance(content, str):
        return util.writeContent(outPath, content)

    else:
        if jsonWrite:
            if jsonFormat:
                return util.writeJson(outPath, content, indent=4)
            else:
                return util.writeJson(outPath, content)

        else:
            util.writeContent(outPath, str(content))
