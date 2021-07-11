from seika.math import Vector2

from src.game_object import GameObjectType
from src.util.new_game_object_pool import GameObjectPool


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
        }

    def process(self, delta_time: float) -> None:
        for lane_index in self._lanes:
            lane = self._lanes[lane_index]
            # Always checking if can spawn for now
            if lane.can_spawn():
                game_object = self._game_object_pool.attempt_spawn(
                    type=GameObjectType.SPIDER
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
