import math
import os

from rich.console import Console

console = Console()


def info(msg: str):
    console.print(f"[bold blue]>>> [Info][/bold blue] {msg}")


def succeed(msg: str):
    console.print(f"[bold green]>>> [Succeed][/bold green] {msg}")


def error(msg: str):
    console.print(f"[bold red]>>> [Error][/bold red] {msg}")


def warning(msg: str):
    console.print(f"[bold yellow]>>> [Warning][/bold yellow] {msg}")


def timeSecToTime(time: float):
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    mill, sec = math.modf(time)
    timeString = "%d:%02d:%02d," % (h, m, s) + str("%.3f" % mill)[2:]
    return timeString


def initOutputPath(outputPath: str):
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
        info(f"Directory {outputPath} has been created")
    else:
        info(f"Directory {outputPath} already exists")
    if outputPath[-1] != "/":
        outputPath += "/"
    return outputPath
