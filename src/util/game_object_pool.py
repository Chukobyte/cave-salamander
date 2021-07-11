from seika.math import Vector2
from seika.node import Node2D
from src.game_object import GameObjectType, GameObject

NEGATIVE_SPACE_POSITION = Vector2(-1000, -1000)
MAX_LIVE_OBJECTS = 20

class SpawnLaneManger(Node2D):
    '''
    position: represents the spawner's sprite's position of where the game object will spawn
    capactiy: how many game objects can be in this lane
    '''
    class SpawnLane:
        def __init__(self, lane_index: int = 0, position: Vector2 = Vector2(0,0),  capacity: int=1):
            self.position = position
            self.capacity=capacity
            self.spawns = 0
            #self.spawns = []
            self.direction = 1 if self.position.x <= 0 else -1 #determines the direction of the spawns; 1 means LTR; -1 means RTL
            self.lane_index = lane_index

        def add_spawn(self, gameObject):
            #if len(self.spawns)< self.capacity:
            if self.spawns< self.capacity:
                gameObject.position = self.position
                v_x = abs(gameObject.velocity.x) * self.direction
                v_y = abs(gameObject.velocity.y) * self.direction

                gameObject.velocity = Vector2(v_x,v_y)
                gameObject.spawn_lane_index = self.lane_index
                self.spawns+=1
                #self.spawns.append(gameObject)
            else:
                print(f">>Capacity meet {self.capacity} at position {self.position}")

        #def remove_spawn(self, gameObject):
        def remove_spawn(self):
            if self.spawns > 0:
                self.spawns-= 1
            else:
                self.spawns=0
            # if gameObject in self.spawns:
            #     self.spawns.remove(gameObject)


    def __init__(self):
        # Have to manually add them, since I can't get SpawnObjects' child nodes
        self.spawn_lanes = []
        self.spawn_lanes.append(self.SpawnLane(lane_index=0,position = self.get_node(name="Spawn_lane_01").get_position(), capacity=1))
        self.spawn_lanes.append(self.SpawnLane(lane_index=1,position = self.get_node(name="Spawn_lane_02").get_position(), capacity=1))
        self.spawn_lanes.append(self.SpawnLane(lane_index=2,position = self.get_node(name="Spawn_lane_03").get_position(), capacity=0))
        self.spawn_lanes.append(self.SpawnLane(lane_index=3,position = self.get_node(name="Spawn_lane_04").get_position(), capacity=0))
        self.spawn_lanes.append(self.SpawnLane(lane_index=4,position = self.get_node(name="Spawn_lane_05").get_position(), capacity=0))
        self.spawn_lanes.append(self.SpawnLane(lane_index=5,position = self.get_node(name="Spawn_lane_06").get_position(), capacity=0))

    def is_spawn_lane_available(self, lane) ->bool:
        if lane.capacity >0:
            #if len(lane.spawns)<lane.capacity:
            if lane.spawns<lane.capacity:
                return True
        return False

    def get_first_available_lane(self) -> SpawnLane:
        for lane in self.spawn_lanes:
            if self.is_spawn_lane_available(lane=lane):
                return lane
        return None

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
        self._spawn_manager = SpawnLaneManger()

    def spawn(self, type:str):
        # this needs to be created since we are removing objects from the _object_pools list
        object_pool_list = [obj for obj in self._object_pools[type]]

        for gameobject in object_pool_list:
            available_lane = self._spawn_manager.get_first_available_lane()
            if available_lane is not None:
                new_gameobject = self.create(type=type)
                new_gameobject.update_properties_based_on_type()
                available_lane.add_spawn(gameObject=new_gameobject)

    def create(self, type: str) -> GameObject:
        self.live_objects += 1
        game_object = self._object_pools[type].pop()
        game_object.type = type
        game_object.active = True
        game_object.update_properties_based_on_type()
        self._live_pool.append(game_object)
        return game_object

    def remove(self, game_object: GameObject) -> None:
        if game_object.spawn_lane_index >0 and game_object.spawn_lane_index < len(self._spawn_manager.spawn_lanes):
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
