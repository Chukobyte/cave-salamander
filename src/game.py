from seika.node import Node2D
from seika.input import Input
from seika.engine import Engine

class Game(Node2D):
    def _physics_process(self, delta_time: float) -> None:
        if Input.is_action_just_pressed(action_name="ui_quit"):
            Engine.exit()
