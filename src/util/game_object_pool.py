from seika.math import Vector2
from seika.node import Node2D

from src.game_object import GameObjectType, GameObject

NEGATIVE_SPACE_POSITION = Vector2(-1000, -1000)
MAX_LIVE_OBJECTS = 20


class GameObjectPool:
    def __init__(self, game: Node2D, snake_node_names=[]):
        self._object_pools = {
            GameObjectType.SNAKE: [
                game.get_node(name=snake_node_name)
                for snake_node_name in snake_node_names
            ],
        }
        self.live_objects = 0
        self._live_pool = []

    def create(self, type: str) -> GameObject:
        self.live_objects += 1
        game_object = self._object_pools[type].pop()
        game_object.type = type
        game_object.active = True
        game_object.update_properties_based_on_type()
        self._live_pool.append(game_object)
        return game_object

    def remove(self, game_object: GameObject) -> None:
        self.live_objects -= 1
        negative_space_separator = 100 * (MAX_LIVE_OBJECTS - self.live_objects)
        game_object.position = Vector2(
            -500 + -negative_space_separator, -500 + -negative_space_separator
        )
        game_object.active = False
        del self._live_pool[game_object]
        self._object_pools[game_object.type].append(game_object)

    def update_velecoity(self, game_object: GameObject, velocity: Vector2) -> None:
        game_object.velocity = velocity

    def move_gameobjects_in_pool(self, deltatime):
        for gameobject in self._live_pool:
            gameobject.move_object(deletatime=deltatime)
