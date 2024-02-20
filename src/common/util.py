# 工具模块
# v1.0.0

import hashlib
import json
import os
import re
import sys

import uuid


# 系统


def getEntryExePath():
    """
    获取python入口可执行文件路径
    """
    if getattr(sys, "frozen", False):
        return os.path.abspath(sys.executable)
    elif __file__:
        return os.path.abspath(__file__)


def getGuid(keepConnector=False):
    """
    获取GUID
        UUID是128位的全局唯一标识符，通常由32字节的字符串表示

    参数:
        keepConnector   是否保留连接符
    """
    # 生成GUID
    guidValue = str(uuid.uuid4())
    if keepConnector:
        return guidValue
    return guidValue.replace("-", "")


# 字符串

## 字符串类型判断


def isEmptyStr(string):
    """
    判断字符串是否是空字符串
        字符串中全部是一到多个字符(\s,\t,\r,\n) 视为空字符串
    """
    if isinstance(string, str) and string.strip() == "":
        return True
    return False


def isNonEmptyStr(string):
    """
    判断字符串是否是非空字符串
        字符串中全部是一到多个字符(\s,\t,\r,\n) 视为空字符串
    """
    if isinstance(string, str) and string.strip() != "":
        return True
    return False


def isIP(str):
    """
    判断一个字符串是否是IP地址(IPv4地址)
        IP地址的范围为0.0.0.0-255.255.255.255
    """
    p = re.compile(
        "^(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]\\d|\\d)\\.(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]\\d|\\d)\\.(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]\\d|\\d)\\.(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]\\d|\\d)$"
    )
    if p.match(str):
        return True
    else:
        return False


def isPort(port):
    """
    是否是端口号(0-65535)
    """
    if isinstance(port, int) and 0 <= port <= 65535:
        return True
    elif isinstance(port, str):
        p = re.compile(
            r"^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
        )
        if p.match(port):
            return True
    return False


def isGUID(string, containsConnector=False):
    """
    判断一个字符串是否是GUID码

    参数:
        containsConnector   是否包含连接符 `-`, 生成的原始GUID码都会有连接符, 很多应用场景中会将连接符去掉后返回
    """
    if containsConnector:
        p = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
        )
        if p.match(string):
            return True

    else:
        p = re.compile(
            r"^[0-9a-fA-F]{8}[0-9a-fA-F]{4}[0-9a-fA-F]{4}[0-9a-fA-F]{4}[0-9a-fA-F]{12}$"
        )
        if p.match(string):
            return True

    return False


def isInt(string, nonnegative=False):
    """
    判断一个字符串是否是整数(十进制)

    参数:
        nonnegative 是否是非负数(包含0)
    """
    if nonnegative:
        p = re.compile(r"^((0+)|([1-9][0-9]*))$")
        if p.match(string):
            return True

    else:
        p = re.compile(r"^((0+)|(-?[1-9][0-9]*))$")
        if p.match(string):
            return True

    return False


def isFloat(string, nonnegative=False):
    """
    判断一个字符串是否是浮点数(小数)

    参数:
        nonnegative 是否是非负数(包含0.00)
    """
    if nonnegative:
        p = re.compile(r"^[0-9]+\.[0-9]+$")
        if p.match(string):
            return True

    else:
        p = re.compile(r"^-?[0-9]+\.[0-9]+$")
        if p.match(string):
            return True

    return False


def isNumber(string):
    """
    判断一个字符串是否是数字(整数或小数)
    """
    p = re.compile(r"^-?((0+)|([1-9][0-9]*)|([0-9]+\.[0-9]+))$")
    if p.match(string):
        return True
    return False


def isMultiplicativeExpression(string, intOnly=False):
    """
    判断一个字符串是否是乘法表达式
        乘法表达式的格式: `数字1 * 数字2 ... * 数字N`
        例如: `1 * 2 * 3` 为一个乘法表达式

    参数:
        intOnly     是否仅仅是整数 为 `True` 时, 表达式中的所有数字必须是int型整数才返回 `True`
    """
    strs = re.split(r"\s*\*\s*", string)
    for str in strs:
        str = str.strip()

        if intOnly:
            if not isInt(str):
                return False

        else:
            if not isNumber(str):
                return False

    return True


def containsIp(string):
    """
    判断字符串中是否包含IP地址(IPv4地址)
        IP地址的范围为0.0.0.0-255.255.255.255
    """
    p = re.compile(
        "(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]\\d|\\d)\\.(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]\\d|\\d)\\.(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]\\d|\\d)\\.(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]\\d|\\d)"
    )
    if p.search(string):
        return True
    else:
        return False


def findIps(string):
    """
    查找字符串中的所有IP地址(IPv4地址)
        IP地址的范围为0.0.0.0-255.255.255.255

    返回:
        返回从前往后查找匹配到的IP列表, 查找不到返回空列表
    """
    subStrPattern = "(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]\\d|\\d)\\.(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]\\d|\\d)\\.(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]\\d|\\d)\\.(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]\\d|\\d)"
    return [subMatch.group() for subMatch in re.finditer(subStrPattern, string)]


## 字符串转换bytes


def getFixedByteLengthBytes(content, byteLength, encoding="utf-8"):
    """
    获取固定字节长度的文本字节
        内容长度不够的, 用空格补全, 长度小于文本字节长度, 返回原文本
        计算文本的字节长度, 默认使用编码(utf-8)

    参数:
        content         文本内容
        byteLength      指定字节长度
        encoding        指定字节编码
    """
    if content is None or len(content) == 0:
        return None
    contentBytes = bytes(content, encoding=encoding)
    contentBytesLen = len(contentBytes)
    if byteLength <= contentBytesLen:
        return contentBytes
    fillSpaceCount = byteLength - contentBytesLen
    return contentBytes + bytes(" " * fillSpaceCount, encoding=encoding)


def getFixedByteLengthContent(content, byteLength, encoding="utf-8"):
    """
    获取固定字节长度的文本内容
        内容长度不够的, 用空格补全; 大于指定字节长度的, 返回原文本
        计算文本的字节长度, 默认使用编码(utf-8)

    参数:
        content         文本内容
        byteLength      指定字节长度
        encoding        指定字节编码
    """
    if content is None or len(content) == 0:
        return content
    contentBytes = bytes(content, encoding=encoding)
    contentBytesLen = len(contentBytes)
    if byteLength <= contentBytesLen:
        return content
    fillSpaceCount = byteLength - contentBytesLen
    return content + " " * fillSpaceCount


# 安全


def stringMd5(content, encoding="utf8"):
    """
    计算字符串的md5值
    """
    if not isinstance(content, str):
        return None
    md5 = hashlib.md5()
    md5.update(content.encode(encoding))
    result = md5.hexdigest()
    return result


def fileMd5(filepath):
    """
    计算文件的md5值
    """
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return None
    md5 = hashlib.md5()
    with open(filepath, "rb") as fo:
        while True:
            data = fo.read(4096)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


# 字典


def isNonEmptyDict(dictData):
    """
    判断字典是否为非空字典
    """
    if isinstance(dictData, dict) and len(dictData) > 0:
        return True
    return False


def isDictHasKeys(dictData, *keys):
    """
    判断字典数据指定的键是否都存在
    """
    if not isinstance(dictData, dict) or len(keys) == 0:
        return False
    dictData_keys = dictData.keys()
    for key in keys:
        if not isinstance(key, str) or not key in dictData_keys:
            return False
    return True


def isDictKeysTrue(dictData, *keys):
    """
    判断字典数据指定的键是否均为True
        判断规则: 检测指定的key都存在, 且值为bool型的 `True` 值时, 返回 True; 反之, 则一律返回 False
    """
    if not isinstance(dictData, dict) or len(keys) == 0:
        return False
    for key in keys:
        if not key in dictData.keys():
            return False
        value = dictData[key]
        if not isinstance(value, bool) or not value:
            return False
    return True


# 文件


def isValidDir(dirPath):
    """
    判断文件目录是否有效
        目录路径不存在时, 会尝试在磁盘上创建, 成功创建也视为有效
        不合法的路径会报异常
    """
    if not isinstance(dirPath, str) or len(dirPath.strip()) == 0:
        return False
    if os.path.exists(dirPath):
        if os.path.isdir(dirPath):
            return True
    else:
        return mkdirs(dirPath)
    return False


def isValidFilePath(filepath):
    """
    判断文件路径是否有效
        判断文件所在目录是否存在, 若存在则视为有效; 反之, 则尝试在磁盘上创建目录, 成功创建也视为有效
        不合法的路径会报异常
    """
    if not isinstance(filepath, str) or len(filepath.strip()) == 0:
        return False
    dirPath = os.path.dirname(filepath)
    if os.path.exists(dirPath):
        return True
    else:
        return mkdirs(dirPath)


def isDir(filepath):
    """
    判断一个文件路径是否是文件夹
        文件路径真实存在且为文件夹
    """
    if isinstance(filepath, str) and filepath != "":
        if os.path.exists(filepath) and os.path.isdir(filepath):
            return True
    return False


def isFile(filepath):
    """
    判断一个路径是否是文件
        文件路径真实存在且为文件
    """
    if isinstance(filepath, str) and filepath != "":
        if os.path.exists(filepath) and os.path.isfile(filepath):
            return True
    return False


def isDirHasFile(dirPath, filePattern):
    """
    判断当前文件夹下否有某类文件

    参数:
        filePattern   文件模式(正则表达式)
    """
    if (
        not isinstance(dirPath, str)
        or len(dirPath.strip()) == 0
        or not isinstance(filePattern, str)
        or len(filePattern.strip()) == 0
    ):
        return False
    if not os.path.exists(dirPath) or not os.path.isdir(dirPath):
        return False
    for subFileName in os.listdir(dirPath):
        if re.search(filePattern, subFileName) is not None:
            return True
    return False


def searchFileNames(dirPath, filePattern, type="*"):
    """
    在当前文件夹下搜索符合指定模式的文件(夹)名称

    参数:
        filePattern   文件模式(正则表达式)
        type          文件类型 不限类型|文件|文件夹(*|file|dir)

    返回:
        返回符合所有符合条件的文件名列表, 没有搜索到返回空列表
    """
    if (
        not isinstance(dirPath, str)
        or len(dirPath.strip()) == 0
        or not isinstance(filePattern, str)
        or len(filePattern.strip()) == 0
    ):
        return None
    if not os.path.exists(dirPath) or not os.path.isdir(dirPath):
        return None
    subFileNames = []
    dirPath = os.path.abspath(dirPath)
    for subFileName in os.listdir(dirPath):
        if re.search(filePattern, subFileName) is not None:
            if type == "*":
                subFileNames.append(subFileName)
            else:
                subFilePath = dirPath + "\\" + subFileName
                if type == "file":
                    if os.path.isfile(subFilePath):
                        subFileNames.append(subFileName)
                elif type == "dir":
                    if os.path.isdir(subFilePath):
                        subFileNames.append(subFileName)
    return subFileNames


def searchFiles(dirPath, filePattern, type="*"):
    """
    在当前文件夹下搜索符合指定模式的文件(夹)

    参数:
        filePattern   文件模式(正则表达式)
        type          文件类型 不限类型|文件|文件夹(*|file|dir)

    返回:
        返回符合所有符合条件的文件路径列表, 没有搜索到返回空列表
    """
    if (
        not isinstance(dirPath, str)
        or len(dirPath.strip()) == 0
        or not isinstance(filePattern, str)
        or len(filePattern.strip()) == 0
    ):
        return None
    if not os.path.exists(dirPath) or not os.path.isdir(dirPath):
        return None
    subFilePaths = []
    dirPath = os.path.abspath(dirPath)
    for subFileName in os.listdir(dirPath):
        if re.search(filePattern, subFileName) is not None:
            subFilePath = dirPath + "\\" + subFileName
            if type == "*":
                subFilePaths.append(subFilePath)
            else:
                if type == "file":
                    if os.path.isfile(subFilePath):
                        subFilePaths.append(subFilePath)
                elif type == "dir":
                    if os.path.isdir(subFilePath):
                        subFilePaths.append(subFilePath)
    return subFilePaths


def getFileName(filepath):
    """
    获取文件名(全名称包含后缀名)
    """
    if not isinstance(filepath, str) or len(filepath.strip()) == 0:
        return None
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return None
    return os.path.basename(filepath)


def getFilePrefixName(filepath):
    """
    获取文件前缀名
    """
    if not isinstance(filepath, str) or len(filepath.strip()) == 0:
        return None
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return None
    filename = os.path.basename(filepath)
    return os.path.splitext(filename)[0]


def getFileExt(filepath):
    """
    获取文件扩展名: `.文件类型名`
    """
    if not isinstance(filepath, str) or len(filepath.strip()) == 0:
        return None
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return None
    filename = os.path.basename(filepath)
    return os.path.splitext(filename)[1]


def getNoRepeatFileName(dirPath, filePreName, fileExt=""):
    """
    获取文件夹下无重复的文件(夹)名称
        在给定的目录下创建一个文件(夹), 若文件名已存在时, 会在文件名后加`(n)`,
        `n` 从2开始向上累加, 直到当前目录下没有同名的文件时结束(最高累加10000次)

    参数:
        dirPath:        给定目录
        filePreName:    文件前缀名(文件类型时, 最后一个点号前面的名称; 文件夹类型时,前缀名就是文件夹名称)
        fileExt:        文件后缀名(文件类型时, 包括最后一个点号及其后面的名称)

    返回:
        无重复的文件(夹)名称
    """
    if (
        dirPath is None
        or not isinstance(filePreName, str)
        or len(filePreName.strip()) == 0
    ):
        return None
    if fileExt is None:
        fileExt = ""
    if not (os.path.exists(dirPath) and os.path.isdir(dirPath)):
        return None
    filename = filePreName + fileExt
    if len(filename.strip()) == 0:
        return None
    if not os.path.exists(dirPath + "\\" + filename):
        return filename
    n = 2
    while n <= 10000:
        filename = "{0}({1}){2}".format(filePreName, n, fileExt)
        if not os.path.exists(dirPath + "\\" + filename):
            return filename
        n += 1
    return None


def getParentDir(currentPath, upperCount=1):
    """
    根据向上层次获取当前文件路径所在的父目录路径(绝对路径(\))

    参数:
        upperCount  向上层次, 1表示当前脚本文件的父目录, 2表示该父目录的父目录, 依次类推, ..., 直到根盘符
                    向上最高支持10次
    """
    if upperCount <= 1:
        upperCount = 1
    elif upperCount >= 10:
        upperCount = 10
    parentDir = os.path.abspath(os.path.dirname(currentPath))
    count = 1
    while count < upperCount:
        parentDir = os.path.abspath(os.path.dirname(parentDir))
        count += 1
    return parentDir


def getRelativePath(dirPath, filepath):
    """
    获取文件相对其所在目录的相对路径(/)
    """
    if not isinstance(dirPath, str) or len(dirPath.strip()) == 0:
        return None
    if not isinstance(filepath, str) or len(filepath.strip()) == 0:
        return None
    dirPath = os.path.abspath(dirPath)
    filepath = os.path.abspath(filepath)
    if filepath != dirPath and filepath.find(dirPath) == 0:
        return filepath.replace(dirPath, "").replace("\\", "/")[1:]
    return None


def getSubAbsolutePath(dirPath, subFileRelativePath):
    """
    获取子文件绝对路径

    参数:
        dirPath         目录路径
        subFilePath     目录下的子文件相对路径(相对目录)
    """
    if not isinstance(dirPath, str) or len(dirPath.strip()) == 0:
        return None
    if (
        not isinstance(subFileRelativePath, str)
        or len(subFileRelativePath.strip()) == 0
    ):
        return None
    dirPath = os.path.abspath(dirPath)
    subFileRelativePath = subFileRelativePath.strip().replace("/", "\\")
    return dirPath + "\\" + subFileRelativePath


def convertFileSize(size):
    """
    转换文件大小
        根据文件字节数转换为对应单位的表示(<1024), 并保留两位小数
        精确的被整除, 不带小数

    参数:
        文件字节数

    返回:
        带单位的文件大小字符串
    """
    # 文件大小单位: `B`表示字节, `KB`表示千字节, 每向后一次递乘1024
    if size < 1024:
        return "{0} {1}".format(size, "B")
    elif 1024 <= size < 1024**2:
        n = 1024
        if size % n == 0:
            return "{0} {1}".format(size // n, "KB")
        else:
            result = "{:.2f} {}".format(size / n, "KB")
            return "{:.2f} {}".format(size / 1024, "KB")
    elif 1024**2 <= size < 1024**3:
        n = 1024**2
        if size % n == 0:
            return "{0} {1}".format(size // n, "MB")
        else:
            return "{:.2f} {}".format(size / n, "MB")
    elif 1024**3 <= size < 1024**4:
        n = 1024**3
        if size % n == 0:
            return "{0} {1}".format(size // n, "GB")
        else:
            return "{:.2f} {}".format(size / n, "GB")
    elif 1024**4 <= size < 1024**5:
        n = 1024**4
        if size % n == 0:
            return "{0} {1}".format(size // n, "TB")
        else:
            return "{:.2f} {}".format(size / n, "TB")
    return None


def mkdirs(dirPath, exist_ok=False):
    """
    根据文件夹路径, 创建一个文件夹
        创建时会从根目录开始, 不存在就创建, 一直递归创建到当前目录
        不合法的路径会报异常

    参数:
        dirPath: 文件夹路径

    返回:
        成功创建返回true
    """
    if not isinstance(dirPath, str) or len(dirPath.strip()) == 0:
        return False
    if os.path.exists(dirPath):
        return False
    os.makedirs(dirPath, exist_ok=exist_ok)
    return True


def readContent(filepath, encoding="utf-8", limit_filesize=1024 * 1024):
    """
    一次性读取文件全部内容

    参数:
        limit_filesize      限制文件大小(<10M), 默认1M文件 超过限制范围不予读取
    """
    if not isinstance(filepath, str) or len(filepath.strip()) == 0:
        return None
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return None
    if (
        not isinstance(limit_filesize, int)
        or limit_filesize <= 0
        or limit_filesize >= 10 * 1024 * 1024
    ):
        limit_filesize = 1024 * 1024
    filesize = os.path.getsize(filepath)
    if filesize > limit_filesize:
        print("filesize out of range")
        return None

    fo = open(filepath, "r", encoding=encoding)
    content = fo.read()
    fo.close()
    return content


def readLines(filepath, encoding="utf-8"):
    """
    读取文件的文本内容, 返回读取的每行内容列表
    """
    if not isinstance(filepath, str) or len(filepath.strip()) == 0:
        return None
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return None
    fo = open(filepath, "r", encoding=encoding)
    lines = []
    while True:
        line = fo.readline()
        if not line:
            break
        lines.append(line)
    fo.close()
    return lines


def writeContent(outPath, content, encoding="utf-8"):
    """
    向文件写入文本内容
        如果文件路径不存在, 则尝试创建文件路径所属的目录
        不合法的路径会报异常
    """
    if not isinstance(outPath, str) or len(outPath.strip()) == 0:
        return False
    if not isinstance(content, str) or len(content) == 0:
        return False
    dirPath = os.path.dirname(outPath)
    if not os.path.exists(dirPath):
        createDir = mkdirs(dirPath)
        if createDir != True:
            return False
    fo = open(outPath, "w", encoding=encoding)
    fo.write(content)
    fo.close()
    return True


def writeLines(outPath, lines, newline=False, encoding="utf-8"):
    """
    向文件写入行列表内容
        如果文件路径不存在, 则尝试创建文件路径所属的目录
        不合法的路径会报异常

    参数:
        lines       行列表
        newline     是否换行(行列表每一个元素尾巴追加换行符 `\n`)
    """
    if not isinstance(outPath, str) or len(outPath.strip()) == 0:
        return False
    if not isinstance(lines, list):
        return False
    dirPath = os.path.dirname(outPath)
    if not os.path.exists(dirPath):
        createDir = mkdirs(dirPath)
        if createDir != True:
            return False
    fo = open(outPath, "w", encoding=encoding)
    if newline:
        lines = [line + "\n" for line in lines]
    fo.writelines(lines)
    fo.close()
    return True


def writeJson(
    outPath,
    jsonObj,
    encoding="utf-8",
    indent=None,
    sort_keys=False,
    ensure_ascii=False,
):
    """
    将json字典数据写入文件
        不合法的路径会报异常

    参数:
        outPath         写入文件路径
        jsonObj         json对象
        encoding        写入文件的编码, 默认 `utf-8`
        indent          写入的json是否缩进,
                            未缩进: 将json字典数据序列化为一行JSONString
                            缩进:   将json字典数据序列化为多行JSONString, 并进行排版美化(缩进4个空格)
        sort_keys       是否对json字典的key进行排序(a-z)
        ensure_ascii    是否确保显示是 `ascii` 字符 如果为 `false`，则序列化的JSON字符串可以包含非 `ascii` 字符; 反之, 则会被全部被转义显示。
                        例如: 汉字 `一` 会转义为 `\u4e00` 显示

    返回:
        成功写入返回 `True`
    """
    if not isinstance(outPath, str) or len(outPath.strip()) == 0:
        return False
    dirPath = os.path.dirname(outPath)
    if not os.path.exists(dirPath):
        createDir = mkdirs(dirPath)
        if createDir != True:
            return False
    jsonString = json.dumps(
        jsonObj,
        indent=indent,
        sort_keys=sort_keys,
        ensure_ascii=ensure_ascii,
    )
    fo = open(outPath, "w", encoding=encoding)
    fo.write(jsonString)
    fo.close()
    return True


def appendContent(filepath, content, created=True, encoding="utf-8"):
    """
    向文件追加内容

    参数:
        created     如果文件不存在, 是否创建
        encoding    文件不存在时, 创建文件的编码; 文件已存在, 源文件的编码

    参数:
        成功追加, 返回True
    """
    if not isinstance(filepath, str) or len(filepath) == 0:
        return False
    if not isinstance(content, str) or len(content) == 0:
        return False
    if os.path.exists(filepath):
        if os.path.isfile(filepath):
            f = open(filepath, "a", encoding=encoding)
            f.write(content)
            f.close()
            return True
        else:
            return False
    else:
        if created != True:
            return False
        # 文件不存在, 尝试先创建父目录, 然后再写文件
        parentDir = os.path.dirname(filepath)
        if len(parentDir) == 0:
            return False

        mkdirs(parentDir)
        if os.path.exists(parentDir):
            f = open(filepath, "w", encoding=encoding)
            f.write(content)
            f.close()
            return True
        return False


class Properties(object):
    """
    配置文件(.properties)类
        可获取配置文件下的所有属性键和值
    """

    def __init__(self, fileName):
        self.fileName = fileName
        self.properties = {}

    def __getDict(self, dict, lineStrName, lineStrValue):
        """
        递归获取字典, 处理属性键包含`.`的情况
        """
        if lineStrName.find(".") > 0:
            k = lineStrName.split(".")[0]
            dict.setdefault(k, {})
            return self.__getDict(dict[k], lineStrName[len(k) + 1 :], lineStrValue)
        else:
            dict[lineStrName] = lineStrValue
            return dict

    def getProperties(self):
        """
        获取配置文件字典信息
        """
        try:
            pro_file = open(self.fileName, "r", encoding="UTF-8")
            for line in pro_file.readlines():
                if line.find("=") > 0:
                    strs = line.split("=")
                    strName = strs[0].strip()
                    strValue = strs[1].strip()
                    self.__getDict(self.properties, strName, strValue)
        except Exception:
            print("getProperties err")
        else:
            pro_file.close()
        return self.properties
