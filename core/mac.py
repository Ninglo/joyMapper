import subprocess


def open_mission_control():
    applescript_command = """
    tell application "System Events" to key code 126 using control down
    """
    subprocess.run(["osascript", "-e", applescript_command])
