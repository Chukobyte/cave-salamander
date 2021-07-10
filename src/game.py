from seika.node import Node2D, TextLabel
from seika.input import Input
from seika.engine import Engine
from seika.math import Vector2, Rect2
from seika.camera import Camera
from seika.physics import Collision
from seika.audio import Audio

from src.game_object import GameObjectType
from src.stats import PlayerStats
from src.util.gui import GUI
from src.util.game_object_pool import GameObjectPool


class Game(Node2D):
    def _start(self) -> None:
        self.frogger = self.get_node(name="Frog")
        self.frogger_collider = self.get_node(name="FrogCollider")
        self.frog_initial_position = self.frogger.position
        self.grid_size = Vector2(16, 16)
        self.player_stats = PlayerStats()
        self.game_gui = GUI(
            score_label=self.get_node(name="ScoreValueLabel"),
            time_label=self.get_node(name="TimeLabel"),
            player_stats=self.player_stats,
        )
        self.game_object_pool = GameObjectPool(
            game=self, snake_node_names=["Snake0", "Snake1"]
        )
        Camera.set_zoom(zoom=Vector2(2, 2))

        Audio.play_music(music_id="assets/audio/music/cave_salamander_theme.wav")

        self.spawn_test_game_objects()

    def _physics_process(self, delta_time: float) -> None:
        if Input.is_action_just_pressed(action_name="ui_quit"):
            Engine.exit()

        self.handle_game_input()

        self.process_collisions()

        self.game_gui.update()

    def handle_game_input(self) -> None:
        if Input.is_action_just_pressed(action_name="move_left"):
            self.frogger.add_to_position(Vector2(-self.grid_size.x, 0))
            Audio.play_sound(sound_id="assets/audio/sound_effect/frog_move_sound.wav")
        elif Input.is_action_just_pressed(action_name="move_right"):
            self.frogger.add_to_position(Vector2(self.grid_size.x, 0))
            Audio.play_sound(sound_id="assets/audio/sound_effect/frog_move_sound.wav")
        if Input.is_action_just_pressed(action_name="move_up"):
            self.frogger.add_to_position(Vector2(0, -self.grid_size.y))
            Audio.play_sound(sound_id="assets/audio/sound_effect/frog_move_sound.wav")
        elif Input.is_action_just_pressed(action_name="move_down"):
            self.frogger.add_to_position(Vector2(0, self.grid_size.y))
            Audio.play_sound(sound_id="assets/audio/sound_effect/frog_move_sound.wav")

    def process_collisions(self) -> None:
        collided_nodes = Collision.get_collided_nodes(node=self.frogger_collider)
        for collided_node in collided_nodes:
            self.player_stats.score += 10
            self.frogger.position = self.frog_initial_position
            break

    # TODO: Test function for spawning.  Move logic into proper place!
    def spawn_test_game_objects(self) -> None:
        snake0 = self.game_object_pool.create(type=GameObjectType.SNAKE)
        snake0.position = Vector2(100, 100)
        print(f"snake = {snake0.entity_id}")
        snake1 = self.game_object_pool.create(type=GameObjectType.SNAKE)
        snake1.position = Vector2(200, 200)
        print(f"snake = {snake1.entity_id}")
