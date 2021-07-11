from seika.math import Vector2
from seika.node import Node2D
from src.game_object import GameObjectType, GameObject
from src.util.spawn_lane_manager import SpawnLaneManger

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
        self._spawn_manager = SpawnLaneManger(gameNode=game)

    def spawn(self, type: str):
        # this needs to be created since we are removing objects from the _object_pools list
        object_pool_list = [obj for obj in self._object_pools[type]]
        # if len(object_pool_list)>0:
        #     print(object_pool_list)

        for gameobject in object_pool_list:
            # print(f"Object: {gameobject}")
            available_lane = self._spawn_manager.get_first_available_lane()
            if available_lane is not None:
                new_gameobject = self.create(type=type)
                new_gameobject.update_properties_based_on_type()
                available_lane.add_spawn(gameObject=new_gameobject)
            # print("")

    def create(self, type: str) -> GameObject:
        self.live_objects += 1
        game_object = self._object_pools[type].pop()
        game_object.type = type
        game_object.active = True
        game_object.update_properties_based_on_type()
        self._live_pool.append(game_object)
        return game_object

    def remove(self, game_object: GameObject) -> None:
        print("Removing")
        if game_object.spawn_lane_index > 0 and game_object.spawn_lane_index < len(
            self._spawn_manager.spawn_lanes
        ):
            self._spawn_manager.spawn_lanes[game_object.spawn_lane_index].remove_spawn()

        self.live_objects -= 1
        negative_space_separator = 100 * (MAX_LIVE_OBJECTS - self.live_objects)
        game_object.position = Vector2(
            -500 + -negative_space_separator, -500 + -negative_space_separator
        )
        game_object.active = False
        self._live_pool.remove(game_object)
        self._object_pools[game_object.type].append(game_object)
        print("Live pool:", self._live_pool)
        print("object_pool:", self._object_pools)

    def update_velecoity(self, game_object: GameObject, velocity: Vector2) -> None:
        game_object.velocity = velocity

    def move_gameobjects_in_pool(self, deltatime):
        for gameobject in self._live_pool:
            if gameobject.active:
                gameobject.move_object(deletatime=deltatime)
            else:
                self.remove(game_object=gameobject)
