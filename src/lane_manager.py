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


class LaneManager:
    def __init__(self, game_object_pool: GameObjectPool):
        self._game_object_pool = game_object_pool
        self._lanes = self._get_initial_lanes()

    def _get_initial_lanes(self) -> list:
        lanes = []
        lanes.append(
            Lane(
                position=Vector2(0, 168),
                capacity=2,
                index=0,
                game_object_type=GameObjectType.SPIDER,
            )
        )
        return lanes

    def process(self) -> None:
        self._game_object_pool.attempt_spawn(type=GameObjectType.SPIDER)
