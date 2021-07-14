from seika.node import Node2D
from seika.camera import Camera
from seika.color import Color
from seika.node import Node2D
from seika.input import Input
from seika.scene import SceneTree
from seika.engine import Engine
from seika.audio import Audio
from seika.camera import Camera
from seika.math import Vector2
from src.util.util import Timer_delta

class Control_screen(Node2D):
    def _start(self):
        Camera.set_zoom(Vector2(1, 1))
        self.instruction_label = self.get_node(name="InstructionLabel")
        self.instruction_flash_timer = Timer_delta(max_time_in_seconds=0.75)
        self.instruction_show = True

    def _physics_process(self, delta_time: float) -> None:
        if Input.is_action_just_pressed(action_name="ui_menu_confirm"):
            Audio.play_sound(sound_id="assets/audio/sound_effect/frog_move_sound.wav")
            SceneTree.change_scene(scene_path="scenes/game.sscn")

        if Input.is_action_just_pressed(action_name="ui_quit"):
            Engine.exit()

        if self.instruction_flash_timer.tick_n_check(delta_time=delta_time):
            self.instruction_show = not self.instruction_show
            if self.instruction_show:
                self.instruction_label.color = Color(1.0, 1.0, 1.0, 1.0)
            else:
                self.instruction_label.color = Color(1.0, 1.0, 1.0, 0.0)