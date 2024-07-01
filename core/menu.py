import rumps


class MenuBar(rumps.App):
    def __init__(self):
        super(MenuBar, self).__init__("GamepadMapped", icon="./gamepad.svg")
        self.menu = ["Preferences", "Settings...", "Say hi"]

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("jk! no preferences available!")

    @rumps.clicked("Silly button")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Say hi")
    def sayhi(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

    def _updateMenuBar(this):
        configs = []
        actions = [
            rumps.MenuItem('Preferences')
        ]
        return [*configs, *actions]


if __name__ == "__main__":
    menu = MenuBar()
    menu.run()
