from seika.node import Node2D, TextLabel
from seika.input import Input
from seika.engine import Engine
from seika.math import Vector2, Rect2
from seika.camera import Camera
from seika.physics import Collision
from seika.audio import Audio
from seika.scene import SceneTree

from src.game_object import GameObjectType
from src.lane_manager import LaneManager
from src.stats import PlayerStats
from src.util.gui import GUI, BottomGUI
from src.util.game_object_pool import GameObjectPool
from src.util.util import GameScreen


class Game(Node2D):
    def _start(self) -> None:
        # GameScreen().BOTTOM_UI_BUFFER = BottomGUI.RECT_HEIGHT
        GameScreen().setBottomBuffer(buffer=BottomGUI.RECT_HEIGHT)

        self.salamander = self.get_node(name="Salamander")
        self.salamander_collider = self.get_node(name="SalamanderCollider")
        # This position should be divisible by the grid size
        self.salamander_initial_position = self.salamander.position
        self.grid_size = (
            GameScreen().getGridSize()
        )  # Vector2(16, 16)  # the sprite's size
        self.player_stats = PlayerStats()
        self.game_gui = GUI(
            score_label=self.get_node(name="ScoreValueLabel"),
            time_label=self.get_node(name="TimeLabel"),
            player_stats=self.player_stats,
        )
        zoom_vector = GameScreen().getZoom()  # Vector2(2, 2)
        Camera.set_zoom(zoom=zoom_vector)
        self.total_salamander_frames = self.salamander.animation_frames
        Audio.play_music(
            music_id="assets/audio/music/cave_salamander_theme.wav", loops=True
        )

        self.screen_width_scaled = GameScreen().getScreenScaled().x
        self.screen_height_scaled = GameScreen().getScreenScaled().y

        self.lane_manager = LaneManager(
            game_object_pool=GameObjectPool(
                game=self,
                rock_node_names=["SmallRock0"],
                snake_node_names=["Snake0", "Snake1"],
                spider_node_names=["Spider0", "Spider1"],
            )
        )

    def _physics_process(self, delta_time: float) -> None:
        if Input.is_action_just_pressed(action_name="ui_quit"):
            Engine.exit()

        self.handle_game_input()

        self.game_gui.update()

        self.lane_manager.process(delta_time=delta_time)

        self.process_collisions()

        self.death_check()

    def handle_game_input(self) -> None:
        player_moved = True
        new_x, new_y = 0, 0
        curr_x = self.salamander.get_position().x
        curr_y = self.salamander.get_position().y

        if Input.is_action_just_pressed(action_name="move_left"):
            new_x = -self.grid_size.x
        elif Input.is_action_just_pressed(action_name="move_right"):
            new_x = self.grid_size.x
        elif Input.is_action_just_pressed(action_name="move_up"):
            new_y = -self.grid_size.y
        elif Input.is_action_just_pressed(action_name="move_down"):
            new_y = self.grid_size.y
        elif Input.is_action_just_pressed(
            action_name="RESET"
        ):  # pressing 'r' for debugging
            self.salamander.position = self.salamander_initial_position
            player_moved = False
            self.player_stats.reset()
            SceneTree.change_scene(scene_path="scenes/title_screen.sscn")
        elif Input.is_action_just_pressed(
            action_name="End"
        ):  # pressing 'r' for debugging
            SceneTree.change_scene(scene_path="scenes/end_screen.sscn")
        elif Input.is_action_just_pressed(
            action_name="Score"
        ):  # pressing 'm' for adding to score points
            self.player_stats.score = (self.player_stats.score + 1) % 10
            self.game_object_pool.move_gameobjects_in_pool()
        else:
            player_moved = False

        # checks if player is within screen boundary. IF so, move player and update animation.
        if (
            curr_x + new_x >= 0
            and curr_x + new_x < self.screen_width_scaled
            and curr_y + new_y >= 0
            and curr_y + new_y < self.screen_height_scaled
            and player_moved
        ):
            self.salamander.add_to_position(Vector2(new_x, new_y))
            self.cycle_salamander_animation()
        elif (
            curr_x < 0
            or curr_y < 0
            or curr_x > self.screen_width_scaled - self.grid_size.x
            or curr_y > self.screen_height_scaled
        ):
            # reset position if somehow outside of screen
            self.salamander.position = self.salamander_initial_position

    def process_collisions(self) -> None:
        collided_nodes = Collision.get_collided_nodes(node=self.salamander_collider)
        for collided_node in collided_nodes:
            reset_position = False

            if "enemy" in collided_node.tags:
                reset_position = True
                self.player_stats.lives -= 1
                if self.player_stats.lives > 0:
                    Audio.play_sound(sound_id="assets/audio/sound_effect/lose_life.wav")
            elif "goal" in collided_node.tags:
                reset_position = True
                points = int(self.game_gui.bottom_gui.timer.time / 1000)
                self.player_stats.score += points
                Audio.play_sound(sound_id="assets/audio/sound_effect/score_goal.wav")

            if reset_position:
                self.salamander.position = self.salamander_initial_position
            break

    def cycle_salamander_animation(self):
        self.salamander.frame = (
            self.salamander.frame + 1
        ) % self.total_salamander_frames
        Audio.play_sound(sound_id="assets/audio/sound_effect/frog_move_sound.wav")

    def death_check(self):
        if self.player_stats.lives <= 0 or self.game_gui.bottom_gui.timer.time <= 0:
            SceneTree.change_scene(scene_path="scenes/end_screen.sscn")
