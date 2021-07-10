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
    # TODO: Is there a better way to check for Project's resolution/screensize?
    # A project's resolution is also it's size?
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    def _start(self) -> None:
        self.frogger = self.get_node(name="Frog")
        self.frogger_collider = self.get_node(name="FrogCollider")
        self.frog_initial_position = self.frogger.position  # This position should be divisible by the grid size
        self.grid_size = Vector2(16, 16) # the sprite's size
        self.player_stats = PlayerStats()
        self.game_gui = GUI(
            score_label=self.get_node(name="ScoreValueLabel"),
            time_label=self.get_node(name="TimeLabel"),
            player_stats=self.player_stats,
        )
        self.game_object_pool = GameObjectPool(
            game=self, snake_node_names=["Snake0", "Snake1"]
        )
        zoom_vector = Vector2(2, 2)
        Camera.set_zoom(zoom=zoom_vector)

        Audio.play_music(music_id="assets/audio/music/cave_salamander_theme.wav")

        self.spawn_test_game_objects()
        # z = dir(Camera)
        # for x in z:
        #     print(x)
        #scaled refers considers zoom level
        self.screen_width_scaled = self.SCREEN_WIDTH / zoom_vector.x

        print(self.game_gui.bottom_gui.RECT_HEIGHT)
        self.screen_height_scaled = ((self.SCREEN_HEIGHT) / zoom_vector.y)- (self.game_gui.bottom_gui.RECT_HEIGHT/3)
        #print(self.screen_width_scaled, self.screen_height_scaled)\
        print("HERE15")

    def _physics_process(self, delta_time: float) -> None:
        if Input.is_action_just_pressed(action_name="ui_quit"):
            Engine.exit()

        self.handle_game_input()

        self.process_collisions()

        self.game_gui.update()

    def handle_game_input(self) -> None:
        player_moved = True
        new_x, new_y = 0, 0
        curr_x = self.frogger.get_position().x
        curr_y = self.frogger.get_position().y

        if Input.is_action_just_pressed(action_name="move_left"):
            new_x = -self.grid_size.x
        elif Input.is_action_just_pressed(action_name="move_right"):
            new_x = self.grid_size.x
        elif Input.is_action_just_pressed(action_name="move_up"):
            new_y = -self.grid_size.y
        elif Input.is_action_just_pressed(action_name="move_down"):
            new_y = self.grid_size.y
        elif Input.is_action_just_pressed(action_name="RESET"): #pressing 'r' for debugging
            self.frogger.position = self.frog_initial_position
            player_moved = False
        else:
            player_moved = False

        # checks if player is within screen boundary. IF so, move player and update animation.
        if(
                curr_x + new_x >=0 and curr_x + new_x < self.screen_width_scaled and
                curr_y + new_y >=0 and curr_y + new_y < self.screen_height_scaled and
                player_moved
        ):
            self.frogger.add_to_position(Vector2(new_x, new_y))
            self.cycle_frogger_animation()
            #print(curr_x, curr_y)
        elif curr_x < 0 or curr_y < 0 or curr_x > self.screen_width_scaled-self.grid_size.x or curr_y > self.screen_height_scaled:
            #reset position if somehow outside of screen
            self.frogger.position = self.frog_initial_position

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

    def cycle_frogger_animation(self):
        self.frogger.frame = (self.frogger.frame + 1) % self.total_frogger_frames
        Audio.play_sound(sound_id="assets/audio/sound_effect/frog_move_sound.wav")
