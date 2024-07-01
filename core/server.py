from flask import Flask, request

from core.config import ConfigService


class App:
    def __init__(this, configService: ConfigService, name=__name__) -> None:
        this._app = Flask(name)
        this._config = configService
        this._registrouter()

    def _registrouter(this):
        this._app.add_url_rule(
            "/activation", "getActivation", this._getActivation, method=["GET"]
        )
        this._app.add_url_rule(
            "/activation", "updateActivation", this._updateActivation, method=["POST"]
        )

        this._app.add_url_rule(
            "/config", "getConfigList", this._getConfigList, method=["GET"]
        )
        this._app.add_url_rule("/config", "addConfig", this._addConfig, method=["PUT"])
        this._app.add_url_rule(
            "/config/<id>", "getConfig", this._getConfig, method=["GET"]
        )
        this._app.add_url_rule(
            "/config/<id>", "updateConfig", this._updateConfig, method=["POST"]
        )

    def _getActivation(this):
        activation = this._config.getActivation()
        return { activation }

    def _updateActivation(this):
        this._config.updateActivation()
        return

    def _getConfig(this, ID):
        config = this._config.getConfig(ID)
        return config

    def _addConfig(this):
        body = request.json
        if not body:
            err
            return

        this._config.addConfig(body)
        return

    def _updateConfig(this, ID):
        body = request.json
        if not body:
            err
            return

        config = this._config.updateConfig(ID, body)
        return config

    def _getConfigList(this):
        return this._config.getConfigList()

    def run(
        this,
        host: str | None = None,
        port: int | None = None,
        debug: bool | None = None,
    ):
        this._app.run(host, port, debug)
