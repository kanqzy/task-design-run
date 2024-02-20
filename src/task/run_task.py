import json
import os
import re
import traceback

from debug import tprint
import log
import logger
import util

import application
import common
import file
import mouse
import keyInput
import qq

ExcuteFilePath = util.getEntryExePath()

# 应用程序根目录(可执行文件位于根目录下的 `bin` 目录下)
AppRootDir = util.getParentDir(ExcuteFilePath, 3)
# LOGGER = log.Logger(logRootDir=AppRootDir + "\\logs", logInConsole=True)
# LOGGER = log.Logger(logInConsole=True, logRootDir=AppRootDir + "\\logs")
LOGGER = logger.getCustomLogger(
    AppRootDir + "\\logs", logInConsole=True, logConsoleFormatter=log.Formatter_Default
)

Err_Log_Formatter = {
    "formatter": log.Empty_Logging_Formatter,
    "msgFormat": "{asctime} - [Task Error]: {message}",
}

# 函数库JSON数据
## basic
Function_Common_Json_Data = json.loads(
    util.readContent(os.path.abspath("./task/function/json/basic/common.json"))
)
Function_File_Json_Data = json.loads(
    util.readContent(os.path.abspath("./task/function/json/basic/file.json"))
)

## ui
Function_Mouse_Json_Data = json.loads(
    util.readContent(os.path.abspath("./task/function/json/ui/mouse.json"))
)
Function_KeyInput_Json_Data = json.loads(
    util.readContent(os.path.abspath("./task/function/json/ui/keyInput.json"))
)

## app
Function_Application_Json_Data = json.loads(
    util.readContent(os.path.abspath("./task/function/json/app/application.json"))
)
Function_QQ_Json_Data = json.loads(
    util.readContent(os.path.abspath("./task/function/json/app/qq.json"))
)


class Express:
    """
    表达式
    """

    def __init__(
        self, name: str, value: object = None, express=None, args: list = None
    ):
        """
        参数:
            name (str): 表达式运算名称 arg|const|var|+|-|...(任务入参|常量|变量名|加|减等)
            value (object): 表达式的值
            express (Express): 表达式中的表达式
                通常, 一个参数运算会使用当前参数,
                例如 `str(a)`, `a` 为最外层表达式 `str`嵌套的表达式
            args (list<dict>): 表达式参数
                数据结构: [
                    {
                        name: str,
                        value: object,
                        express: Express
                    },
                    ...
                ]
        """
        self.name = name
        self.value = value
        self.express: Express = express
        self.args = args

    def hasArgs(self) -> bool:
        return isinstance(self.args, list) and len(self.args) > 0

    @classmethod
    def parseFromDict(cls, dictData: dict):
        name = dictData["name"]
        value = dictData.get("value")
        express = dictData.get("express")
        args = dictData.get("args")
        if args is None or len(args) == 0:
            parsed_express = None
            if express:
                parsed_express = cls.parseFromDict(express)
            return Express(name, value, parsed_express)

        parsed_args = []
        for arg in args:
            arg_name = arg["name"]
            arg_value = arg.get("value")
            arg_express = arg.get("express")
            parsed_arg = None
            if arg_express is None:
                parsed_arg = {"name": arg_name, "value": arg_value}
            else:
                parsed_arg = {
                    "name": arg_name,
                    "express": cls.parseFromDict(arg_express),
                }
            parsed_args.append(parsed_arg)

        return Express(name, value, args=parsed_args)

    def toDict(self) -> dict:
        tprint("Express toDict into ...", enable=False)
        tprint("self: ", self, enable=False)
        tprint("self name, value: ", self.name, self.value, enable=False)
        tprint("self.express: ", self.express, enable=False)
        tprint(enable=False)

        dictData = {
            "name": self.name,
            "value": self.value,
            "express": self.express.toDict() if self.express else None,
        }
        if self.hasArgs():
            arg_dictDatas = []
            for arg in self.args:
                arg_dictData = {
                    "name": arg["name"],
                    "value": arg.get("value"),
                }
                arg_express: Express = arg.get("express")
                if arg_express is not None:
                    arg_dictData["express"] = arg_express.toDict()
                arg_dictDatas.append(arg_dictData)
            dictData["args"] = arg_dictDatas
            return dictData

        else:
            return dictData


class ParameterType:
    """
    函数参数类型(形参)
    """

    def __init__(
        self,
        name: str,
        type: str,
        text: str,
        required: bool = None,
        description: str = None,
        default: object = None,
    ):
        self.name = name
        self.type = type
        self.text = text
        self.required = required
        self.description = description
        self.default = default

    @classmethod
    def parseFromDict(cls, dictData: dict):
        name = dictData.get("name")
        type = dictData.get("type")
        text = dictData.get("text")
        required = dictData.get("required")
        description = dictData.get("description")
        default = dictData.get("default")
        parameterType = ParameterType(name, type, text, required, description, default)
        return parameterType

    @classmethod
    def parseListFromData(cls, args: list) -> list:
        parameterTypes = []
        for arg in args:
            parameterType = cls.parseFromDict(arg)
            parameterTypes.append(parameterType)
        return parameterTypes

    def toDict(self) -> dict:
        selfDict = vars(self)
        newDcit = dict(selfDict)
        newDcit["name"] = newDcit["name"]
        newDcit["text"] = newDcit["text"]
        newDcit["description"] = newDcit["description"]
        return newDcit


def get_function_parameterTypes(url: str) -> list[ParameterType]:
    json_data = []
    # basic
    json_data.extend(Function_Common_Json_Data)
    json_data.extend(Function_File_Json_Data)

    # ui
    json_data.extend(Function_Mouse_Json_Data)
    json_data.extend(Function_KeyInput_Json_Data)

    # app
    json_data.extend(Function_Application_Json_Data)
    json_data.extend(Function_QQ_Json_Data)

    params = None
    for function in json_data:
        if url and url == function["url"]:
            params = function["params"]
            break
    if params is None:
        return None
    parameterTypes = []
    for param in params:
        parameterType = ParameterType.parseFromDict(param)
        parameterTypes.append(parameterType)
    return parameterTypes


class Parameter:
    """
    函数参数(实参)
    """

    def __init__(
        self, type: ParameterType, value: object = None, express: Express = None
    ):
        # 初始传入的属性
        self.type = type
        self.value = value
        self.express = express

        # 后续计算的属性
        ## 参数为表达式时计算的值
        self._cacValue = None
        ## 解析的其它数据
        self._parsedData = {}

    def cacValue(self, task):
        self._cacValue = expressCac(task, self.express)

    def getValue(self):
        if self._cacValue is not None:
            return self._cacValue
        return self.value

    @classmethod
    def _parseListFromData(cls, args: list, url: str, taskFilePath: str = None) -> list:
        """
        参数:
            taskFilePath (str): 当前参数所在的任务文件路径
        """
        args_len = len(args)
        parameterTypes = get_function_parameterTypes(url)
        parameterTypes_len = len(parameterTypes)

        # while和if~else语句块, 作为函数参数解析时,
        # 第1个参数是条件判断, 第2个参数是 `blocks` 属性下的 `action` 或 `elseaction` 流块

        if args_len < parameterTypes_len:
            LOGGER.error(
                "url `{0}`: args length {1} less than parameterTypes length {2}",
                url,
                args_len,
                parameterTypes_len,
            )
            return None

        parameters = []
        i = 0
        while i < parameterTypes_len:
            parameterType: ParameterType = parameterTypes[i]
            arg = args[i]
            arg_name = arg.get("name")
            if arg_name != parameterType.name:
                LOGGER.error(
                    "arg_name `{0}` not match with parameterType `{1}`: name not equal",
                    arg_name,
                    parameterType,
                )
                return None

            arg_value = arg.get("value")
            arg_express_data = arg.get("express")

            arg_express = None
            if arg_express_data is not None:
                arg_express = Express.parseFromDict(arg_express_data)

            parameter = Parameter(parameterType, arg_value, arg_express)
            parameters.append(parameter)
            i += 1

        # 调用其它任务(/agerun/common/flow), 形参只有1个, 实参1个以上, 后面跟随的是调用的任务入参
        if url == "/agerun/common/flow":
            ## 在当前任务文件所在的目录下, 以1个参数的值作为任务文件路径名(不带后缀名), 查找对应的任务文件
            firstParameter: Parameter = parameters[0]
            taskDir = os.path.dirname(taskFilePath)
            referTaskFilePath = os.path.join(taskDir, firstParameter.value + ".json")
            if not util.isFile(referTaskFilePath):
                raise Exception(
                    "illegal refer task value `{0}: refer task file `{1}` not found`".format(
                        firstParameter.value, referTaskFilePath
                    )
                )
            referTaskFilePath = os.path.abspath(referTaskFilePath)
            referTaskJsonData = json.loads(util.readContent(referTaskFilePath).strip())

            tprint("referTaskJsonData args: ", referTaskJsonData["args"], enable=False)

            referTaskParameterTypes = ParameterType.parseListFromData(
                referTaskJsonData["args"]
            )
            referTaskParameterTypes_dict = [
                argType.toDict() for argType in referTaskParameterTypes
            ]

            tprint(
                "referTaskParameterTypes_dict: ",
                referTaskParameterTypes_dict,
                enable=False,
            )

            referTaskParameterTypes_len = len(referTaskParameterTypes)
            if args_len - 1 != referTaskParameterTypes_len:
                raise Exception(
                    "illegal refer task args : length {0} not equal to declare argTypes length {1}".format(
                        args_len - 1, referTaskParameterTypes_len
                    )
                )
            referTask = {
                "jsonPath": referTaskFilePath,
                "jsonData": referTaskJsonData,
                "argTypes": referTaskParameterTypes,
            }
            firstParameter._parsedData["referTask"] = referTask

            i = 1
            while i < args_len:
                arg = args[i]
                parameterType: ParameterType = referTaskParameterTypes[i - 1]
                arg_name = arg.get("name")
                if arg_name != parameterType.name:
                    LOGGER.error(
                        "arg_name `{0}` not match with parameterType `{1}`: name not equal",
                        arg_name,
                        parameterType,
                    )
                    return None

                arg_value = arg.get("value")
                arg_express_data = arg.get("express")

                arg_express = None
                if arg_express_data is not None:
                    arg_express = Express.parseFromDict(arg_express_data)

                parameter = Parameter(parameterType, arg_value, arg_express)
                parameters.append(parameter)

                i += 1

        return parameters

    @classmethod
    def parseListFromArgs(cls, args: list, parameterTypes: list):
        args_len = len(args)
        if args_len == 0:
            return []

        parameters = []
        i = 0
        while i < args_len:
            parameterType: ParameterType = parameterTypes[i]
            arg = args[i]
            arg_name = arg.get("name")
            if arg_name != parameterType.name:
                LOGGER.error(
                    "arg_name `{0}` not match with parameterType `{1}`: name not equal",
                    arg_name,
                    parameterType,
                )
                return None

            arg_value = arg.get("value")
            arg_express_data = arg.get("express")

            arg_express = None
            if arg_express_data is not None:
                arg_express = Express.parseFromDict(arg_express_data)

            parameter = Parameter(parameterType, arg_value, arg_express)
            parameters.append(parameter)
            i += 1

        return parameters

    @classmethod
    def parseListFromData(cls, taskFilePath: str, taskBlockData: dict) -> list:
        url = taskBlockData["url"]
        args: list[Parameter] = taskBlockData["args"]

        args_len = len(args)
        parameterTypes = get_function_parameterTypes(url)
        parameterTypes_len = len(parameterTypes)

        if url == "/agerun/common/while":
            firstParameter: Parameter = cls.parseListFromArgs(args, parameterTypes)[0]

            # while 语句 作为函数参数解析时, 第1个参数是条件判断, 第2个参数是 `blocks` 属性下的 `action` 流块
            actionParameters = []
            actionDatas = taskBlockData["blocks"]["action"]
            for actionData in actionDatas:
                parameter = cls.parseListFromData(taskFilePath, actionData)
                actionParameters.append(parameter)

            secondParameter = Parameter(
                parameterTypes[1], value={"action": actionParameters}
            )

            return [firstParameter, secondParameter]

        elif url == "/agerun/common/if":
            firstParameter: Parameter = cls.parseListFromArgs(args, parameterTypes)[0]

            # if~else 语句 作为函数参数解析时, 第1个参数是条件判断,
            #   第2和第3个参数分别是 `blocks` 属性下的 `action` 和 `elseAction` 流块
            actionParameters = []
            actionDatas = taskBlockData["blocks"]["action"]
            for actionData in actionDatas:
                parameter = cls.parseListFromData(taskFilePath, actionData)
                actionParameters.append(parameter)

            elseActionParameters = []
            elseActionDatas = taskBlockData["blocks"].get("elseAction")
            if elseActionDatas:
                for elseActionData in elseActionDatas:
                    parameter = cls.parseListFromData(taskFilePath, elseActionData)
                    elseActionParameters.append(parameter)

            secondParameter = Parameter(
                parameterTypes[1], value={"action": actionParameters}
            )

            if len(elseActionParameters) > 0:
                thirdParameter = Parameter(
                    parameterTypes[2], value={"elseAction": elseActionParameters}
                )
                return [firstParameter, secondParameter, thirdParameter]
            else:
                return [firstParameter, secondParameter]

        elif url == "/agerun/common/flow":
            # 调用其它任务, 形参只有1个, 实参1个以上, 后面跟随的是实际调用的任务参数
            firstParameter: Parameter = cls.parseListFromArgs([args[0]], parameterTypes)

            # 在当前任务文件所在的目录下, 以第1个参数的值作为任务文件路径名(不带后缀名), 查找对应的任务文件
            taskDir = os.path.dirname(taskFilePath)
            referTaskFilePath = os.path.join(taskDir, firstParameter.value + ".json")
            if not util.isFile(referTaskFilePath):
                raise Exception(
                    "illegal refer task value `{0}: refer task file `{1}` not found`".format(
                        firstParameter.value, referTaskFilePath
                    )
                )

            referTaskFilePath = os.path.abspath(referTaskFilePath)
            referTaskJsonData = json.loads(util.readContent(referTaskFilePath).strip())
            referTaskParameterTypes = ParameterType.parseListFromData(
                referTaskJsonData["args"]
            )
            referTaskParameterTypes_len = len(referTaskParameterTypes)
            if args_len - 1 != referTaskParameterTypes_len:
                raise Exception(
                    "illegal refer task args : length {0} not equal to declare argTypes length {1}".format(
                        args_len - 1, referTaskParameterTypes_len
                    )
                )

            referTask = {
                "jsonPath": referTaskFilePath,
                "jsonData": referTaskJsonData,
                "argTypes": referTaskParameterTypes,
            }
            firstParameter._parsedData["referTask"] = referTask
            leftParameters = cls.parseListFromArgs(args[1:], referTaskParameterTypes)

            parameters = [firstParameter]
            parameters.extend(leftParameters)

            return parameters

        else:
            # check_result = cls.check_isParameterMatch(args, parameterTypes)
            # if not check_result["isMatch"]:
            #     LOGGER.error("url `{0}`: args data not match parameterTypes", url)
            #     return None            

            return cls.parseListFromArgs(args, parameterTypes)

    def toDict(self) -> dict:
        tprint("into toDict ...", enable=False)
        tprint("self.value: ", self.value, enable=False)
        tprint(enable=False)

        dictData = {
            "type": self.type.toDict(),
            "value": Parameter.getValueJsonData(self.value),
            "express": self.express.toDict() if self.express else None,
            "_cacValue": self._cacValue,
        }
        if self._parsedData:
            dictData["_parsedData"] = self._parsedData
        return dictData

    def getMarkInfo(self) -> dict:
        tprint("into getMarkInfo ...", enable=False)
        tprint("self.getValue(): ", self.getValue(), enable=False)
        tprint(enable=False)

        dictData = {
            "type": self.type.type,
            "name": self.type.name,
            "value": Parameter.getValueJsonData(self.getValue()),
        }
        return dictData

    @classmethod
    def getValueJsonData(cls, value: object):
        if isinstance(value, dict) and (
            "action" in value.keys() or "elseAction" in value.keys()
        ):
            dictData = {}
            action = value.get("action")
            tprint("action type: ", type(action), enable=False)
            tprint("action: ", action, enable=False)

            elseAction = value.get("elseAction")
            if action:
                actionDatas = []
                for act in action:
                    actDatas = []
                    for _param in act:
                        param: Parameter = _param
                        actDatas.append(param.toDict())
                    actionDatas.append(actDatas)

                dictData["action"] = actionDatas

            if elseAction:
                elseActionDatas = []
                for act in elseAction:
                    actDatas = []
                    for _param in act:
                        param: Parameter = _param
                        actDatas.append(param.toDict())
                    elseActionDatas.append(actDatas)

                dictData["elseAction"] = elseActionDatas

            return dictData

        return value

    @classmethod
    def getParameter(cls, params: list, paramName: str):
        if paramName == "return":
            params_len = len(params)
            i = params_len - 1
            while i >= 0:
                param: Parameter = params[i]
                if param.type.name == paramName:
                    return param
                i -= 1

        else:
            for param_ in params:
                param: Parameter = param_
                if param.type.name == paramName:
                    return param

        return None

    @classmethod
    def check_isParameterMatch(
        cls, parameterDatas: list[dict], parameterTypes: list[ParameterType]
    ) -> bool:
        """
        检测参数数据和参数类型是否匹配

        检测过程:
            检测参数类型中的每一个必填参数, 在实际参数中找打与之匹配的参数

        返回:
            {
                isMatch: bool,
                // 经过排序后的参数数据(排序后和形参顺序一致)
                sortedParameterDatas: list[Parameter]
            }
        """
        sortedParameterDatas = []
        for parameterType in parameterTypes:
            if parameterType.required:
                for parameterData in parameterDatas:
                    if parameterData["name"] == parameterType.name:
                        sortedParameterDatas.append(parameterDatas)
                        break
                    else:
                        return {"isMatch": False}
        return {"isMatch": True, "sortedParameterDatas": sortedParameterDatas}


def run_function(task, url: str, args: list[Parameter]):
    arg: Parameter = None
    arg2: Parameter = None
    arg3: Parameter = None
    argsLen = len(args)
    if argsLen > 0:
        arg = args[0]
    if argsLen > 1:
        arg2 = args[1]
    if argsLen > 2:
        arg3 = args[2]

    # common
    if url == "/agerun/common/print":
        common.printLog(arg.getValue())
    elif url == "/agerun/common/wait":
        common.wait(arg.getValue())
    elif url == "/agerun/common/capture_screen_region":
        common.capture_screen_region(arg.getValue(), arg2.getValue() if arg2 else None)
    elif url == "/agerun/common/getFormatNowTime":
        common.getFormatNowTime(arg.getValue() if arg else None)

    # file
    elif url == "/agerun/file/saveJsonData":
        result = file.saveJsonData(arg.getValue(), arg2.getValue())
        returnParam = Parameter.getParameter(args, "return")
        if returnParam:
            task.setDic(returnParam.express.value, result)

    # ui/mouse
    elif url == "/agerun/ui/mouse":
        mouse.mouse_move(arg.getValue())
    elif url == "/agerun/ui/mouse_input":
        mouse.mouse_move_input(arg.getValue(), arg2.getValue())
    elif url == "/agerun/ui/mouse_input_enter":
        mouse.mouse_move_input_enter(arg.getValue(), arg2.getValue())
    elif url == "/agerun/ui/mouse_mousedown":
        mouse.mouse_mousedown(arg.getValue())
    elif url == "/agerun/ui/mouse_doubleclic":
        mouse.mouse_doubleclick(arg.getValue())
    elif url == "/agerun/ui/mouse_get_text":
        recognize_text = mouse.mouse_get_text(arg.getValue(), arg2.getValue())
        task.setDic(arg3.express.value, recognize_text)

    # ui/keyInput
    elif url == "/agerun/ui/keyInput/pressKey":
        keyInput.pressKey(arg.getValue())
    elif url == "/agerun/ui/keyInput/pressHotKey":
        keyInput.pressHotKey(arg.getValue())
    elif url == "/agerun/ui/keyInput/inputChineseChars":
        keyInput.inputChineseChars(arg.getValue(), arg2.getValue() if arg2 else None)
    elif url == "/agerun/ui/keyInput/inputChineseCharsWithLetters":
        keyInput.inputChineseCharsWithLetters(
            arg.getValue(), arg2.getValue() if arg2 else None
        )
    elif url == "/agerun/ui/keyInput/switchToChineseInput":
        if arg:
            result = keyInput.switchToChineseInput()
            task.setDic(arg.express.value, result)
        else:
            keyInput.switchToChineseInput()
    elif url == "/agerun/ui/keyInput/switchToEngInput":
        if arg:
            result = keyInput.switchToEngInput()
            task.setDic(arg.express.value, result)
        else:
            keyInput.switchToEngInput()

    # app/application
    elif url == "/agerun/app/application/quickStartApp":
        application.quickStartApp(arg.getValue())
    elif url == "/agerun/app/application/activateWindow":
        result = application.activateWindow(arg.getValue())
        if arg2:
            task.setDic(arg2.express.value, result)
    elif url == "/agerun/app/application/exitApp":
        result = application.exitApp(arg.getValue())
        if arg2:
            task.setDic(arg2.express.value, result)

    # app/qq
    elif url == "/agerun/app/qq/waittingForLoginAppear":
        result = (
            qq.waittingForLoginAppear(arg.getValue())
            if arg and arg.type.name == "waittingTimeLimit"
            else qq.waittingForLoginAppear()
        )
        returnParam = Parameter.getParameter(args, "return")
        if returnParam:
            task.setDic(returnParam.express.value, result)

    elif url == "/agerun/app/qq/select_qq_number_input":
        tprint("xx2 ready into select_qq_number_input ...")
        result = qq.select_qq_number_input(arg.getValue(), arg2.getValue())        
        tprint("xx2 arg3: ", arg3)
        returnParam = Parameter.getParameter(args, "return")
        if returnParam:
            tprint("xx2 returnParam.express.value: ", returnParam.express.value)
            tprint("xx2 result: ", result)
            task.setDic(returnParam.express.value, result)

    elif url == "/agerun/app/qq/check_qq_logined":
        result = qq.check_qq_logined(arg.getValue())
        returnParam = Parameter.getParameter(args, "return")
        if returnParam:
            task.setDic(returnParam.express.value, result)

    elif url == "/agerun/app/qq/waittingForContactHomeAppear":
        result = qq.waittingForContactHomeAppear(
            arg.getValue(), arg2.getValue() if arg2 else None
        )
        returnParam = Parameter.getParameter(args, "return")
        if returnParam:
            task.setDic(returnParam.express.value, result)

    elif url == "/agerun/app/qq/get_searchPrompt_centerPos":
        result = qq.get_searchPrompt_centerPos()
        returnParam = Parameter.getParameter(args, "return")
        if returnParam:
            task.setDic(returnParam.express.value, result)

    elif url == "/agerun/app/qq/get_searchIcon_centerPos":
        result = qq.get_searchIcon_centerPos()
        returnParam = Parameter.getParameter(args, "return")
        if returnParam:
            task.setDic(returnParam.express.value, result)

    elif url == "/agerun/app/qq/get_searchFirstViewInfo_centerPos":
        result = qq.get_searchFirstViewInfo_centerPos()
        returnParam = Parameter.getParameter(args, "return")
        if returnParam:
            task.setDic(returnParam.express.value, result)

    elif url == "/agerun/app/qq/foucus_search_text":
        result = qq.foucus_search_text()
        returnParam = Parameter.getParameter(args, "return")
        if returnParam:
            task.setDic(returnParam.express.value, result)

    elif url == "/agerun/app/qq/foucus_chat_window_sendMessage":
        result = qq.foucus_chat_window_sendMessage(arg.getValue())
        returnParam = Parameter.getParameter(args, "return")
        if returnParam:
            task.setDic(returnParam.express.value, result)

    elif url == "/agerun/app/qq/foucus_friendInfo_window_and_draw_left":
        result = qq.foucus_friendInfo_window_and_draw_left()
        returnParam = Parameter.getParameter(args, "return")
        if returnParam:
            task.setDic(returnParam.express.value, result)

    elif url == "/agerun/app/qq/recognize_friendInfo_window_data":
        result = qq.recognize_friendInfo_window_data()
        returnParam = Parameter.getParameter(args, "return")
        if returnParam:
            task.setDic(returnParam.express.value, result)

    else:
        LOGGER.error("not found function for url `{0}`", url)


class BlockFlow:
    """
    任务块流

    一个任务可理解为一个任务方法, 而一个任务块流则是该方法下的一个流程执行块,
    该块通常分为以下几种类型:
        * fn(x1,...,xN)
        * var_name = fn(x1,...,xN)
        * var_name = const_value
        * var_name = expression
        *   if condition:
                action
            else:
                action
        *   while condition:
                action
    以上类型, 除了 if 和 while 语句块外, 其他的都为单个语句, 等价于实际代码中的一行语句,
    带有 "=" 表示赋值语句, 而 if 和 while 语句块中的 action 为块体动作, 可以继续拆解为多个语句(块)
    """

    def __init__(
        self, task, id: str, url: str, args: list = [], actions1: list = [], actions2=[]
    ):
        """
        任务块流构造

        参数:
            task (Task): 任务块流所属的任务
            id (str): 任务块流id
            url (str): 任务块流调用的函数路径
            args (list<Parameter>): 任务块流执行的函数参数
            actions1 (list<BlockFlow>): 语句块(if, while等)列表
            actions2 (list<BlockFlow>): 语句块(else)列表
        """
        self.task: Task = task
        self.id = id
        self.url = url
        self.args = args
        self.actions1 = actions1
        self.actions2 = actions2

    def __calculateAllParameterValues(self):
        if isinstance(self.args, list) and len(self.args) > 0:
            for _arg in self.args:
                param: Parameter = _arg
                if param.express:
                    param.cacValue(self.task)

    def excute(self):
        # 设置
        show_args = False

        try:
            self.task.monitorCall(self)
            self.task.blocked(self)

            self.__calculateAllParameterValues()

            if self.url in [
                "/agerun/variable/text",
                "/agerun/variable/number",
                "/agerun/variable/bool",
                "/agerun/variable/dict",
                "/agerun/variable/array",
            ]:
                name_arg: Parameter = [
                    arg for arg in self.args if arg.type.name == "name"
                ][0]
                value_arg: Parameter = [
                    arg for arg in self.args if arg.type.name == "value"
                ][0]
                self.task.setDic(name_arg.value, value_arg.getValue())
                LOGGER.info(
                    "var `{0}` success assigned by value `{1}`, and set to dic",
                    name_arg.value,
                    value_arg.getValue(),
                )

            elif self.url == "/agerun/common/flow":
                firtArg: Parameter = self.args[0]
                referTask: dict = firtArg._parsedData["referTask"]
                referTaskFilePath = referTask["jsonPath"]
                referTaskJsonData = referTask["jsonData"]

                referTaskArgTypes = []
                taskArgs = []
                args_len = len(self.args)
                i = 1
                while i < args_len:
                    arg: Parameter = self.args[i]
                    referTaskArgTypes.append(arg.type)
                    taskArgs.append(arg.getValue())
                    i += 1

                Task(
                    referTaskFilePath,
                    *taskArgs,
                    **{
                        "taskJsonData": referTaskJsonData,
                        "taskArgTypes": referTaskArgTypes,
                    }
                ).run()

            elif self.url == "/agerun/common/interrupt":
                self.task.interrupt()

            else:
                if show_args:
                    LOGGER.info("before run_function self.args: ")
                    args_list = [arg.toDict() for arg in self.args]
                    args_list_str = json.dumps(args_list, ensure_ascii=False, indent=4)
                    LOGGER.info(args_list_str, raw=True)

                run_function(self.task, self.url, self.args)

            self.task.monitorReturn(self)

        except Exception as e:
            LOGGER.error("excute err", errorType=e)
            self.task.log(str(e))
            traceback.print_exc()

    def toDict(self, include_type=True) -> dict:
        dictData = {
            "task": {
                "id": self.task.id,
                "text": self.task.text,
                "author": self.task.author,
            },
            "id": self.id,
            "url": self.url,
            # "args": [arg.toDict() for arg in self.args],
            "args": [arg.getMarkInfo() for arg in self.args] if self.args else [],
        }
        if self.actions1:
            dictData["actions1"] = [act.toDict() for act in self.actions1]
        if self.actions2:
            dictData["actions2"] = [act.toDict() for act in self.actions2]

        tprint("dictData args: ", dictData["args"], enable=False)
        tprint("dictData actions1: ", dictData.get("actions1"), enable=False)
        tprint("dictData actions2: ", dictData.get("actions2"), enable=False)

        if include_type:
            typeName = type(self).__name__
            dictData["type"] = typeName

        return dictData

    def toString(self, *exclude_attrs) -> str:
        dictData = self.toDict()
        dictData_keys = dictData.keys()
        for exclude_attr in exclude_attrs:
            if exclude_attr in dictData_keys:
                del dictData[exclude_attr]
        return json.dumps(dictData, ensure_ascii=False, indent=4)
        # return str(self.toDict(*exclude_attrs))


class BlockWhile(BlockFlow):
    def excute(self):
        try:
            self.task.monitorCall(self)
            self.task.blocked(self)

            tprint("BlockWhile self.args: ", self.args)
            if self.args:
                args_dict = [arg.toDict() for arg in self.args]
                tprint("args_dict: ", args_dict)

            while True:
                firstParameter: Parameter = self.args[0]
                firstParameter.cacValue(self.task)
                if firstParameter.getValue():
                    for act in self.actions1:
                        act.excute()
                else:
                    break

            self.task.monitorReturn(self)

        except Exception as e:
            LOGGER.error("excute err")
            self.task.log(str(e))
            traceback.print_exc()


class BlockIf(BlockFlow):
    def excute(self):
        try:
            self.task.monitorCall(self)
            self.task.blocked(self)

            firstParameter: Parameter = self.args[0]
            firstParameter.cacValue(self.task)
            if firstParameter.getValue():
                for act in self.actions1:
                    act.excute()
            else:
                if self.actions2:
                    for act in self.actions2:
                        act.excute()

            self.task.monitorReturn(self)

        except Exception as e:
            LOGGER.error("excute err")
            self.task.log(str(e))
            traceback.print_exc()


class Task:
    def __init__(self, taskFilePath: str, *taskArgs, **options):
        """
        参数:
            taskFilePath (str): 任务文件路径

        动态元组参数:
            taskArgs (object): 任务入参

        动态字典参数:
            options {
                taskJsonData (dict): 任务文件JSON数据
                taskArgTypes (list): 任务文件入参类型
            }

        """
        if not util.isFile(taskFilePath):
            raise Exception(
                "illegal taskFilePath `{0}`: not existed".format(taskFilePath)
            )
        self.taskFilePath = os.path.abspath(taskFilePath)

        self.id: str = None
        self.text: str = None
        self.author: str = None

        # 记录指向任务过程中运算的变量名和值
        self.__dic = {}
        # 记录指向任务过程中从外部传过来的覆盖已计算的变量名和值,
        # 有可能是外部调试设置的值, 撤销调试后, 仍然显示原有已计算的, 所以要和 `__dic` 区分开
        self.__varDic = {}

        # 任务方法入参(从外部传入的最终计算的值(非表达式))
        self.args = []
        # 任务方法执行语句块
        self.blocks = []

        # 打断点阻塞的块id
        self.blockIds = []

        # 任务中断
        self._interrupted = None

        self.__load(taskFilePath, taskArgs, options)

    def parseBlockFlows(self, tasks: list) -> list:
        blockFlows = []

        for task in tasks:
            url = task["url"]
            args = Parameter.parseListFromData(self.taskFilePath, task)
            blockFlow = None
            if url == "/agerun/common/while":
                actionTasks = task["blocks"]["action"]
                actionBlocks = self.parseBlockFlows(actionTasks)
                blockFlow = BlockWhile(
                    self, task["id"], url, args, actions1=actionBlocks
                )

            elif url == "/agerun/common/if":
                actionTasks = task["blocks"]["action"]
                actionBlocks = self.parseBlockFlows(actionTasks)
                elseActionTasks = task["blocks"].get("elseAction")
                elseActionBlocks = (
                    self.parseBlockFlows(elseActionTasks) if elseActionTasks else None
                )
                blockFlow = BlockIf(
                    self,
                    task["id"],
                    url,
                    args,
                    actions1=actionBlocks,
                    actions2=elseActionBlocks,
                )

            else:
                blockFlow = BlockFlow(self, task["id"], url, args)
            blockFlows.append(blockFlow)
        return blockFlows

    def __load(self, taskFilePath: str, taskArgs: tuple, options: dict):
        """
        加载JSON任务文件
        """
        taskJsonData = options.get("taskJsonData")
        taskArgTypes = options.get("taskArgTypes")
        jsonData = None
        try:
            jsonData: dict = None
            if isinstance(taskJsonData, dict):
                jsonData = taskJsonData
            else:
                jsonString = util.readContent(taskFilePath).strip()
                jsonData = json.loads(jsonString)

            self.id = jsonData.get("id")
            self.text = jsonData.get("text")
            self.author = jsonData.get("author")
            if taskArgTypes is None:
                taskArgTypes = ParameterType.parseListFromData(jsonData["args"])
            taskArgTypes_len = len(taskArgTypes)
            if len(taskArgs) != taskArgTypes_len:
                errMsg = "taskArgs `{0}` not match with taskArgTypes `{1}`".format(
                    taskArgs, taskArgTypes
                )
                LOGGER.error(errMsg)
                raise Exception(errMsg)

            i = 0
            while i < taskArgTypes_len:
                arg = Parameter(taskArgTypes[i], value=taskArgs[i])
                self.args.append(arg)
                i += 1

            self.blocks = self.parseBlockFlows(jsonData["tasks"])

        except Exception as e:
            errMsg = str(e)
            self.log(errMsg)
            traceback.print_exc()
            raise Exception("load err: " + errMsg)

    def getArg(self, argName: str):
        """
        根据任务方法入参名称, 获取其对应的入参值
        """
        for _arg in self.args:
            arg: Parameter = _arg
            if arg.type.name == argName:
                return arg.value
        return None

    def getDic(self, key: str):
        """
        根据键(变量名)从已存储到字典中的变量名, 获取其对应的变量值
        """
        if key in self.__varDic.keys():
            return self.__varDic[key]
        else:
            return self.__dic[key]

    def setDic(self, key: str, value: object):
        if key in self.__varDic.keys():
            self.__varDic[key] = value
        else:
            self.__dic[key] = value

    def run(self):
        """
        运行任务
        """
        LOGGER.info("task[{0}] run start ...\n", self.getMarkInfo())

        for _block in self.blocks:
            if self._interrupted:
                LOGGER.info("任务中断了")
                break
            block: BlockFlow = _block
            block.excute()
            LOGGER.info("\n", raw=True)

        LOGGER.info("dic: ")
        tprint("__dic: ", self.__dic)

        LOGGER.info(
            json.dumps(self.__dic, ensure_ascii=False, indent=4) + "\n", raw=True
        )
        LOGGER.info("task[{0}] run end\n", self.getMarkInfo("args"))

    def monitorCall(self, blockFlow: BlockFlow):
        LOGGER.info("BlockFlow[{0}] before excute\n", blockFlow.toString())

    def monitorReturn(self, blockFlow: BlockFlow):
        LOGGER.info(
            "BlockFlow[{0}] after excute\n",
            blockFlow.toString("task", "args", "actions1", "actions2"),
        )

    def log(self, error: str):
        LOGGER.error(
            error,
            logConsoleFormatter=Err_Log_Formatter,
            logFileFormatter=Err_Log_Formatter,
        )

    def blocked(self, blockFlow: BlockFlow):
        while True:
            if blockFlow.id in self.blockIds:
                continue
            else:
                break

    def interrupt(self):
        self._interrupted = True

    def toDict(self, *exclude_attrs) -> dict:
        dictData = {
            "taskFilePath": self.taskFilePath,
            "id": self.id,
            "text": self.text,
            "author": self.author,
            # "args": [arg.toDict() for arg in self.args],
            "args": [arg.getMarkInfo() for arg in self.args],
            "blocks": [block.toDict() for block in self.blocks],
            "blockIds": str(self.blockIds),
        }

        for delKey in exclude_attrs:
            del dictData[delKey]

        return dictData

    def toString(self, *exclude_attrs) -> str:
        return json.dumps(self.toDict(*exclude_attrs), ensure_ascii=False)

    def getMarkInfo(self, *exclude_attrs):
        dictData = {
            "taskFilePath": self.taskFilePath,
            "id": self.id,
            "text": self.text,
            "author": self.author,
            "args": [arg.getMarkInfo() for arg in self.args],
        }
        for exclude_attr in exclude_attrs:
            del dictData[exclude_attr]
        return json.dumps(dictData, ensure_ascii=False, indent=4)


def expressCac(task: Task, express: Express) -> object:
    """
    计算表达式所代表的最终值
    """
    name = express.name
    if express.hasArgs():
        tprint("into expressCac hasArgs 1111", enable=True)

        arg: dict = express.args[0]
        arg_value: object = arg.get("value")
        arg_express: Express = arg.get("express")

        tprint(
            "arg_value: [{0}], arg_express: [{1}]".format(
                arg_value, arg_express.toDict() if arg_express else None
            ),
            enable=True,
        )

        arg_cacValue = None
        if arg_express is None:
            arg_cacValue = arg_value
        else:
            arg_cacValue = expressCac(task, arg_express)
        tprint("arg_cacValue: ", arg_cacValue, enable=False)

        # 有限参数运算
        if name == "getKeyValue":
            tprint("into name getKeyValue ...")
            tprint("first_arg_value type: ", type(arg_cacValue))
            tprint("first_arg_value: ", arg_cacValue)
            first_arg_value = arg_cacValue
            
            arg_2: dict = express.args[1]
            arg_2_value: object = arg_2.get("value")
            arg_2_express: Express = arg_2.get("express")

            arg_2_cacValue = None
            if arg_2_express is None:
                arg_2_cacValue = arg_2_value
            else:
                arg_2_cacValue = expressCac(task, arg_2_express)
            tprint("arg_2_cacValue: ", arg_2_cacValue, enable=False)
            
            second_arg_value = arg_2_cacValue
            return first_arg_value[second_arg_value]

        # 多个参数累计运算
        value = arg_cacValue
        args_len = len(express.args)
        i = 1
        while i < args_len:
            arg: dict = express.args[i]
            arg_value: object = arg.get("value")
            arg_express: Express = arg.get("express")

            tprint(
                "while every loop arg_value: [{0}], arg_express: [{1}]".format(
                    arg_value, arg_express.toDict() if arg_express else None
                ),
                enable=False,
            )

            tprint("xx1 arg_cacValue before ...")
            arg_cacValue = None
            if arg_express is None:
                arg_cacValue = arg_value
            else:
                arg_cacValue = expressCac(task, arg_express)
                tprint("while every loop arg_cacValue: ", arg_cacValue, enable=False)

            tprint("xx1 arg_cacValue: ", arg_cacValue)

            if name == "+":
                tprint("into + ...")
                value += arg_cacValue
            elif name == "-":
                value -= arg_cacValue
            elif name == "*":
                tprint("start multiply")
                tprint("value: ", value)
                tprint("arg_cacValue: ", arg_cacValue)
                tprint()
                value = value * arg_cacValue
            elif name == "/":
                value /= arg_cacValue
            elif name == "//":
                value //= arg_cacValue
            elif name == "%":
                value %= arg_cacValue

            elif name == "&&":
                value = value and arg_cacValue
            elif name == "||":
                value = value or arg_cacValue

            elif name == "<":
                value = value < arg_cacValue
            elif name == "<=":
                value = value <= arg_cacValue
            elif name == "==":
                value = value == arg_cacValue
            elif name == ">":
                value = value > arg_cacValue
            elif name == ">=":
                value = value >= arg_cacValue

            else:
                raise Exception(
                    "unsupported args express operator name: {0}".format(name)
                )

            i += 1

        return value

    else:
        nested_express: Express = express.express
        if name == "arg":
            return task.getArg(express.value)
        elif name == "const":
            return express.value
        elif name == "var" or name == "variable":
            return task.getDic(express.value)

        elif re.match(r"^(text|number|list|array|object)\.length$", name):
            value = None
            if nested_express:
                value = expressCac(task, nested_express)
            else:
                value = express.value
            return len(value)

        elif name == "toString":
            value = None
            if nested_express:
                value = expressCac(task, nested_express)
            else:
                value = express.value
            tprint("xx3 value: ", value)
            return str(value)

        elif name == "!":
            value = None
            if nested_express:
                value = expressCac(task, nested_express)
            else:
                value = express.value
            return not value

        else:
            raise Exception(
                "unsupported no args express operator name `{0}`".format(name)
            )
