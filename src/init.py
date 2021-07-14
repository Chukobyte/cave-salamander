from seika.node import Node2D
from seika.scene import SceneTree


class Init(Node2D):
    def _start(self) -> None:
        #SceneTree.change_scene(scene_path="scenes/control_screen.sscn")
        SceneTree.change_scene(scene_path="scenes/title_screen.sscn")
