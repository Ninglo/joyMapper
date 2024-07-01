import queue
from core.config import ConfigService
from core.server import App
from joyController import JoyController
import threading

configQueue = queue.Queue()
stopEvent = threading.Event()

def joyControllerThread():
    JoyController(configQueue, stopEvent)

def main():
    db = DB()
    configService = ConfigService(db, configQueue)
    configService.get
    app = App(configService)
    app.run()
    
    threading.Thread(target=joyControllerThread)
