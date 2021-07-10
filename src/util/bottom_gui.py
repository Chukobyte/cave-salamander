from seika.node import TextLabel
from src.util.util import Timer


class BottomGUI:
    def __init__(self, time_label: TextLabel):
        self.time_label = time_label
        self.timer = Timer(time_in_millis=120000)
        self.time = 120000

    def update(self) -> None:
        self.timer.tick()
        self.time_label.text = f"Time: {self.timer.time / 1000}"
