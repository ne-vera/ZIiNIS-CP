from gui import GUI
from rubik import Cubik

class Controller:
    def __init__(self, gui : GUI, model: Cubik) -> None:
        self.gui = gui
        self.model = model
