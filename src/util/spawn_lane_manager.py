# from seika.math import Vector2
#
#
# class SpawnLaneManger:
#     """
#     position: represents the spawner's sprite's position of where the game object will spawn
#     capactiy: how many game objects can be in this lane
#     """
#
#     class SpawnLane:
#         def __init__(
#             self,
#             lane_index: int = 0,
#             position: Vector2 = Vector2(0, 0),
#             capacity: int = 1,
#         ):
#             self.position = position
#             self.capacity = capacity
#             self.spawns = 0
#             # self.spawns = []
#             self.direction = (
#                 1 if self.position.x <= 0 else -1
#             )  # determines the direction of the spawns; 1 means LTR; -1 means RTL
#             self.lane_index = lane_index
#
#         def add_spawn(self, gameObject):
#             # if len(self.spawns)< self.capacity:
#             if self.spawns < self.capacity:
#                 gameObject.position = self.position
#                 v_x = abs(gameObject.velocity.x) * self.direction
#                 v_y = abs(gameObject.velocity.y) * self.direction
#
#                 gameObject.velocity = Vector2(v_x, v_y)
#                 gameObject.spawn_lane_index = self.lane_index
#                 self.spawns += 1
#                 print(self.lane_index)
#                 # self.spawns.append(gameObject)
#             else:
#                 print(f">>Capacity meet {self.capacity} at position {self.position}")
#
#         # def remove_spawn(self, gameObject):
#         def remove_spawn(self):
#             print(f"Removing spawn from index: {self.lane_index}")
#             if self.spawns > 0:
#                 self.spawns -= 1
#             else:
#                 self.spawns = 0
#             # if gameObject in self.spawns:
#             #     self.spawns.remove(gameObject)
#
#     def __init__(self, gameNode):
#         self.gameNode = gameNode
#         # Have to manually add them, since I can't get SpawnObjects' child nodes
#         self.spawn_lanes = []
#         self.spawn_lanes.append(
#             self.SpawnLane(
#                 lane_index=0,
#                 position=self.gameNode.get_node(name="Spawn_lane_01").get_position(),
#                 capacity=1,
#             )
#         )
#         self.spawn_lanes.append(
#             self.SpawnLane(
#                 lane_index=1,
#                 position=self.gameNode.get_node(name="Spawn_lane_02").get_position(),
#                 capacity=1,
#             )
#         )
#         self.spawn_lanes.append(
#             self.SpawnLane(
#                 lane_index=2,
#                 position=self.gameNode.get_node(name="Spawn_lane_03").get_position(),
#                 capacity=0,
#             )
#         )
#         self.spawn_lanes.append(
#             self.SpawnLane(
#                 lane_index=3,
#                 position=self.gameNode.get_node(name="Spawn_lane_04").get_position(),
#                 capacity=0,
#             )
#         )
#         self.spawn_lanes.append(
#             self.SpawnLane(
#                 lane_index=4,
#                 position=self.gameNode.get_node(name="Spawn_lane_05").get_position(),
#                 capacity=0,
#             )
#         )
#         self.spawn_lanes.append(
#             self.SpawnLane(
#                 lane_index=5,
#                 position=self.gameNode.get_node(name="Spawn_lane_06").get_position(),
#                 capacity=0,
#             )
#         )
#
#     def is_spawn_lane_available(self, lane) -> bool:
#         if lane.capacity > 0:
#             # if len(lane.spawns)<lane.capacity:
#             if lane.spawns < lane.capacity:
#                 return True
#         return False
#
#     def get_first_available_lane(self) -> SpawnLane:
#         for lane in self.spawn_lanes:
#             if self.is_spawn_lane_available(lane=lane):
#                 return lane
#         return None
