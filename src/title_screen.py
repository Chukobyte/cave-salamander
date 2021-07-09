from seika.node import Node2D
from seika.input import Input
from seika.scene import SceneTree
from seika.engine import Engine

class Title_screen(Node2D):
    def _physics_process(self, delta_time: float) -> None:
        if Input.is_action_just_pressed(action_name="ui_menu_confirm"):
            SceneTree.change_scene(scene_path="scenes/game.sscn")

        if Input.is_action_just_pressed(action_name="ui_quit"):
            Engine.exit()
