import argparse

from src import subtitleGenerate
from src.tools.configEnum import FolderOrFile, SubType
from src.tools.tool import initOutputPath


def main():
    parse = argparse.ArgumentParser(description="IDOLY PRIDE Subtitle Generator")
    parse.add_argument("-p", "--path", type=str, default="",
                       help="Enter the path to the source file or the source directory")
    parse.add_argument("-o", "--output", type=str, default="./output/  ",
                       help="Fill in the output path, do not fill in the default setting for the program root directory \"output\" folder (the program will automatically generate")
    parse.add_argument("-t", "--type", type=str, choices=["srt", "ass"], default="srt",
                       help="Select the type of file to be converted, ASS file or SRT file")
    parse.add_argument("-m", "--mode", type=str, choices=["file", "folder"], default="file",
                       help="Select the generation mode, single file mode or folder mode")
    parse.add_argument("--name", action="store_true",
                       help="Select whether to include character names or not, if this parameter is added, character names will be added in front of the line when converting to SRT subtitles and ASS subtitles will generate a separate line of subtitles")
    parse.add_argument("--style", action="store_true",
                       help="When converting ASS files, add this parameter to allow each character to have its own subtitle style")

    args = parse.parse_args()
    mode = FolderOrFile(args.mode)
    subType = SubType(args.type)
    includeName = args.name
    outputPath = initOutputPath(args.output.strip())
    personalStyle = args.style
    subtitleGenerate.generateSubtitle(mode, args.path, subType, includeName, outputPath, personalStyle)


if __name__ == "__main__":
    main()
