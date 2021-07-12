from seika.node import Node2D
from seika.input import Input
from seika.scene import SceneTree
from seika.engine import Engine
from seika.audio import Audio
from seika.camera import Camera
from seika.math import Vector2


class Title_screen(Node2D):
    def _start(self):
        Camera.set_zoom(Vector2(1, 1))
        Audio.stop_music()

    def _physics_process(self, delta_time: float) -> None:
        if Input.is_action_just_pressed(action_name="ui_menu_confirm"):
            Audio.play_sound(sound_id="assets/audio/sound_effect/frog_move_sound.wav")
            SceneTree.change_scene(scene_path="scenes/game.sscn")

        if Input.is_action_just_pressed(action_name="ui_quit"):
            Engine.exit()
