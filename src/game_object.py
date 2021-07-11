from seika.node import Sprite
from seika.math import Vector2
from src.util.util import GameScreen


class GameObjectType:
    SNAKE = "Snake"


class GameObjectProperties:
    # The properties are based on the game object's sprite properties (which we can not directly get)
    def __init__(self, w=0, h=0, x_s=1, y_s=1, t=2):
        self.width = w
        self.height = h
        self.x_scale = x_s
        self.y_scale = y_s
        self.walk_timer = t  # in seconds; time it takes to make one step

    def __str__(self):
        return f"\nWidth: {self.width} Height: {self.height}\nX Scale: {self.x_scale} Y Scale: {self.y_scale}\nWalking Timer: {self.walk_timer}\n"

class DefaultGameObjectProperties:
    default_properties = {GameObjectType.SNAKE: GameObjectProperties(w=2, h=2, x_s=8, y_s=8, t=0.5)}


class GameObject(Sprite):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.velocity = Vector2()
        self.active = False
        self.type = None
        self.properties = GameObjectProperties()
        self.timer = self.properties.walk_timer

    def update_properties(self, new_property: GameObjectProperties):
        self.properties = new_property
        self.timer = self.properties.walk_timer

    def update_properties_based_on_type(self):
        if self.type in DefaultGameObjectProperties.default_properties:
            self.properties = DefaultGameObjectProperties.default_properties[self.type]
            self.timer = self.properties.walk_timer

    def move_object(self, deletatime) -> None:
        if self.timer > 0:
            self.timer = self.timer - deletatime
        else:
            self.timer = self.properties.walk_timer
            curr_x = self.get_position().x
            curr_y = self.get_position().y

            velocity_x = self.velocity.x
            velocity_y = self.velocity.y

            width = self.properties.width * self.properties.x_scale
            height = self.properties.height * self.properties.y_scale

            new_x = curr_x + velocity_x
            new_y = curr_y + velocity_y

            if (
                new_x > 0
                and new_x + width < GameScreen().getScreenScaled().x
                and new_y >= 0
                and new_y + height < GameScreen().getScreenScaled().y
            ):
                self.set_position(Vector2(new_x, new_y))
