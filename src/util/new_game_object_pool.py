from seika.math import Vector2
from seika.node import Node2D
from src.game_object import GameObjectType, GameObject

NEGATIVE_SPACE_POSITION = Vector2(-1000, -1000)
MAX_LIVE_OBJECTS = 20


class GameObjectPool:
    def __init__(
        self,
        game: Node2D,
        rock_node_names=[],
        snake_node_names=[],
        spider_node_names=[],
    ):
        self._object_pools = {
            GameObjectType.ROCK: [
                game.get_node(name=rock_node_name) for rock_node_name in rock_node_names
            ],
            GameObjectType.SNAKE: [
                game.get_node(name=snake_node_name)
                for snake_node_name in snake_node_names
            ],
            GameObjectType.SPIDER: [
                game.get_node(name=spider_node_name)
                for spider_node_name in spider_node_names
            ],
        }
        self._live_pool = []
        # self._spawn_manager = SpawnLaneManger(gameNode=game)

    def process(self) -> None:
        self.attempt_spawn(type=GameObjectType.SPIDER)

    def attempt_spawn(self, type: str) -> bool:
        if len(self._object_pools[type]) > 0:
            game_object = self._spawn_object(type=type)
            game_object.position = Vector2(100, 100)
            return True
        return False

    def _spawn_object(self, type: str) -> GameObject:
        game_object = self._object_pools[type].pop()
        game_object.type = type
        game_object.active = True
        game_object.update_properties_based_on_type()
        self._live_pool.append(game_object)
        return game_object

    def remove_object(self, game_object: GameObject) -> None:
        negative_space_separator = 100 * (MAX_LIVE_OBJECTS - len(self._live_pool))
        game_object.position = Vector2(
            -500 + -negative_space_separator, -500 + -negative_space_separator
        )
        game_object.active = False
        self._live_pool.remove(game_object)
        self._object_pools[game_object.type].append(game_object)
