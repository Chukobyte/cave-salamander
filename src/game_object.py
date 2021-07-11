from seika.node import Sprite
from seika.math import Vector2
from src.util.util import GameScreen

class GameObjectType:
    SNAKE = "Snake"

class GameObjectProperties:
    def __init__(self, w=0 ,h=0, x_s=1, y_s=1):
        self.width =w
        self.height=h
        self.x_scale = x_s
        self.y_scale = y_s
    def __str__(self):
        return f"Width: {self.width} Height: {self.height} X Scale: {self.x_scale} Y Scale: {self.y_scale}"

    # @staticmethod
    # def get_default_properties(self):
    #     return GameObjectProperties(w=2,h=2,s_x=8,s_y=8)

class DefaultGameObjectProperties:
    default_properties = {
        "Snake":GameObjectProperties(w=2,h=2,x_s=8,y_s=8)
    }

class GameObject(Sprite):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.velocity = Vector2()
        self.active = False
        self.type = None
        self.properties = GameObjectProperties()

    def update_properties(self, new_property: GameObjectProperties):
        self.properties = new_property

    def update_properties_based_on_type(self):
        if self.type in DefaultGameObjectProperties.default_properties:
            self.properties = DefaultGameObjectProperties.default_properties[self.type]

    def move_object(self) -> None:
        curr_x = self.get_position().x
        curr_y = self.get_position().y

        velocity_x = self.velocity.x
        velocity_y = self.velocity.y

        width = self.properties.width * self.properties.x_scale
        height = self.properties.height * self.properties.y_scale

        new_x = curr_x + velocity_x
        new_y = curr_y + velocity_y


        if (new_x > 0 and new_x + width < GameScreen().getScreenScaled().x and
            new_y >= 0 and new_y + height < GameScreen().getScreenScaled().y):
            self.set_position(Vector2(new_x,new_y))



