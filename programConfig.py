from enum import Enum


class FolderOrFile(Enum):
    """
    Select Mode Only One File Or A Folder
    """
    File = 0
    Folder = 1


class SubType(Enum):
    SRT = 0
    ASS = 1


class StyleMode(Enum):
    OneStyle = 0
    DifferentStyle = 1
