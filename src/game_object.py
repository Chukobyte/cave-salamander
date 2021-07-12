from seika.node import Sprite
from seika.math import Vector2
from src.util.util import GameScreen
from seika.node import AnimatedSprite


class GameObjectType:
    SMALL_ROCK = "Small Rock"
    BIG_ROCK = "Big Rock"
    SNAKE = "Snake"
    SPIDER = "Spider"
    GOAL = "Goal"


class GameObjectProperties:
    # The properties are based on the game object's sprite properties (which we can not directly get)
    def __init__(self, w=0, h=0, s=Vector2(1, 1), t=2.0, v=Vector2(-8, 0)):
        self.width = w
        self.height = h
        self.scale = s
        self.walk_timer = t  # in seconds; time it takes to make one step
        self.velocity = v

    def __str__(self):
        return f"\nWidth: {self.width} Height: {self.height}\nX Scale: {self.scale.x} Y Scale: {self.scale.y}\nWalking Timer: {self.walk_timer}\n"


class DefaultGameObjectProperties:
    default_properties = {
        GameObjectType.SMALL_ROCK: GameObjectProperties(
            w=16, h=16, s=Vector2(1, 1), t=0.1, v=Vector2(-16, 0)
        ),
        GameObjectType.BIG_ROCK: GameObjectProperties(
            w=48, h=16, s=Vector2(1, 1), t=0.3, v=Vector2(-16, 0)
        ),
        GameObjectType.SNAKE: GameObjectProperties(
            w=2, h=2, s=Vector2(8, 8), t=0.02, v=Vector2(-8, 0)
        ),
        GameObjectType.SPIDER: GameObjectProperties(
            w=2, h=2, s=Vector2(1, 1), t=0.01, v=Vector2(8, 0)
        ),
        GameObjectType.GOAL: GameObjectProperties(
            w=14, h=14, s=Vector2(1, 1), t=0.5, v=Vector2(0, 0)
        ),
    }


class GameObject(AnimatedSprite):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.properties = GameObjectProperties()
        self.velocity = self.properties.velocity
        self.active = False
        self.type = None
        self.timer = self.properties.walk_timer
        self.spawn_lane_index = -1
        self.collider = None
        self.last_moved_velocity = Vector2(0, 0)

    def update_properties(self, new_property: GameObjectProperties):
        self.properties = new_property
        self.timer = self.properties.walk_timer
        self.velocity = self.properties.velocity

    def update_properties_based_on_type(self):
        if self.type in DefaultGameObjectProperties.default_properties:
            self.properties = DefaultGameObjectProperties.default_properties[self.type]
            self.timer = self.properties.walk_timer
            self.velocity = self.properties.velocity

    def move_object(self, delta_time: float) -> bool:
        if self.timer > 0:
            self.timer -= delta_time
            return False
        else:
            self.timer = self.properties.walk_timer
            curr_x = self.get_position().x
            curr_y = self.get_position().y

            velocity_x = self.velocity.x
            velocity_y = self.velocity.y

            width = self.properties.width * self.properties.scale.x
            height = self.properties.height * self.properties.scale.y

            new_pos = Vector2(curr_x + velocity_x, curr_y + velocity_y)

            # modified so gameobjects are off screen
            if (
                new_pos.x > 0 - (width * 2)
                and new_pos.x < GameScreen().getScreenScaled().x + width
                and new_pos.y >= 0
                and new_pos.y + height < GameScreen().getScreenScaled().y
            ):
                self.set_position(new_pos)
                self.last_moved_velocity = Vector2(velocity_x, velocity_y)
            else:
                self.active = False
            return True

    # Mainly for the goal game object types
    def move_off_screen(self) -> None:
        self.position = Vector2(-32, 0)
