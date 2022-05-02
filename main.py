import json

from Message import Message
from tool import timeSecToTime

originalFile = open("./sourcetxt/adv_event_2205_01_04.txt", encoding="UTF-8")
fileName = originalFile.name.split("/")[-1].split(".")[-2].__str__()
srtFile = open("./output/%s.srt" % fileName, mode='w', encoding="UTF-8")
messageList = []
fileLines = originalFile.readlines()
for line in fileLines:
    if line.__contains__("message"):
        # 数据切割
        afterSplit = line[9:line.__len__() - 2].replace("\\", "").replace("{user}", "牧野").split(" ")
        # 格式化数据
        text = afterSplit[0][5:]
        name = afterSplit[1][5:]
        timeJson = afterSplit[3][5:].replace("_", "")
        timeObject = json.loads(timeJson)
        # 计算时间轴的时间
        startTime = timeObject["startTime"]
        takeTime = timeObject["duration"]
        endTime = startTime + takeTime
        startTimeString = timeSecToTime(startTime)
        endTimeString = timeSecToTime(endTime)
        messageList.append(Message(text, name, timeJson, messageList.__len__() + 1, startTimeString, endTimeString))

for message in messageList:
    srtFile.write(str(message.number) + "\n")
    srtFile.write(message.startTimeSting + " --> " + message.endTimeSting + "\n")
    srtFile.write(message.text + "\n\n")
originalFile.close()
