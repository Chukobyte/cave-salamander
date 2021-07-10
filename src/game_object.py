from seika.node import Sprite
from seika.math import Vector2


class GameObjectType:
    SNAKE = "Snake"


class GameObject(Sprite):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.velocity = Vector2()
        self.active = False
        self.type = None
