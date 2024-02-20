# 日志模块
# v1.0.0

from datetime import datetime
import inspect
import logging
import os
import time
import traceback

import util


# 空原生格式 当前模块以及外部模块所有创建的日志样式格式化器 `formatter` 属性值均必须使用该值
Empty_Logging_Formatter = logging.Formatter()

# 标准样式格式(带日期样式输出日志内容)
Formatter_Standard = {
    # 是否记录最上层的日志信息 为 `False` 时, 只会显示运行时堆栈最底层调用处信息(日志文件名和代码行号);
    # 反之, 则会显示运行时堆栈最上层调用处信息。
    # 例如: 运行时堆栈的最上层需要记录日志处调用了一个日志方法, 该方法调用了日志模块 `log.py`,
    #       该模块下有一个日志类下的某方法调用了底层的日志代码 `logger.info(msg, *args, **kwargs)`,
    #       若此处设为 `False`, 则只会记录底层日志代码执行处日志信息
    "logTopLevel": True,
    # 记录日志时, 会将`logging` 中 `Formatter` 设为空, 并将记录的日志消息内容 `msg` 转换为 `msgFormat` 格式的消息内容
    "formatter": Empty_Logging_Formatter,
    # 输出的日志消格式
    "msgFormat": "{asctime} - {filename}[line:{lineno}] - {levelname}: {message}",
}

# 原生格式(原样输出日志内容)
Formatter_Raw = {"formatter": Empty_Logging_Formatter}

# 默认格式
Formatter_Default = Formatter_Standard


def isValidFormatter(logFormatter):
    """
    判断日志样式格式化器是否合法有效
        在当前模块下已经定义了这些日志样式格式化器模板: `Formatter_Standard`, `Formatter_Raw`
        除此之外, 调用者也可以 参考 `Formatter_Standard` 自定义一个日志样式格式化器:
            一个字典类型, 其中必须有 `formatter`属性, 且值必须是 `Empty_Logging_Formatter`,
            其他则可按情况自定义
    """
    if not isinstance(logFormatter, dict):
        return False
    # `formatter` 属性值必须是空原生格式器
    if logFormatter.get("formatter") is not Empty_Logging_Formatter:
        return False
    return True


def isValidLogLevel(logLevel):
    """
    判断日志级别是否合法有效
        必须属于 `logging` 模块下的
        日志级别(CRITICAL|FATAL, ERROR, WARNING|WARN, INFO, DEBUG)
    """
    if (
        logLevel is logging.CRITICAL
        or logLevel is logging.ERROR
        or logLevel is logging.WARNING
        or logLevel is logging.INFO
        or logLevel is logging.DEBUG
    ):
        return True
    return False


def getLogger(**kwargs):
    """
    获取一个日志记录器(`logging.getLogger(logName)`)
        一个日志记录器可将日志内容记录到指定的记录源(控制台|文件)

    参数:
        kwargs {
            logName             日志记录器名 默认 `log`
            logFormatter        日志文件样  默认带日期格式的样式 `Formatter_Default`
            logLevel            日志记录级别 默认 `logging.DEBUG`
            logSource           日志记录源 将日志内容记录到指定的记录源(控制台|文件).
                                取值为: "console" 表示控制台, "${文件名|文件路径}" 表示记录到的指定文件.
                                默认 `log.log` 表示在当前脚本文件 `log.py` 的父级目录下的一个日志文件
            logFileEncoding     记录日志的文件编码 默认 `utf-8`
            logFileMode         记录日志的文件打开模式 默认: `a`
        }

    返回:
        日志记录器(logging.getLogger)
    """
    logName = "log"
    logFormatter = Formatter_Default
    logLevel = logging.DEBUG
    logSource = "log.log"
    logFileEncoding = "utf-8"
    logFileMode = "a"

    for key, value in kwargs.items():
        if key == "logName":
            if util.isNonEmptyStr(value):
                logName = value

        elif key == "logFormatter":
            if isValidFormatter(value):
                logFormatter = value

        elif key == "logLevel":
            if isValidLogLevel(value):
                logLevel = value

        elif key == "logSource":
            if util.isNonEmptyStr(value):
                logSource = value

        elif key == "logFileEncoding":
            if util.isNonEmptyStr(value):
                logFileEncoding = value

        elif key == "logFileMode":
            if util.isNonEmptyStr(value):
                logFileMode = value

    logger = logging.getLogger(logName)
    logger.setLevel(logging.DEBUG)

    if logSource.lower() == "console":
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logLevel)
        stream_handler.setFormatter(logFormatter["formatter"])
        logger.addHandler(stream_handler)
        return logger

    else:
        logFilePath = os.path.abspath(logSource)
        if util.isValidFilePath(logFilePath):
            file_handler = logging.FileHandler(
                logFilePath, encoding=logFileEncoding, mode=logFileMode
            )
            file_handler.setLevel(logLevel)
            file_handler.setFormatter(logFormatter["formatter"])
            logger.addHandler(file_handler)
            return logger

        else:
            print("illegal logSource `{0}`".format(logSource))
            return None


class Logger:
    """
    日志记录器
    """

    # 历史日志记录间隔时间类型: 每半小时/小时/天/周/月/季度/半年/年(FH|HH|DD|WW|MM|QY|HY|YY)
    # 在间隔时间内会在源日志文件内容后追加日志内容, 超过间隔时间后将重新创建目录和日志文件进行记录(默认: `DD`)
    __LogHistoryInterval_Types = ["FH", "HH", "DD", "WW", "MM", "QY", "HY", "YY"]
    # 计算记录历史日志的间隔时间(秒)
    __LogHistoryInterval_Times = [
        30 * 60 * 1.0,
        60 * 60 * 1.0,
        24 * 60 * 60 * 1.0,
        7 * 24 * 60 * 60 * 1.0,
        30 * 24 * 60 * 60 * 1.0,
        3 * 30 * 24 * 60 * 60 * 1.0,
        6 * 30 * 24 * 60 * 60 * 1.0,
        12 * 30 * 24 * 60 * 60 * 1.0,
    ]

    # 每一次记录日志输出时, 一次性输出的最高次数
    __Every_Log_Out_Max_Count = 10

    # 记录日志类型
    __LogTypes = ["debug", "info", "warn", "error"]

    # 日志是否记录到最底层栈
    __Bottom_Stack = False

    def __init__(self, **kwargs):
        """
        日志器构造

        参数:
            kwargs {
                logName                 日志记录器名称 默认 `log`
                logInConsole            是否在控制台记录日志 默认 `False`
                logInFile               是否在文件中记录日志 输出的日志文件会记录所有类型(debug|info|warn|error) 默认 `True`
                logInDebugFile          是否在调试文件中记录日志 输出的日志文件仅记录类型(debug). 默认 `False`
                logConsoleFormatter     日志控制台样式 默认带日期格式的样式 `Formatter_Default`
                logFileFormatter        日志文件样式 默认带日期格式的样式 `Formatter_Default`
                logDebugFileFormatter   调试日志文件样式 默认带日期格式的样式 `Formatter_Default`
                logLevel                日志记录级别(全局级别 控制台日志, 文件日志, 调试文件日志均适用) 默认 `logging.DEBUG`
                logConsoleLevel         控制台日志级别 默认 `logLevel`
                logFileLevel            文件日志级别 默认 `logLevel`
                logDebugFileLevel       调试文件日志级别 默认 `logLevel`
                logRootDir              日志根目录 默认 `当前脚本文件父级目录(向上2级)\logs`
                logFileName             日志文件名 默认 `log.log`
                logDebugFileName        调试日志文件名 默认 `debug.log`
                logFileEncoding         记录日志的文件(日志文件和调试日志文件)编码 默认 `utf-8`
                logToHistory            是否将当前日志记录同步记录到历史文件中 默认 `True`
                logHistoryRecordType    历史日志记录类型: 每半小时/小时/天/周/月/季度/半年/年(FH|HH|DD|WW|MM|QY|HY|YY).
                                        记录到一个历史日志文件间隔时间, 超过这个时间间隔将重新创建目录(以当前时间作为目录名称)和日志文件进行记录.
                                        当且仅当 `logToHistory` 为 `True`时有效 默认 `DD`
            }
        """
        logName = "log"
        logInConsole = False
        logInFile = True
        logInDebugFile = False
        logConsoleFormatter = Formatter_Default
        logFileFormatter = Formatter_Default
        logDebugFileFormatter = Formatter_Default
        logLevel = logging.DEBUG
        logConsoleLevel = None
        logFileLevel = None
        logDebugFileLevel = None        
        logRootDir = None
        logFileName = "log.log"
        logDebugFileName = "debug.log"
        logFileEncoding = "utf-8"
        # 每记录一次日志文件时, 都会将原有的日志内容覆盖掉
        logFileMode = "w"
        logToHistory = True
        logHistoryRecordType = "DD"
        logHistoryRecordTypeIndex = 2

        for key, value in kwargs.items():
            if key == "logName":
                if util.isNonEmptyStr(value):
                    logName = value

            elif key == "logInConsole":
                if value:
                    logInConsole = True

            elif key == "logInFile":
                if not value:
                    logInFile = False

            elif key == "logInDebugFile":
                if value:
                    logInDebugFile = True

            elif key == "logConsoleFormatter":
                if isValidFormatter(value):
                    logConsoleFormatter = value

            elif key == "logFileFormatter":
                if isValidFormatter(value):
                    logFileFormatter = value

            elif key == "logDebugFileFormatter":
                if isValidFormatter(value):
                    logDebugFileFormatter = value

            elif key == "logLevel":
                if isValidLogLevel(value):
                    logLevel = value

            elif key == "logConsoleLevel":
                if isValidLogLevel(value):
                    logConsoleLevel = value

            elif key == "logFileLevel":
                if isValidLogLevel(value):
                    logFileLevel = value

            elif key == "logDebugFileLevel":
                if isValidLogLevel(value):
                    logDebugFileLevel = value

            elif key == "logRootDir":
                if util.isValidDir(value):
                    logRootDir = os.path.abspath(value)
                else:
                    print("illegal logRootDir: ", value)

            elif key == "logFileName":
                if util.isNonEmptyStr(value):
                    logFileName = value

            elif key == "logDebugFileName":
                if util.isNonEmptyStr(value):
                    logDebugFileName = value

            elif key == "logFileEncoding":
                logFileEncoding = value

            elif key == "logToHistory":
                if not value:
                    logToHistory = False

            elif key == "logHistoryRecordType":
                _logHistoryRecordTypeIndex = self.__getLogHistoryIntervalTypeIndex(
                    value
                )
                if _logHistoryRecordTypeIndex != -1:
                    logHistoryRecordType = value
                    logHistoryRecordTypeIndex = _logHistoryRecordTypeIndex

        if logRootDir is None:
            logRootDir = os.path.join(util.getParentDir(util.getEntryExePath(), 2), "logs")

        logger_console = None
        if logInConsole:
            if logConsoleLevel is None:
                logConsoleLevel = logLevel
            logger_console = getLogger(
                logName=logName + "_console",
                logFormatter=logConsoleFormatter,
                logLevel=logConsoleLevel,
                logSource="console",
            )

        logger_file = None
        if logInFile:
            if logFileLevel is None:
                logFileLevel = logLevel
            logFilePath = os.path.join(logRootDir, "log", logFileName)
            logger_file = getLogger(
                logName=logName + "_file",
                logFormatter=logFileFormatter,
                logLevel=logFileLevel,
                logSource=logFilePath,
                logFileEncoding=logFileEncoding,
                logFileMode=logFileMode,
            )

        logger_debug_file = None
        if logInDebugFile:
            if logDebugFileLevel is None:
                logDebugFileLevel = logLevel
            logDebugFilePath = os.path.join(logRootDir, "log", logDebugFileName)
            logger_debug_file = getLogger(
                logName=logName + "_debug_file",
                logFormatter=logDebugFileFormatter,
                logLevel=logDebugFileLevel,
                logSource=logDebugFilePath,
                logFileEncoding=logFileEncoding,
                logFileMode=logFileMode,
            )

        self.__logName = logName
        self.__logInConsole = logInConsole
        self.__logInFile = logInFile
        self.__logInDebugFile = logInDebugFile
        self.__logConsoleFormatter = logConsoleFormatter
        self.__logFileFormatter = logFileFormatter
        self.__logDebugFileFormatter = logDebugFileFormatter
        self.__logFileLevel = logFileLevel
        self.__logDebugFileLevel = logDebugFileLevel
        self.__logRootDir = logRootDir
        self.__logFileName = logFileName
        self.__logDebugFileName = logDebugFileName
        self.__logFileEncoding = logFileEncoding
        self.__logToHistory = logToHistory
        self.__logHistoryRecordTypeIndex = logHistoryRecordTypeIndex
        self.__logger_console = logger_console
        self.__logger_file = logger_file
        self.__logger_debug_file = logger_debug_file
        # 日志记录次数(外部每调用1次 `debug|info|warn|error` 方法, 均累加1次)
        self.__logCount = 0

    def __getLogHistoryIntervalTypeIndex(self, logHistoryRecordType):
        """
        获取 `logHistoryRecordType` 在 `__LogHistoryInterval_Types` 中的索引
        """
        for index in range(len(Logger.__LogHistoryInterval_Types)):
            __LogHistoryInterval_Type = Logger.__LogHistoryInterval_Types[index]
            if __LogHistoryInterval_Type == logHistoryRecordType:
                return index
        return -1

    @property
    def logConsoleFormatter(self):
        return self.__logConsoleFormatter

    @logConsoleFormatter.setter
    def logConsoleFormatter(self, value):
        """
        设置输出到控制台的日志样式格式化器
        """
        if isValidFormatter(value):
            self.__logConsoleFormatter = value

    @property
    def logFileFormatter(self):
        return self.__logFileFormatter

    @logFileFormatter.setter
    def logFileFormatter(self, value):
        """
        设置输出到文件的日志样式格式化器
        """
        if isValidFormatter(value):
            self.__logFileFormatter = value

    def __getLogCallFrame(self, top=True):
        """
        获取日志运行时的堆栈信息

        参数:
            top     是否是最上层的调用堆栈
        """
        # 获取运行时堆栈
        outerFrames = inspect.getouterframes(inspect.currentframe())
        # `outerFrames` 第1个元素为当前代码行 `outerFrames = inspect.getouterframes(inspect.currentframe())`
        # 最上层日志调用处信息为 日志方法 `debug|info|warn|error`的上一个堆栈 为第5个元素
        # 最底层日志调用处信息为 方法 `__log` 下的 代码行 `formatMsg_file = self.__getFormatMsg(logType, logFileFormatter, msg)` 为第3个元素
        if top:
            return outerFrames[4]
        else:
            return outerFrames[2]

    def __getFormatMsg(self, logType, logFormatter, msg):
        """
        获取日志格式化后的消息内容
        """
        if logFormatter is Formatter_Raw:
            return msg
        msgFormat = logFormatter.get("msgFormat")
        if not util.isNonEmptyStr(msgFormat):
            return msg

        formatDict = {}
        if msgFormat.find("{asctime}") != -1:
            # 获取当前时间并格式化
            nowTime = datetime.now()
            nowTimeFormat = nowTime.strftime("%Y-%m-%d %H:%M:%S")
            nowTimeFormat += "," + str(nowTime.microsecond // 1000)
            formatDict["asctime"] = nowTimeFormat

        filename_index = msgFormat.find("{filename}")
        lineno_index = msgFormat.find("{lineno}")
        levelname_index = msgFormat.find("{levelname}")
        if filename_index != -1 or lineno_index != -1 or levelname_index != -1:
            logTopLevel = logFormatter.get("logTopLevel")
            callFrame = self.__getLogCallFrame(logTopLevel)
            if filename_index != -1:
                formatDict["filename"] = os.path.basename(callFrame.filename)
            if lineno_index != -1:
                formatDict["lineno"] = callFrame.lineno
            if levelname_index != -1:
                formatDict["levelname"] = logType.upper()

        if msgFormat.find("{message}") != -1:
            formatDict["message"] = msg
        return msgFormat.format(**formatDict)

    def __getErrorStack(self, catchExceptionType):
        """
        获取异常堆栈信息

        参数:
            catchExceptionType      捕获的异常类型

        返回:
            捕获的异常堆栈信息(从最外层的程序入口到捕获的异常所对应的代码位置)
        """
        format_stack = traceback.format_stack()
        format_exception = traceback.format_exception(catchExceptionType)
        format_exception_len = len(format_exception)
        exceptionOfStacks = []
        exceptionOfStacks.append(format_exception[0])
        exceptionOfStacks.append(format_stack[0])
        i = 1
        while i < format_exception_len:
            exceptionOfStacks.append(format_exception[i])
            i += 1
        return "".join(exceptionOfStacks)

    def __getStackContent(self, logType, logStack, errorType, errorStack):
        """
        获取堆栈内容
        """
        stackContent = ""
        if logStack:
            formatStacks = traceback.format_stack()
            # 日志的堆栈 最上层是最外层的程序入口, 最底层是 代码行 `formatStacks = traceback.format_stack()`
            # 的地方 `debug|info|warn|error`
            # 该地方是当前方法的上一层方法, 截取堆栈信息时应截止到到倒数第二个元素
            logFormatStacks = []
            if Logger.__Bottom_Stack:
                for i in range(0, len(formatStacks)):
                    logFormatStacks.append(formatStacks[i])
            else:
                # 最底层堆栈 截止到倒数第二个元素 即代码行 `self.__log(Logger.__LogTypes[1], msg, *args, **kwargs)`
                for i in range(0, len(formatStacks) - 2):
                    logFormatStacks.append(formatStacks[i])
            stackContent += "\n" + "".join(logFormatStacks)
        if logType == "error" and isinstance(errorType, BaseException) and errorStack:
            stackContent += "\n" + self.__getErrorStack(errorType)
        return stackContent

    def __loggingRecord(self, logger, logType, msg, logOutCount):
        """
        记录日志(调用底层logging)

        参数:
            logger      日志记录器(`logging.getLogger(logName)`)
            msg         日志消息内容
            logOutCount 日志输出次数
        """
        if logType not in Logger.__LogTypes:
            logType = Logger.__LogTypes[1]

        for i in range(logOutCount):
            if logType == Logger.__LogTypes[0]:
                logger.debug(msg)
            elif logType == Logger.__LogTypes[1]:
                logger.info(msg)
            elif logType == Logger.__LogTypes[2]:
                logger.warn(msg)
            elif logType == Logger.__LogTypes[3]:
                logger.error(msg)

    def __scanLogHisotrySubDir(self):
        """
        扫描历史日志目录(/logs/history)
            只扫描这种日期格式的子文件夹: `YY-MM-DD HH-mm-ss`

        返回:
            扫描到的距离当前日期最近的日志文件夹路, 距离当前的时间差(秒)
            ```
            scanLatestDirpath, timeDistance
            ```
        """
        logHistoryDir = os.path.join(self.__logRootDir, "history")
        if not (os.path.exists(logHistoryDir) and os.path.isdir(logHistoryDir)):
            return None, None
        maxTime = 0
        maxTimeSubFilePath = ""

        nowTime = datetime.now()
        for subFileName in os.listdir(logHistoryDir):
            subFilePath = logHistoryDir + "\\" + subFileName
            if os.path.isdir(subFilePath):
                try:
                    timeObj = datetime.strptime(subFileName, "%Y-%m-%d %H-%M-%S")
                    if timeObj < nowTime:
                        if maxTime == 0:
                            maxTime = timeObj
                            maxTimeSubFilePath = subFilePath
                        elif timeObj > maxTime:
                            maxTime = timeObj
                            maxTimeSubFilePath = subFilePath
                except ValueError:
                    pass

        if maxTimeSubFilePath != "":
            return maxTimeSubFilePath, (nowTime - maxTime).total_seconds()
        else:
            return None, None

    def __logHistoryInit(self):
        """
        记录历史日志初始化
        """
        logHisotrySubDir, timeDistance = self.__scanLogHisotrySubDir()
        createSubDir = False
        if (
            logHisotrySubDir is None
            or timeDistance
            > Logger.__LogHistoryInterval_Times[self.__logHistoryRecordTypeIndex]
        ):
            createSubDir = True
            logHisotrySubDir = os.path.join(
                self.__logRootDir,
                "history",
                time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()),
            )
            util.mkdirs(logHisotrySubDir)

        logFilePath_history = os.path.join(logHisotrySubDir, self.__logFileName)
        logger_history = getLogger(
            logName=self.__logName + "_history",
            logFormatter=self.__logFileFormatter,
            logLevel=self.__logFileLevel,
            logSource=logFilePath_history,
            logFileEncoding=self.__logFileEncoding,
        )

        logDebugFilePath_history = os.path.join(
            logHisotrySubDir, self.__logDebugFileName
        )
        logger_debug_history = None
        if self.__logInDebugFile:
            logger_debug_history = getLogger(
                logName=self.__logName + "_debug_history",
                logFormatter=self.__logDebugFileFormatter,
                logLevel=self.__logDebugFileLevel,
                logSource=logDebugFilePath_history,
                logFileEncoding=self.__logFileEncoding,
            )

        # 未创建文件夹时, 会直接在原日志文件后追加内容, 追加前空两行
        if not createSubDir:
            self.__loggingRecord(logger_history, "", "", 2)
            if logger_debug_history:
                self.__loggingRecord(logger_debug_history, "", "", 2)

        self.__logger_history = logger_history
        self.__logger_debug_history = logger_debug_history

    def __log(self, logType, msg, *args, **kwargs):
        """
        记录日志

        参数:
            logType                     日志类型 `__LogTypes` debug|info|warn|error
            msg                         日志消息内容 非字符串类型会转为字符串处理
            args                        元组参数 `msg` 的占位符参数
            kwargs {                    动态参数
                logConsoleFormatter     日志控制台样式
                logFileFormatter        日志文件样式
                logDebugFileFormatter   调试日志文件样式
                logInConsole            是否在控制台中记录日志(当且仅当属性 `logInConsole` 为 `True` 时有效) 默认 `True`
                logInFile               是否在文件中记录日志(当且仅当属性 `logInFile` 为 `True` 时有效) 默认 `True`
                logInDebugFile          是否在调试日志文件中记录日志(当且仅当属性 `logInDebugFile` 为 `True` 时才有效) 默认 `True`
                logOnlyInDebugFile      只在调试文件中记录(当且仅当属性 `logInDebugFile` 为 `True` 且日志类型为 `debug` 时有效).
                                        默认 `False`, 即在日志文件 `log.log` 和 调试日志文件中 `debug.log` 都记录调试日志
                logStack                是否显示日志堆栈信息(从底层的日志调用处(调用代码 `traceback.format_stack()`位置)
                                        到最上层的程序启动入口堆栈) 默认 `False`
                errorType               异常类型 从捕获处传递的异常类型
                errorStack              是否显示异常堆栈信息(当且仅当 `logType` 为 `error`, 且 `errorType`有值时有效) 默认 `True`
                raw                     是否按原生的 `msg` 输出(不带日志格式样式) 默认 `False`
                logCount                日志输出次数 默认 `1`
            }
            注意:
                `kwargs` 为动态参数, 接收时会按以上键值对解包, 剩余的键值对一律按格式化 `msg` 的占位符处理
        """
        # 累加1次日志记录次数
        self.__logCount += 1
        logConsoleFormatter = self.__logConsoleFormatter
        logFileFormatter = self.__logFileFormatter
        logDebugFileFormatter = self.__logDebugFileFormatter
        logInConsole = True
        logInFile = True
        logInDebugFile = True
        logOnlyInDebugFile = False
        logStack = False
        errorType = None
        errorStack = True
        raw = False
        logOutCount = 1

        # 动态参数中的常规键
        generalKeys = []
        for key, value in kwargs.items():
            if key == "logConsoleFormatter":
                if isValidFormatter(value):
                    logConsoleFormatter = value
                generalKeys.append(key)

            elif key == "logFileFormatter":
                if isValidFormatter(value):
                    logFileFormatter = value
                generalKeys.append(key)

            elif key == "logDebugFileFormatter":
                if isValidFormatter(value):
                    logDebugFileFormatter = value
                generalKeys.append(key)

            elif key == "logInConsole":
                if not value:
                    logInConsole = False
                generalKeys.append(key)

            elif key == "logInFile":
                if not value:
                    logInFile = False
                generalKeys.append(key)

            elif key == "logInDebugFile":
                if not value:
                    logInDebugFile = False
                generalKeys.append(key)

            elif key == "logOnlyInDebugFile":
                if value:
                    logOnlyInDebugFile = True
                generalKeys.append(key)

            elif key == "logCount":
                if isinstance(value, int) and value > 1:
                    if value > Logger.__Every_Log_Out_Max_Count:
                        value = Logger.__Every_Log_Out_Max_Count
                    logOutCount = value
                generalKeys.append(key)

            if key == "logStack":
                if isinstance(value, bool) and value:
                    logStack = True
                generalKeys.append(key)

            if key == "errorType":
                if isinstance(value, Exception):
                    errorType = value
                generalKeys.append(key)

            if key == "errorStack":
                if isinstance(value, bool) and not value:
                    errorStack = False
                generalKeys.append(key)

            if key == "raw":
                if isinstance(value, bool) and value:
                    raw = True
                generalKeys.append(key)

        # 传递的动态参数中, 常规键赋值给了变量, 要进行删除, 剩余的键当做格式化 日志消息内容 `msg` 的占位符处理
        for generalKey in generalKeys:
            del kwargs[generalKey]

        # 非字符串类型会转为字符串处理
        if not isinstance(msg, str):
            msg = "{0}".format(msg)

        # 注意: 如果 `msg` 为 JSON字符串, `args` 和 `kwargs`应均设置为空,
        # 否则在进行字符串占位符格式化时会报错
        if len(args) > 0 or len(kwargs.keys()) > 0:
            msg = msg.format(*args, **kwargs)
        formatMsg_file = self.__getFormatMsg(logType, logFileFormatter, msg)
        stackContent = self.__getStackContent(logType, logStack, errorType, errorStack)

        if self.__logInConsole and logInConsole:
            consoleFormatMsg = msg
            if raw != True:
                consoleFormatMsg = (
                    formatMsg_file
                    if logConsoleFormatter == logFileFormatter
                    else self.__getFormatMsg(logType, logConsoleFormatter, msg)
                )
                consoleFormatMsg += stackContent
            self.__loggingRecord(
                self.__logger_console, logType, consoleFormatMsg, logOutCount
            )

        if self.__logInFile and logInFile and not logOnlyInDebugFile:
            fileFormatMsg = msg
            if raw != True:
                fileFormatMsg = formatMsg_file
                fileFormatMsg += stackContent
            self.__loggingRecord(
                self.__logger_file, logType, fileFormatMsg, logOutCount
            )
            if self.__logToHistory:
                if self.__logCount == 1:
                    self.__logHistoryInit()
                self.__loggingRecord(
                    self.__logger_history, logType, fileFormatMsg, logOutCount
                )

        if logType == Logger.__LogTypes[0] and (
            self.__logInDebugFile and logInDebugFile
        ):
            debugFileFormatMsg = msg
            if raw != True:
                debugFileFormatMsg = (
                    formatMsg_file
                    if logDebugFileFormatter == logFileFormatter
                    else self.__getFormatMsg(logType, logDebugFileFormatter, msg)
                )
                debugFileFormatMsg += stackContent
            self.__loggingRecord(
                self.__logger_debug_file, logType, debugFileFormatMsg, logOutCount
            )
            if self.__logToHistory:
                if self.__logCount == 1:
                    self.__logHistoryInit()
                self.__loggingRecord(
                    self.__logger_debug_history,
                    logType,
                    debugFileFormatMsg,
                    logOutCount,
                )

    def debug(self, msg, *args, **kwargs):
        """
        记录调试日志

        参数:
            msg                         日志消息内容 非字符串类型会转为字符串处理
            args                        元组参数 `msg` 的占位符参数
            kwargs {                    动态参数
                logConsoleFormatter     日志控制台样式
                logFileFormatter        日志文件样式
                logDebugFileFormatter   调试日志文件样式
                logInConsole            是否在控制台中记录日志(当且仅当属性 `logInConsole` 为 `True` 时有效). 默认 `True`
                logInFile               是否在文件中记录日志(当且仅当属性 `logInFile` 为 `True` 时有效). 默认 `True`
                logInDebugFile          是否在调试日志文件中记录日志(当且仅当属性 `logInDebugFile` 为 `True` 时有效). 默认 `True`
                logOnlyInDebugFile      只在调试文件中记录(当且仅当属性 `logInDebugFile` 为 `True` 时有效).
                                        默认 `False`, 即在日志文件 `log.log` 和 调试日志文件中 `debug.log` 都记录
                logStack                是否显示日志堆栈信息(从底层的日志调用处(调用代码 `traceback.format_stack()`位置)
                                        到最上层的程序启动入口堆栈). 默认 `False`
                raw                     是否按原生的 `msg` 输出(不带日志格式样式). 默认 `False`
                logCount                日志输出次数. 默认 `1`
            }
        """
        self.__log(Logger.__LogTypes[0], msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        记录信息日志

        参数:
            msg                         日志消息内容 非字符串类型会转为字符串处理
            args                        元组参数 `msg` 的占位符参数
            kwargs {                    动态参数
                logConsoleFormatter     日志控制台样式
                logFileFormatter        日志文件样式
                logInConsole            是否在控制台中记录日志(当且仅当属性 `logInConsole` 为 `True` 时有效). 默认 `True`
                logInFile               是否在文件中记录日志(当且仅当属性 `logInFile` 为 `True` 时有效). 默认 `True`
                logStack                是否显示日志堆栈信息(从底层的日志调用处(调用代码 `traceback.format_stack()`位置)
                                        到最上层的程序启动入口堆栈). 默认 `False`
                raw                     是否按原生的 `msg` 输出(不带日志格式样式). 默认 `False`
                logCount                日志输出次数. 默认 `1`
            }
        """
        self.__log(Logger.__LogTypes[1], msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        """
        记录警告日志

        参数:
            msg                         日志消息内容 非字符串类型会转为字符串处理
            args                        元组参数 `msg` 的占位符参数
            kwargs {                    动态参数
                logConsoleFormatter     日志控制台样式
                logFileFormatter        日志文件样式
                logInConsole            是否在控制台中记录日志(当且仅当属性 `logInConsole` 为 `True` 时有效). 默认 `True`
                logInFile               是否在文件中记录日志(当且仅当属性 `logInFile` 为 `True` 时有效). 默认 `True`
                logStack                是否显示日志堆栈信息(从底层的日志调用处(调用代码 `traceback.format_stack()`位置)
                                        到最上层的程序启动入口堆栈). 默认 `False`
                raw                     是否按原生的 `msg` 输出(不带日志格式样式). 默认 `False`
                logCount                日志输出次数. 默认 `1`
            }
        """
        self.__log(Logger.__LogTypes[2], msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        记录错误日志

        参数:
            msg                         日志消息内容 非字符串类型会转为字符串处理
            args                        元组参数 `msg` 的占位符参数
            kwargs {                    动态参数
                logConsoleFormatter     日志控制台样式
                logFileFormatter        日志文件样式
                logInConsole            是否在控制台中记录日志(当且仅当属性 `logInConsole` 为 `True` 时有效). 默认 `True`
                logInFile               是否在文件中记录日志(当且仅当属性 `logInFile` 为 `True` 时有效). 默认 `True`
                logStack                是否显示日志堆栈信息(从底层的日志调用处(调用代码 `traceback.format_stack()`位置)
                                        到最上层的程序启动入口堆栈). 默认 `False`
                errorType               异常类型 从捕获处的传递的异常类型
                errorStack              是否显示异常堆栈信息(当且仅当 `logType` 为 `error`, 且 `errorType`有值时有效). 默认 `True`
                raw                     是否按原生的 `msg` 输出(不带日志格式样式). 默认 `False`
                logCount                日志输出次数. 默认 `1`
            }
        """
        self.__log(Logger.__LogTypes[3], msg, *args, **kwargs)
