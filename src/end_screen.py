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
        self.instruction_label = self.get_node(name="InstructionLabel")
        self.LOSE_TEXT = "Press Enter to get back to Main Menu"
        self.WIN_TEXT = "Press Enter to continue playing"
        self.update_screen()

    def update_screen(self):
        game_gui = GUI(
            score_label=self.get_node(name="ScoreLabel"),
            time_label=self.get_node(name="TimeLabel"),
            player_stats=self.player_stats,
        )
        final_score_text = "Final Score: {0}".format(self.player_stats.score)
        game_gui.top_gui.update_text(text=final_score_text)
        game_gui.bottom_gui.time_label.text = (
            f"Time: {self.player_stats.end_time / 1000}"
        )
        if self.player_stats.goals <= 0:
            end_title_label = self.get_node(name="EndTitle")
            end_title_label.text = "You Win !"
            self.instruction_label.text = self.WIN_TEXT
        else:
            self.instruction_label.text = self.LOSE_TEXT

    def _physics_process(self, delta_time: float) -> None:
        if Input.is_action_just_pressed(action_name="ui_menu_confirm"):
            if self.player_stats.goals <= 0:
                self.player_stats.sub_reset()
                Audio.play_sound(
                    sound_id="assets/audio/sound_effect/frog_move_sound.wav"
                )
                SceneTree.change_scene(scene_path="scenes/game.sscn")
            else:
                self.player_stats.reset()
                Audio.play_sound(
                    sound_id="assets/audio/sound_effect/frog_move_sound.wav"
                )
                SceneTree.change_scene(scene_path="scenes/title_screen.sscn")

        if Input.is_action_just_pressed(action_name="RESET"):
            self.player_stats.reset()
            Audio.play_sound(sound_id="assets/audio/sound_effect/frog_move_sound.wav")
            SceneTree.change_scene(scene_path="scenes/game.sscn")

        if Input.is_action_just_pressed(action_name="ui_quit"):
            Engine.exit()
