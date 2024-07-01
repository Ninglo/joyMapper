from pynput.keyboard import Key
from pynput.mouse import Button

KEY_MAP = {
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
    "page_up": Key.page_up,
    "page_down": Key.page_down,
    #
    "esc": Key.esc,
    "cmd": Key.cmd,
    "alt": Key.alt,
    "ctrl": Key.ctrl,
    "shift": Key.shift,
    "enter": Key.enter,
    #
    "f12": Key.f12,
}

MOUSE_MAP = {
    "left": Button.left,
    "right": Button.right,
    "middle": Button.middle,
}


def getKeyByStr(str, device):
    _map = KEY_MAP if device == "keyboard" else MOUSE_MAP
    if str in _map.keys():
        return _map[str]

    if len(str) == 1:
        return str
    return None
