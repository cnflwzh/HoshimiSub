from enum import Enum


class FolderOrFile(Enum):
    """
    Select Mode Only One File Or A Folder
    """
    File = "file"
    Folder = "folder"


class SubType(Enum):
    """
    Select which kind of subtitle you want to generate
    """
    SRT = "srt"
    ASS = "ass"
