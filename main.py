import argparse

from src import subtitleGenerate
from src.tools.configEnum import FolderOrFile, SubType
from src.tools.tool import initOutputPath


def main():
    parse = argparse.ArgumentParser(description="IDOLY PRIDE Subtitle Generator")
    parse.add_argument("-m", "--mode", type=str, choices=["file", "folder"], default="file",
                       help="Select Mode Only One File Or A Folder")
    parse.add_argument("-p", "--path", type=str, default="", help="Enter the path to the file or directory")
    parse.add_argument("-t", "--type", type=str, choices=["srt", "ass"], default="srt",
                       help="Enter the type of subtitle")
    parse.add_argument("-n", "--name", action="store_true",
                       help="If you add this argument, the role name will be included in the output, note that when "
                            "in SRT mode it is added before each line of text by default, ASS mode will be a separate "
                            "line, remember edit your ass template file")
    parse.add_argument("-o", "--output", type=str, default="./output/  ", help="Enter the path to the output file")

    args = parse.parse_args()
    mode = FolderOrFile(args.mode)
    subType = SubType(args.type)
    includeName = args.name
    outputPath = initOutputPath(args.output.strip())
    subtitleGenerate.generateSubtitle(mode, args.path, subType, includeName, outputPath)


if __name__ == "__main__":
    main()
