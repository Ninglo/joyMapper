import queue
from typing import Any, List

class ConfigService:
    def __init__(this, db, configQueue: queue.Queue) -> None:
        this._db = db
        this._queue = configQueue

    def getActivation(this) -> str:
        activation = this._db.get('act')
        return activation

    def getActivationConfig(this) -> Any:
        activation = this._db.get('act')
        configs = this._db.get('config')
        activationConfig = next(filter(lambda config: config.id == activation, configs))
        return activationConfig

    def updateActivation(this, ID: str) -> None:
        this._db.update()
        configs = this._db.get(config)
        config = next(filter(lambda config: config.id == ID, configs), None)
        this._queue.put(config)
        return

    def getConfig(this, ID: str):
        config = this._db.get(ID)
        return config

    def addConfig(this, config: "ConfigService") -> None:
        this._db.add(config)
        this._db.update(activate, config.id)
        return

    def updateConfig(this, ID: str, config: "ConfigService") -> Config:
        updatedConfig = this._db.update(ID, config)
        return updatedConfig

    def getConfigList(this) -> List["ConfigService"]:
        activation = this._db.get(activation)
        _configs = this._db.get(config)
        configs = map(lambda config: {'url': f'/api/config/{config.id}', 'activation': config.id == activation}, _configs)
        return configs
