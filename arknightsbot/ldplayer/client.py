import subprocess
from time import sleep

# Commands to prepare LDplayer for bot

closeLD = [
    "C:\\LDPlayer\\LDPlayer9\\dnconsole.exe",
    "quitall"
]
configureLD = [
    "C:\\LDPlayer\\LDPlayer9\\dnconsole.exe",
    "modify",
    "--index",
    "1",
    "--resolution",
    "1280,720,240",
    "--cpu",
    "4",
    "--memory",
    "4096"
]
launchLD = [
    "C:\\LDPlayer\\LDPlayer9\\dnconsole.exe",
    "launch",
    "--index",
    "1"
]
launchAK = [
    "C:\\LDPlayer\\LDPlayer9\\dnconsole.exe",
    "runapp",
    "--index",
    "1",
    "--packagename",
    "com.YoStarEN.Arknights"
]

# Commands for image recognition

# Takes a screenshot of emulator window and saves it into the shared folder
# Using this method so bot can run in background behind other windows despite many writes to disk
take_screenshot = [
    "C:\\LDPlayer\\LDPlayer9\\dnconsole.exe",
    "adb",
    "--index",
    "1",
    "--command",
    "shell screencap -p /mnt/shared/Pictures/ss.png"
]


def run_command(args: list[str], timeout=0) -> str:
    """Run a command and return the output"""
    with subprocess.Popen(args, shell=False) as process:
        try:
            outs, errs = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            outs, errs = process.communicate()
            print("Command timed out")
    if errs:
        return errs.decode("utf-8")
    elif outs:
        return outs.decode("utf-8")
    else:
        return ""


def start_ld():
    commands = [
        closeLD,
        configureLD,
        launchLD,
        launchAK
    ]
    # App will not launch if LDplayer is not fully initialized
    for index, command in enumerate(commands):
        if index >= 3:
            sleep(10)
        run_command(command, timeout=5)


def restart_ld():
    start_ld()


def capture_screen():
    run_command(take_screenshot, timeout=5)


def click_on_location(point: tuple):
    x, y = point
    click = [
        "C:\\LDPlayer\\LDPlayer9\\dnconsole.exe",
        "adb",
        "--index",
        "1",
        "--command",
        "shell input tap " + str(x) + " " + str(y)
    ]
    run_command(click, timeout=5)
