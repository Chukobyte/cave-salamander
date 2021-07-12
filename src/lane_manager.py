from seika.color import Color
from seika.math import Vector2, Rect2
from seika.renderer import Renderer

from src.game_object import GameObjectType
from src.util.game_object_pool import GameObjectPool


class Lane:
    def __init__(
        self, position: Vector2, capacity: int, index: int, game_object_type: str
    ):
        self.position = position
        self.capacity = capacity
        self.index = index
        self.game_object_type = game_object_type

    # TODO: add in a timer for some thing when capacity is above 1
    def can_spawn(self) -> bool:
        return self.capacity > 0

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


class LaneManager:
    def __init__(self, game_object_pool: GameObjectPool):
        self._game_object_pool = game_object_pool
        self._lanes = self._get_initial_lanes()

    def _get_initial_lanes(self) -> dict:
        return {
            0: Lane(
                position=Vector2(0, 168),
                capacity=1,
                index=0,
                game_object_type=GameObjectType.SPIDER,
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
            ),
        }

    def process(self, delta_time: float) -> None:
        for lane_index in self._lanes:
            lane = self._lanes[lane_index]
            lane.draw()
            # Always checking if can spawn for now
            if lane.can_spawn():
                game_object = self._game_object_pool.attempt_spawn(
                    type=lane.game_object_type
                )
                game_object.position = lane.position
                game_object.spawn_lane_index = lane.index
                lane.capacity -= 1

        # Movement
        dead_game_object_pool = []
        for live_game_object in self._game_object_pool.live_pool:
            live_game_object.move_object(delta_time=delta_time)
            if not live_game_object.active:
                dead_game_object_pool.append(live_game_object)

        # Clean up
        for dead_game_object in dead_game_object_pool:
            lane_to_cleanup = self._lanes[dead_game_object.spawn_lane_index]
            lane_to_cleanup.capacity += 1
            self._game_object_pool.remove_object(game_object=dead_game_object)
