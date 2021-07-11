from seika.node import Node2D
from seika.input import Input
from seika.scene import SceneTree
from seika.engine import Engine
from seika.audio import Audio
from seika.camera import Camera
from seika.math import Vector2
from src.stats import PlayerStats
from src.util.gui import GUI


class EndScreen(Node2D):
    def _start(self):
        Camera.set_zoom(Vector2(1, 1))
        Audio.stop_music()
        Audio.play_music(music_id="assets/audio/music/end_game_jingle.wav", loops=False)
        self.player_stats = PlayerStats()
        self.update_screen()

    def update_screen(self):
        game_gui = GUI(
            score_label=self.get_node(name="ScoreLabel"),
            # time_label=self.get_node(name="TimeLabel"),
            player_stats=self.player_stats,
        )
        final_score_text = "Final Score: {0}".format(self.player_stats.score)
        game_gui.top_gui.update_text(text=final_score_text)

    def _physics_process(self, delta_time: float) -> None:
        if Input.is_action_just_pressed(action_name="ui_menu_confirm"):
            self.player_stats.reset()
            SceneTree.change_scene(scene_path="scenes/title_screen.sscn")

        if Input.is_action_just_pressed(action_name="ui_quit"):
            Engine.exit()
