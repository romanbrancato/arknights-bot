import subprocess
from time import sleep
from arknightsbot.utils.logger import logger

# Commands to prepare LDplayer for bot

file_path = "\\LDPlayer\\LDPlayer9\\dnconsole.exe"

close_LD = [
    file_path,
    "quit",
    "--name",
    "Arknights_Bot"
]
configure_LD = [
    file_path,
    "modify",
    "--name",
    "Arknights_Bot",
    "--resolution",
    "1280,720,240",
    "--cpu",
    "4",
    "--memory",
    "4096"
]
launch_LD = [
    file_path,
    "launch",
    "--name",
    "Arknights_Bot"
]
launch_AK = [
    file_path,
    "runapp",
    "--name",
    "Arknights_Bot",
    "--packagename",
    "com.YoStarEN.Arknights"
]

is_ld_done_initializing = [
    file_path,
    "adb",
    "--name",
    "Arknights_Bot",
    "--command",
    "shell getprop sys.boot_completed"
]

quit_AK = [
    file_path,
    "killapp",
    "--name",
    "Arknights_Bot",
    "--packagename",
    "com.YoStarEN.Arknights"
]

# Commands for image recognition

# Takes a screenshot of emulator window and saves it into the shared folder
# Using this method so bot can run in background behind other windows despite the writes to disk
take_screenshot = [
    file_path,
    "adb",
    "--name",
    "Arknights_Bot",
    "--command",
    "shell screencap -p /mnt/shared/Pictures/ss.png"
]

# Commands for navigation

swipe_left = [
    file_path,
    "adb",
    "--name",
    "Arknights_Bot",
    "--command",
    "shell input swipe 600 550 1260 550 500"
]
swipe_right = [
    file_path,
    "adb",
    "--name",
    "Arknights_Bot",
    "--command",
    "shell input swipe 1260 550 600 550 500"
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
        close_LD,
        configure_LD,
        launch_LD,
        launch_AK
    ]
    # App will not launch if LDplayer is not fully initialized
    for index, command in enumerate(commands):
        # Added delay between close and launch command as getprop sys.boot_completed returns false positive if called
        # too quickly after closing
        if index == 1:
            sleep(2)
        if index >= 3:
            while is_ld_initialized() is not True:
                sleep(5)
        run_command(command, timeout=5)


def is_ld_initialized():
    if subprocess.run(is_ld_done_initializing, capture_output=True, text=True).stdout.strip() == "1":
        logger.log("LD initialized, starting Arknights")
        return True
    else:
        logger.log("LD not fully initialized yet")


def restart_AK():
    logger.log("Restarting Arknights")
    run_command(quit_AK, timeout=5)
    sleep(1)
    run_command(launch_AK, timeout=5)


def capture_screen():
    run_command(take_screenshot, timeout=5)


def click_on_location(point: tuple, delay_before=0, delay_after=0):
    sleep(delay_before)
    x, y = point
    click = [
        file_path,
        "adb",
        "--name",
        "Arknights_Bot",
        "--command",
        "shell input tap " + str(x) + " " + str(y)
    ]
    run_command(click, timeout=5)
    sleep(delay_after)


def scroll(direction):
    if direction == "left":
        run_command(swipe_left, timeout=5)
    if direction == "right":
        run_command(swipe_right, timeout=5)
