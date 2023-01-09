
import subprocess
from time import sleep


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

def main():
    #Launch commands to prepare emulator for bot
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
    run_command(args=closeLD, timeout = 5)
    run_command(args=configureLD, timeout=5)
    run_command(args=launchLD, timeout=5)
    #Delay to allow LD to initialize
    sleep(5)
    run_command(args=launchAK, timeout=5)

if __name__ == "__main__":
    main()