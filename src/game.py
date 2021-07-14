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
from src.util.util import Timer_delta


class Abyss:
    TOP_Y_LIMIT = 22.0
    BOTTOM_Y_LIMIT = 88.0


class Game(Node2D):
    DEBUG = False

    def _start(self) -> None:
        GameScreen().setBottomBuffer(buffer=BottomGUI.RECT_HEIGHT)
        self.end_scene_transition_timer = Timer_delta(max_time_in_seconds=0.5)
        self.ready_to_transition = False

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
        Audio.play_music(
            music_id="assets/audio/music/cave_salamander_theme.wav", loops=True
        )

        self.screen_width_scaled = GameScreen().getScreenScaled().x
        self.screen_height_scaled = GameScreen().getScreenScaled().y

        self.lane_manager = LaneManager(
            game_object_pool=GameObjectPool(
                game=self,
                small_rock_node_names=["SmallRock0"],
                big_rock_left_node_names=[
                    "BigRock0",
                    "BigRock1",
                    "BigRock2",
                    "BigRock3",
                ],
                big_rock_right_node_names=[
                    "BigRock4",
                    "BigRock5",
                    "BigRock6",
                    "BigRock7",
                ],
                bat_left_node_names=["Bat0", "Bat1"],
                snake_node_names=["Snake0", "Snake1"],
                spider_node_names=["Spider0", "Spider1"],
            )
        )

        # Grabbing a dictionary of goal collision node tags as the keys where the value is the Goal Game Object
        # Assumes the Goal's collision's tags and numbering align with the what appears in the game.sscn file, respectively
        self.goals = {}
        goal_objects = [
            self.get_node(name=goal_node_name)
            for goal_node_name in [
                "EndGoalLabel0",
                "EndGoalLabel1",
                "EndGoalLabel2",
                "EndGoalLabel3",
                "EndGoalLabel4",
            ]
        ]
        for x in range(0, len(goal_objects)):
            self.goals[f"goal{x}"] = goal_objects[x]

    def _physics_process(self, delta_time: float) -> None:
        if Input.is_action_just_pressed(action_name="ui_quit"):
            Engine.exit()

        # print(f"fps = {Engine.get_fps()}")

        self.handle_game_input(delta_time=delta_time)

        self.game_gui.update()

        # If player is dying, stop enemies from spawning and moving
        if not self.player_stats.dying:
            self.lane_manager.process(delta_time=delta_time)

        self._process_collisions()

        self.death_check(delta_time=delta_time)

    def handle_game_input(self, delta_time) -> None:
        player_moved = False

        new_x, new_y = 0, 0
        curr_x = self.salamander.get_position().x
        curr_y = self.salamander.get_position().y

        # can_walk = self.player_stats.walking_timer.tick_n_check(delta_time=delta_time)
        can_walk = self.player_stats.check_can_walk(delta_time=delta_time)

        if not self.player_stats.dying:
            if can_walk:
                if Input.is_action_just_pressed(action_name="move_left"):
                    player_moved = True
                    new_x = -self.grid_size.x
                elif Input.is_action_just_pressed(action_name="move_right"):
                    player_moved = True
                    new_x = self.grid_size.x
                elif Input.is_action_just_pressed(action_name="move_up"):
                    player_moved = True
                    new_y = -self.grid_size.y
                elif Input.is_action_just_pressed(action_name="move_down"):
                    player_moved = True
                    new_y = self.grid_size.y

            # Keeping outside of dying check for debugging
            if (
                Input.is_action_just_pressed(action_name="RESET") and self.DEBUG
            ):  # pressing 'r' for debugging
                self.salamander.position = self.salamander_initial_position
                player_moved = False
                self.player_stats.reset()
                SceneTree.change_scene(scene_path="scenes/title_screen.sscn")
            elif (
                Input.is_action_just_pressed(action_name="End") and self.DEBUG
            ):  # pressing 'e' for debugging
                # self.player_stats.end_time = self.game_gui.bottom_gui.timer.time
                # SceneTree.change_scene(scene_path="scenes/end_screen.sscn")
                self.salamander.position = Vector2(
                    self.salamander_initial_position.x, 4
                )
            elif Input.is_action_just_pressed(
                action_name="GetLife"
            ):  # pressing 'Space' bar
                self.check_if_can_add_lives()
        # checks if player is within screen boundary. IF so, move player and update animation.
        if (
            GameScreen.is_position_within_screen(
                position=Vector2(curr_x + new_x, curr_y + new_y)
            )
            and player_moved
        ):
            self.player_stats.can_walk = False
            self.salamander.add_to_position(Vector2(new_x, new_y))
            if (
                self._is_salamander_in_abyss()
                and not self._is_salamander_on_step_on_object()
            ):
                self._process_salamander_death()
            else:
                self._cycle_salamander_animation()
        elif (
            curr_x < 0
            or curr_y < 0
            or curr_x > self.screen_width_scaled - self.grid_size.x
            or curr_y > self.screen_height_scaled
        ):
            # reset position if somehow outside of screen
            self.salamander.position = self.salamander_initial_position

    def _process_collisions(self) -> None:
        if not self.player_stats.dying:
            step_on = False
            Collision.update_collisions(node=self.salamander_collider)
            collided_nodes = Collision.get_collided_nodes(node=self.salamander_collider)
            for collided_node in collided_nodes:
                reset_position = False

                if "enemy" in collided_node.tags:
                    self._process_salamander_death()
                elif "step_on" in collided_node.tags:
                    for (
                        moved_object
                    ) in (
                        self.lane_manager.game_object_movement_context.moved_game_objects
                    ):
                        if moved_object.collider == collided_node:
                            # TODO: may need to adjust for different speeds
                            if GameScreen.is_position_within_screen(
                                position=self.salamander.position
                                + moved_object.last_moved_velocity
                            ):
                                self.salamander.add_to_position(
                                    moved_object.last_moved_velocity
                                )
                            break
                    step_on = True
                elif any(item in self.goals for item in collided_node.tags):
                    # assumes the goal tag is the first element
                    goal_tag = collided_node.tags[0]
                    reset_position = True
                    points = int(self.game_gui.bottom_gui.timer.time / 1000)
                    self.player_stats.score += points * 2
                    self.player_stats.goals -= 1
                    self.goals[goal_tag].move_off_screen()
                    Audio.play_sound(
                        sound_id="assets/audio/sound_effect/score_goal.wav"
                    )

                    # Keep player where they are once they get all the goals
                    if self.player_stats.goals <= 0:
                        reset_position = False

                if reset_position:
                    self.salamander.position = self.salamander_initial_position
                break
            if not step_on and self._is_salamander_in_abyss():
                self._process_salamander_death()
            self.lane_manager.game_object_movement_context.clear()

    def reset_salamander_position(self):
        self.salamander.position = self.salamander_initial_position
        self.salamander.set_animation(animation_name="walk")
        self.player_stats.dying = False

    def _cycle_salamander_animation(self):
        self.salamander.frame = (
            self.salamander.frame + 1
        ) % self.salamander.animation_frames
        Audio.play_sound(sound_id="assets/audio/sound_effect/frog_move_sound.wav")

    def _is_salamander_in_abyss(self) -> bool:
        pos_y = self.salamander.position.y
        if Abyss.TOP_Y_LIMIT <= pos_y <= Abyss.BOTTOM_Y_LIMIT:
            return True
        return False

    def _is_salamander_on_step_on_object(self) -> bool:
        Collision.update_collisions(node=self.salamander_collider)
        for collided_node in Collision.get_collided_nodes(
            node=self.salamander_collider
        ):
            if "step_on" in collided_node.tags:
                return True
        return False

    def _process_salamander_death(self) -> None:
        self.player_stats.lives -= 1
        if self.player_stats.lives >= 0:
            self.player_stats.dying = True
            Audio.play_sound(sound_id="assets/audio/sound_effect/lose_life.wav")
            # self.salamander.play(animation_name="death")
            # have to set since 'death' animation doesn't have more than 1 frame
            self.salamander.frame = 0
            self.salamander.set_animation(animation_name="death")

    def death_check(self, delta_time):
        # Death check
        if (
            self.player_stats.lives <= 0
            or self.player_stats.goals <= 0
            or self.game_gui.bottom_gui.timer.time <= 0
        ):
            # Run transition timer get to end screen
            self.player_stats.dying = True
            self.player_stats.end_time = self.game_gui.bottom_gui.timer.time
            if self.end_scene_transition_timer.tick_n_check(delta_time=delta_time):
                SceneTree.change_scene(scene_path="scenes/end_screen.sscn")

        elif self.player_stats.dying:
            if self.player_stats.dying_timer.tick_n_check(delta_time=delta_time):
                self.reset_salamander_position()

    # only intended for when getting goal
    def check_if_can_add_lives(self):
        if (
            self.player_stats.lives < self.player_stats.MAX_LIVES
            and self.player_stats.score >= 1000
        ):
            self.player_stats.lives += 1
            self.player_stats.score -= 1000
