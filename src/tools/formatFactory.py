def characterNameReplace(waitForReplace: str, replace_dict: dict):
    if replace_dict.get(waitForReplace) is None:
        return waitForReplace
    return replace_dict.get(waitForReplace)[0]


def subStyleReplace(waitForReplace: str, replace_dict: dict):
    if replace_dict.get(waitForReplace) is None:
        return "IP_MESSAGE"
    return replace_dict.get(waitForReplace)[1]
