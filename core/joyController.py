from functools import reduce
import queue
import threading
from typing import Any, List
import pygame
from pynput.keyboard import Controller as Keyboard
from pynput.mouse import Controller as Mouse

from key import getKeyByStr
from macro import Macro
from configs import configMap 


def clip(x: int) -> int:
    return max(min(x, 1), -1)


def add_lists(list1, list2):
    return [a + b for a, b in zip(list1, list2)]


class Action:
    def __init__(this, device: str, type: str, value) -> None:
        this.device = device
        this.type = type
        this.value = value if isinstance(value, list) else [value]


def inDeadAreas(_location: int, deadAreas: List[Any]) -> bool:
    location = _location
    for [start, end] in deadAreas:
        if start <= location <= end:
            return True
    return False


def mapEvent(event: pygame.event.Event, config: Any) -> Action:
    if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
        index = event.button
        if index >= len(config["buttons"]):
            return None

        buttonConfig = config["buttons"][index]
        device = buttonConfig["device"]
        type = buttonConfig["type"]
        value = buttonConfig["value"]
        if device == "macro" and event.type == pygame.JOYBUTTONDOWN:
            return Action(device, f"{type}_down", value)
        if device == "macro" and event.type == pygame.JOYBUTTONUP:
            return Action(device, f"{type}_up", value)
        if (device == "keyboard" or device == "mouse") and type == "click":
            actionType = "press" if event.type == pygame.JOYBUTTONDOWN else "release"
            key = getKeyByStr(value, device)
            if key == None:
                return None
            return Action(device, actionType, key)
        if device == "mouse" and type == "move":
            return (
                Action(device, type, value) if event == pygame.JOYBUTTONDOWN else None
            )
        if device == "mouse" and type == "scroll":
            return (
                Action(device, type, value) if event == pygame.JOYBUTTONDOWN else None
            )

    if event.type == pygame.JOYAXISMOTION:
        index: int = event.axis
        location: int = clip(event.value)
        if index >= len(config["axis"]):
            return None

        axisConfig = config["axis"][index]
        device = axisConfig["device"]
        type = axisConfig["type"]
        value = axisConfig["value"]
        deadAreas = value["deadAreas"]
        if inDeadAreas(location, deadAreas):
            return None

        if device == "macro":
            return Action(device, actionType, value)
        if (device == "keyboard" or device == "mouse") and type == "click":
            key = getKeyByStr(value, device)
            if key == None:
                return None
            return Action(device, type, key)
        if device == "mouse" and (type == "move" or type == "scroll"):
            proportion = value["proportion"]
            location = 1 if event.value > 0 else -1 if event.value < 0 else 0
            return Action(
                device,
                type,
                [proportion["x"] * location, proportion["y"] * location],
            )

    if event == pygame.JOYHATMOTION:
        print(event)
        return


JOY_INPUT_EVENTS = [
    pygame.JOYBUTTONDOWN,
    pygame.JOYBUTTONUP,
    pygame.JOYAXISMOTION,
    pygame.JOYHATMOTION,
]


class JoyController:
    def __init__(this, configQueue: queue.Queue, stopEvent: threading.Event) -> None:
        if configQueue.empty():
            raise "config not exist"

        this._configQueue = configQueue
        this._stopEvent = stopEvent
        keyboard = Keyboard()
        mouse = Mouse()
        macro = Macro(keyboard)
        this._device = {
            "keyboard": keyboard,
            "mouse": mouse,
            "macro": macro,
        }
        this._config = this._getConfig()

        this._init()

    def _init(this):
        pygame.init()
        pygame.joystick.init()

        this._listenJoyEvent()

    def _getConfig(this) -> Any:
        if this._configQueue.empty():
            return this._config
        else:
            config = None
            while not this._configQueue.empty():
                config = this._configQueue.get()
                this._configQueue.task_done()
            return config

    def _makeAction(this, event: pygame.event.Event) -> Action:
        config = this._getConfig()
        action = mapEvent(event, config)
        return action

    def _doAction(this, action: Action) -> None:
        device = action.device
        type = action.type
        value = action.value

        method = getattr(this._device[device], type, None)
        if method:
            method(*value)

    def _isDnoe(this) -> bool:
        return this._stopEvent.is_set()

    def _listenJoyEvent(this) -> None:
        while True:
            events = pygame.event.get()
            actions = []
            for event in events:
                if this._isDnoe():
                    return
                if event.type == pygame.QUIT:
                    this._quit()
                    return
                if event.type == pygame.JOYDEVICEADDED:
                    index = event.dict["device_index"]
                    stick = pygame.joystick.Joystick(index)
                    stick.init()
                if event.type in JOY_INPUT_EVENTS:
                    action = this._makeAction(event)
                    if action:
                        actions.append(action)

            if len(actions):
                mouseMoveValue = reduce(
                    add_lists,
                    map(
                        lambda action: action.value,
                        filter(lambda action: action.type == "move", actions),
                    ),
                    [0, 0],
                )
                mouseScrollValue = reduce(
                    add_lists,
                    map(
                        lambda action: action.value,
                        filter(lambda action: action.type == "scroll", actions),
                    ),
                    [0, 0],
                )
                anotherActions = list(
                    filter(
                        lambda action: action.type not in ["move", "scroll"], actions
                    )
                )
                anotherActions.append(Action("mouse", "move", mouseMoveValue))
                anotherActions.append(Action("mouse", "scroll", mouseScrollValue))
                for action in anotherActions:
                    this._doAction(action)

    def _quit(this) -> None:
        pygame.quit()


if __name__ == "__main__":
    config = configMap['vscode']
    configQueue = queue.Queue()
    configQueue.put(config)
    stopEvent = threading.Event()
    controller = JoyController(configQueue, stopEvent)
