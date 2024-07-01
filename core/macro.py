from pynput.keyboard import Controller as Keyboard

from key import getKeyByStr
from mac import open_mission_control


class Macro:
    def __init__(this, keyboard: Keyboard):
        this._keyboard = keyboard

    def missionControl_down(this, *args):
        open_mission_control()

    def shortcut_down(this, *keys: list[str]) -> None:
        for _key in keys:
            key = getKeyByStr(_key, "keyboard")
            this._keyboard.press(key)

    def shortcut_up(this, *keys: list[str]) -> None:
        for _key in keys:
            key = getKeyByStr(_key, "keyboard")
            this._keyboard.release(key)
