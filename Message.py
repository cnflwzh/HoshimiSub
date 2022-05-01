class Message:
    """单条Message的基类"""

    def __init__(self, text, name, timejson, number, startTimeSting, endTimeSting):
        self.text = text
        self.name = name
        self.timejson = timejson
        self.number = number
        self.startTimeSting = startTimeSting
        self.endTimeSting = endTimeSting
