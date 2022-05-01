import math


def timeSecToTime(time: float):
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    mill, sec = math.modf(time)
    timeString = "%d:%02d:%02d," % (h, m, s) + str("%.3f" % mill)[2:]
    print(timeString)
    return timeString
