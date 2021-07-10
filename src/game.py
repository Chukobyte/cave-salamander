from seika.node import Node2D
from seika.input import Input
from seika.engine import Engine
from seika.math import Vector2
from seika.camera import Camera
from seika.physics import Collision

class Game(Node2D):
    def _start(self) -> None:
        self.frogger = self.get_node(name="Frog")
        self.frogger_collider = self.get_node(name="FrogCollider")
        self.frog_initial_position = self.frogger.position
        self.grid_size = Vector2(16, 16)
        Camera.set_zoom(zoom=Vector2(4, 4))

    def _physics_process(self, delta_time: float) -> None:
        if Input.is_action_just_pressed(action_name="ui_quit"):
            Engine.exit()

        self.handle_game_input()

        self.process_collisions()

    def handle_game_input(self) -> None:
        if Input.is_action_just_pressed(action_name="move_left"):
            self.frogger.add_to_position(Vector2(-self.grid_size.x, 0))
        elif Input.is_action_just_pressed(action_name="move_right"):
            self.frogger.add_to_position(Vector2(self.grid_size.x, 0))
        if Input.is_action_just_pressed(action_name="move_up"):
            self.frogger.add_to_position(Vector2(0, -self.grid_size.y))
        elif Input.is_action_just_pressed(action_name="move_down"):
            self.frogger.add_to_position(Vector2(0, self.grid_size.y))

    def process_collisions(self) -> None:
        collided_nodes = Collision.get_collided_nodes(node=self.frogger_collider)
        for collided_node in collided_nodes:
            # print(f"collided with node with entity id = {collided_node.entity_id}")
            self.frogger.position = self.frog_initial_position
            break
