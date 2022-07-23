class Message:
    """单条Message的基类"""

    def __init__(self, text, name, timejson, messageType, startTimeSting, endTimeSting):
        self.text = text
        self.name = name
        self.timejson = timejson
        self.messageType = messageType
        self.startTimeSting = startTimeSting
        self.endTimeSting = endTimeSting
