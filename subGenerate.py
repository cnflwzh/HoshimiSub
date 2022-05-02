import json
import os
from os.path import join

from message import Message
from programConfig import FolderOrFile, SubType
from tool import *


def generateSub(mode: int, filePath: str, subType: int):
    if mode == FolderOrFile.File:
        info("Single File Mode")
        if subType == SubType.SRT:
            basicSrt(filePath)
        if subType == SubType.ASS:
            error("Single File ASS IS Not Complete Yet")
    if mode == FolderOrFile.Folder:
        if subType == SubType.SRT:
            multFile(filePath, subType)
        if subType == SubType.ASS:
            error("Folder ASS IS Not Complete Yet")


def basicSrt(filePath: str):
    originalFile = open(filePath, encoding="UTF-8")
    fileName = originalFile.name.split("/")[-1].split(".")[-2].__str__()
    # 输出路径
    srtFile = open("./output/%s.srt" % fileName, mode='w', encoding="UTF-8")
    info("Output path:""./output/%s.srt" % fileName)
    messageList = []
    fileLines = originalFile.readlines()
    for line in fileLines:
        if line.__contains__("message"):
            # 数据切割
            afterSplit = line[9:line.__len__() - 2].replace("\\", "").replace("{user}", "マネージャー").split(" ")
            # 处理当text中包含多个空格的情况
            if afterSplit.__len__() > 4:
                warning("Message Text include space")
                loopTimes = afterSplit.__len__() - 3
                tempText = ""
                for i in range(0, loopTimes, 1):
                    tempText += afterSplit[i] + " "
                tempText = tempText.strip()
                del afterSplit[0:afterSplit.__len__() - 3]
                afterSplit.insert(0, tempText)
            # 格式化数据
            text = afterSplit[0][5:]
            name = afterSplit[1][5:]
            if afterSplit.__len__() == 4:
                timeJson = afterSplit[3][5:].replace("_", "")
            else:
                timeJson = afterSplit[2][5:].replace("_", "")
            timeObject = json.loads(timeJson)
            # 计算时间轴的时间
            startTime = timeObject["startTime"]
            takeTime = timeObject["duration"]
            endTime = startTime + takeTime
            startTimeString = timeSecToTime(startTime)
            endTimeString = timeSecToTime(endTime)
            # warning("num=" + messageList.__len__().__str__() + "text=" + text + "  json=" + timeJson)
            messageList.append(
                Message(text, name, timeJson, messageList.__len__() + 1, startTimeString, endTimeString))

    for message in messageList:
        srtFile.write(str(message.number) + "\n")
        srtFile.write(message.startTimeSting + " --> " + message.endTimeSting + "\n")
        srtFile.write(message.text + "\n\n")
    originalFile.close()
    succeed("Single Finished Successfully")


def multFile(filePath: str, subType: int):
    fileList = os.listdir(filePath)
    for singleFile in fileList:
        basicSrt(join(filePath + singleFile))
    succeed("Multi Finished Successfully")
