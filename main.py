import subGenerate
from programConfig import FolderOrFile, SubType

# Configuration
# 该选项为选择处理模式，文件夹或单文件 File Folder
mode = FolderOrFile.Folder
# 该选项为指定文件或文件夹路径
filePath = "./sourcetxt/"
# 该选项指定字幕类型  ASS SRT 目前版本只支持SRT格式
subType = SubType.SRT

subGenerate.generateSub(mode, filePath, subType)
