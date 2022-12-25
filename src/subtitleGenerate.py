import sys

from jinja2 import FileSystemLoader, Environment

from src.tools.configEnum import FolderOrFile, SubType
from src.tools.formatFactory import characterNameReplace, subStyleReplace
from src.tools.getMessage import getMessage
from src.tools.tool import *

characterTag = "IP_NAME"
dialogTag = "IP_MESSAGE"
cueCaption = "IP_CUE"


def generateSubtitle(mode: FolderOrFile, filePath: str, subType: SubType, includeName: bool, outputPath: str,
                     personalStyle: bool):
    character_text = open("src/template/Character.txt", "r", encoding="UTF-8").read()
    lines = character_text.split("\n")
    # 创建一个用于存储替换信息的字典
    replace_dict = {}
    for line in lines:
        parts = line.split("=")
        # 如果行有三个部分，则第一个部分是原文，第二个部分是汉化文本
        if len(parts) == 3:
            original_text = parts[0]
            translated_text = parts[1]
            subtitle_style = parts[2]
            # 将原文、汉化文本和字幕样式存储在字典中，以原文角色名为键
            replace_dict[original_text] = (translated_text, subtitle_style)
        else:
            raise Exception(
                "Character.txt is not formatted correctly at:" + line + "make sure your Character.txt such as: \n 'original_text=translated_text=subtitle_style'")
    try:
        if filePath == "":
            error("filePath is None")
            sys.exit(0)
        # 判断为单文件模式或文件夹模式
        match mode:
            case FolderOrFile.File:
                # 判断输出文件类型
                match subType:
                    case SubType.SRT:
                        info("======Single file conversion to SRT task is starting======")
                        srtGenerate(filePath, includeName, outputPath, replace_dict)
                    case SubType.ASS:
                        info("======Single file conversion to ASS task is starting======")
                        assGenerate(filePath, includeName, outputPath, replace_dict, personalStyle)
            case FolderOrFile.Folder:
                match subType:
                    case SubType.SRT:
                        info("======Batch conversion to SRT task is starting======")
                        batchSRT(filePath, includeName, outputPath, replace_dict)
                    case SubType.ASS:
                        info("======Batch conversion to ASS task is starting======")
                        batchASS(filePath, includeName, outputPath, replace_dict, personalStyle)

    except Exception as e:
        print(e)
        error("generateSubtitle error: %s" % e)


def getSingleFileInfo(filePath):
    """
    获取单个文件中的所有信息
    :param filePath: 文件路径
    :return:
    """
    # 读取文件并获取文件内容
    originalFile = open(filePath, encoding="UTF-8")
    messageList = []
    for lines in originalFile.readlines():
        if lines[0:10].__contains__("message") or lines[0:12].__contains__("narration"):
            messageList.append(getMessage(lines))
    originalFile.close()
    return messageList


def batchSRT(filePath, includeName, outputPath, dict_character):
    """
    生成批量SRT文件
    :param dict_character:
    :param outputPath: 输出路径
    :param filePath: 文件夹路径
    :param includeName: 是否包含名字
    :return:
    """
    fileList = os.listdir(filePath)
    for file in fileList:
        srtGenerate(filePath + "/" + file, includeName, outputPath, dict_character)
    succeed("All files have been converted to SRT")


def srtGenerate(filePath, includeName, outputPath, dict_character):
    """
    生成单个SRT文件
    :param dict_character:
    :param outputPath: 输出文件路径
    :param filePath: 文件路径
    :param includeName: 是否包含名字
    :return:
    """
    try:
        messageList = getSingleFileInfo(filePath)
        fileName = filePath.replace("\\", "/").split("/")[-1].split(".")[-2].__str__()
        info("Now Processing: %s" % fileName)
        srtFile = open(outputPath + "%s.srt" % fileName, mode='w', encoding="UTF-8")
        i = 0
        if includeName:
            for message in messageList:
                if message.text is not None:
                    i += 1
                    srtFile.write(i.__str__() + "\n")
                    srtFile.write(message.startTimeSting + " --> " + message.endTimeSting + "\n")
                    if message.name is not None:
                        srtFile.write(characterNameReplace(message.name, dict_character) + "：" + message.text + "\n\n")
                    else:
                        srtFile.write(message.text + "\n\n")
        else:
            for message in messageList:
                if message.text is not None:
                    i += 1
                    srtFile.write(i.__str__() + "\n")
                    srtFile.write(message.startTimeSting + " --> " + message.endTimeSting + "\n")
                    srtFile.write(message.text + "\n\n")
        srtFile.close()
        succeed("%s has been converted to SRT" % fileName)
    except Exception as e:
        error("srtGenerate: %s" % e + "\nError file: %s" % filePath)


def batchASS(filePath, includeName, outputPath, dict_character, personalStyle):
    """
    生成批量ASS文件
    :param dict_character:
    :param outputPath: 文件输出路径
    :param filePath: 文件夹路径
    :param includeName: 是否包含名字
    :return:
    """
    fileList = os.listdir(filePath)
    for file in fileList:
        assGenerate(filePath + "/" + file, includeName, outputPath, dict_character, personalStyle)
    succeed("All files have been converted to ASS")


def assGenerate(filePath, includeName, outputPath, dict_character, personalStyle):
    """
    生成单个ASS文件
    :param personalStyle:
    :param dict_character:
    :param outputPath: 文件输出路径
    :param filePath: 文件路径
    :param includeName: 是否包含名字
    :return:
    """
    fileName = filePath.replace("\\", "/").split("/")[-1].split(".")[-2].__str__()
    info("Now Processing: %s" % fileName)
    preProcessedMessages = getSingleFileInfo(filePath)
    assFile = open(outputPath + "%s.ass" % fileName, mode='w', encoding="UTF-8")
    messageList = []
    if includeName:
        for message in preProcessedMessages:
            if message.text is None:
                continue
            if message.messageType == "message":
                nameLine = {"text": characterNameReplace(message.name, dict_character),
                            "startTimeSting": message.startTimeSting,
                            "endTimeSting": message.endTimeSting, "messageType": characterTag}
                messageList.append(nameLine)
                if personalStyle:
                    message.messageType = subStyleReplace(message.name, dict_character)
                else:
                    message.messageType = dialogTag
            if message.messageType == "narration":
                message.messageType = cueCaption
            if message.text.__contains__("（") and message.text.__contains__("）"):
                message.text = message.text.replace("（", "").replace("）", "")
                message.messageType = cueCaption
            messageList.append(message)

    else:
        for message in preProcessedMessages:
            if message.messageType == "message":
                if personalStyle:
                    message.messageType = subStyleReplace(message.name, dict_character)
                else:
                    message.messageType = dialogTag
            if message.messageType == "narration":
                message.messageType = cueCaption
            messageList.append(message)
    env = Environment(loader=FileSystemLoader("src/template"))
    template = env.get_template("asstemp.ass")
    assFile.write(template.render(messageList=messageList))
    succeed("%s has been converted to ASS" % fileName)
