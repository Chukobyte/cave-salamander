from seika.color import Color
from seika.math import Vector2, Rect2
from seika.renderer import Renderer

from src.game_object import GameObjectType, GameObject
from src.util.game_object_pool import GameObjectPool
import random


class GameObjectMovementContext:
    def __init__(self):
        self._moved_game_objects = []
        self.player_step_on_game_object = None

    @property
    def moved_game_objects(self) -> list:
        return self._moved_game_objects.copy()

    def add(self, game_object: GameObject) -> None:
        self._moved_game_objects.append(game_object)

    def clear(self) -> None:
        self._moved_game_objects.clear()


class Lane:
    def __init__(
        self,
        position: Vector2,
        capacity: int,
        index: int,
        game_object_type: str,
        max_time: float = -1,
    ):
        self.position = position
        self.capacity = capacity
        self.index = index
        self.game_object_type = game_object_type
        self.MAX_SPAWN_TIME = (
            max_time if max_time >= 0 else round(random.uniform(0.5, 1.5), 1)
        )  # for seconds
        self.timer = self.MAX_SPAWN_TIME
        # print(self.MAX_SPAWN_TIME)

    def can_spawn(self, delta_time) -> bool:
        if self.timer <= 0:
            self.timer = self.MAX_SPAWN_TIME
            return self.capacity > 0
        else:
            self.timer -= delta_time
            return False

    def draw(self, camera_zoom=Vector2(2, 2)) -> None:
        Renderer.draw_texture(
            texture_path="assets/images/white_square.png",
            source_rect=Rect2(0, 0, 2, 2),
            dest_rect=Rect2(
                self.position.x * camera_zoom.x, self.position.y * camera_zoom.y, 16, 16
            ),
            z_index=-1,
            color=Color(1.0, 1.0, 1.0),
        )


STEP_ON_OBJECT_TYPES = [GameObjectType.BIG_ROCK_LEFT, GameObjectType.BIG_ROCK_RIGHT]


class LaneManager:
    def __init__(self, game_object_pool: GameObjectPool):
        self.game_object_movement_context = GameObjectMovementContext()
        self._game_object_pool = game_object_pool
        self._lanes = self._get_initial_lanes()

    def _get_initial_lanes(self) -> dict:
        return {
            0: Lane(
                position=Vector2(0, 168),
                capacity=1,
                index=0,
                game_object_type=GameObjectType.SPIDER,
                max_time=0.5,
            ),
            1: Lane(
                position=Vector2(384, 152),
                capacity=1,
                index=1,
                game_object_type=GameObjectType.SNAKE,
            ),
            2: Lane(
                position=Vector2(0, 136),
                capacity=1,
                index=2,
                game_object_type=GameObjectType.SPIDER,
            ),
            3: Lane(
                position=Vector2(384, 120),
                capacity=1,
                index=3,
                game_object_type=GameObjectType.SMALL_ROCK,
                max_time=1.5,
            ),
            4: Lane(
                position=Vector2(384, 88),
                capacity=2,
                index=4,
                game_object_type=GameObjectType.BIG_ROCK_LEFT,
                max_time=1.5,
            ),
            5: Lane(
                position=Vector2(0, 72),
                capacity=2,
                index=5,
                game_object_type=GameObjectType.BIG_ROCK_RIGHT,
                max_time=1.5,
            ),
            6: Lane(
                position=Vector2(384, 56),
                capacity=2,
                index=6,
                game_object_type=GameObjectType.BIG_ROCK_LEFT,
                max_time=2.0,
            ),
            7: Lane(
                position=Vector2(0, 40),
                capacity=2,
                index=7,
                game_object_type=GameObjectType.BIG_ROCK_RIGHT,
                max_time=2.0,
            ),
            8: Lane(
                position=Vector2(384, 24),
                capacity=1,
                index=8,
                game_object_type=GameObjectType.BIG_ROCK_LEFT,
                max_time=2.5,
            ),
        }

    def process(self, delta_time: float) -> None:
        for lane_index in self._lanes:
            lane = self._lanes[lane_index]
            lane.draw()
            # Always checking if can spawn for now
            if lane.can_spawn(delta_time=delta_time):
                # a minor redundant but necessary call, since attempt_spawn can return None and crash game
                if self._game_object_pool.is_spawnable(lane.game_object_type):
                    game_object = self._game_object_pool.attempt_spawn(
                        type=lane.game_object_type
                    )
                    game_object.position = lane.position
                    game_object.spawn_lane_index = lane.index
                    lane.capacity -= 1

        # Movement
        dead_game_object_pool = []
        for live_game_object in self._game_object_pool.live_pool:
            if (
                live_game_object.move_object(delta_time=delta_time)
                and live_game_object.type in STEP_ON_OBJECT_TYPES
            ):
                self.game_object_movement_context.add(game_object=live_game_object)
            if not live_game_object.active:
                dead_game_object_pool.append(live_game_object)

        # Clean up
        for dead_game_object in dead_game_object_pool:
            lane_to_cleanup = self._lanes[dead_game_object.spawn_lane_index]
            lane_to_cleanup.capacity += 1
            self._game_object_pool.remove_object(game_object=dead_game_object)
