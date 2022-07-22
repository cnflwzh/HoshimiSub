import subGenerate
from programConfig import *

# TODO 缺少灰色样式文本的解析

# Configuration
# 该选项为选择处理模式，文件夹或单文件 File Folder
mode = FolderOrFile.File
# 该选项为指定文件或文件夹路径
filePath = "./sourcetxt/adv_card_rui_04_01.txt"
# 该选项指定字幕类型  ASS SRT 目前版本只支持SRT格式
subType = SubType.ASS
# 该选项用于指定ASS字幕时的样式，是不同人不同样式还是所有人一个样式 OneStyle or DifferentStyle
styleMode = StyleMode.OneStyle

subGenerate.generateSub(mode, filePath, subType, styleMode)
