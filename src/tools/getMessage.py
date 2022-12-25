import json

from src.message import Message
from src.tools.tool import timeSecToTime, error


def getMessage(line: str):
    try:
        messageProperty = convertProperty(line)
        timeJson = messageProperty.get("clip").replace("_", "")
        if timeJson[-1] != "}":
            timeJson += "}"
        timeObject = json.loads(timeJson)
        startTime = timeSecToTime(timeObject["startTime"])
        endTime = timeSecToTime(timeObject["startTime"] + timeObject["duration"])
        return Message(messageProperty.get("text"), messageProperty.get("name"), messageProperty.get("clip"),
                       messageProperty.get("type"), startTime, endTime)
    except Exception as e:
        error("getMessage:" + e.__str__() + "\nErrorText=" + line)


def convertProperty(line: str):
    try:
        messageSetting = {}
        removeBrackets = line[1:line.__len__() - 2].replace("\\", "").replace("{user}", "マネージャー")
        if removeBrackets.__contains__("narration"):
            messageSetting["type"] = "narration"
            formatText = splitLine(removeBrackets[10:])
            for line in formatText:
                strs = line.split('=')
                strs[1] = line[len(strs[0]) + 1:]
                messageSetting[strs[0]] = strs[1]
        if removeBrackets.__contains__("message"):
            messageSetting["type"] = "message"
            formatText = splitLine(removeBrackets[8:])
            for line in formatText:
                strs = line.split('=')
                strs[1] = line[len(strs[0]) + 1:]
                messageSetting[strs[0]] = strs[1]
        return messageSetting
    except Exception as e:
        error("convertProperty:" + e.__str__() + "\nErrorText=" + line)


# .replace('\u0020', '\n').split("\n")
def splitLine(text: str):
    try:
        canReturn = True
        afterSplit = text.replace('\u0020', '\n').split("\n")
        for element in afterSplit:
            if element.__contains__("="):
                continue
            else:
                canReturn = False
                break
        if canReturn:
            return afterSplit
        else:
            tempTextProperty = ""
            waitForDelete = []
            for element in afterSplit:
                if element.__contains__("text="):
                    tempTextProperty += element
                    waitForDelete.append(element)
                    continue
                if element.__contains__("="):
                    continue
                else:
                    tempTextProperty += element
                    waitForDelete.append(element)
            for element in waitForDelete:
                afterSplit.remove(element)
            afterSplit.insert(0, tempTextProperty)
            return afterSplit
    except Exception as e:
        error("splitLine:" + e.__str__() + "\nErrorText=" + text)
