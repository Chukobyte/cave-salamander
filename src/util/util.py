from seika.math import Vector2

TICK_RATE = 10


class Timer:
    def __init__(self, time_in_millis: int):
        self.time = time_in_millis

    def tick(self) -> None:
        self.time -= TICK_RATE


# For the playable screen only (not menus)
class GameScreen:
    SCREEN_HEIGHT_SCALED = 0
    SCREEN_WIDTH_SCALED = 0
    _instance = None

    """
    The top/bottom ui buffer is for areas that cannot be accessable
    """

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.SCREEN_WIDTH = 800
            cls.SCREEN_HEIGHT = 450 - 16
            cls.GRID_X, cls.GRID_Y = 16, 16
            cls.ZOOM_X, cls.ZOOM_Y = 2, 2
            cls.TOP_UI_BUFFER = (
                0  # pixels in y axis on TOP of screen meant for GUI and not users
            )
            cls.BOTTOM_UI_BUFFER = (
                0  # pixels in y axis on BOTTOM of screen meant for GUI and not users
            )
            cls.SCREEN_WIDTH_SCALED = int(cls.SCREEN_WIDTH / cls.ZOOM_X)
            cls.SCREEN_HEIGHT_SCALED = int(
                (cls.SCREEN_HEIGHT / cls.ZOOM_Y) - (cls.BOTTOM_UI_BUFFER / 3)
            )
        return cls._instance

    def setTopBuffer(cls, buffer: int):
        cls.TOP_UI_BUFFER = buffer
        cls.updateScreenScaled()

    def setBottomBuffer(cls, buffer: int):
        cls.BOTTOM_UI_BUFFER = buffer
        cls.updateScreenScaled()

    def updateScreenScaled(cls):
        cls.SCREEN_WIDTH_SCALED = int(cls.SCREEN_WIDTH / cls.ZOOM_X)
        cls.SCREEN_HEIGHT_SCALED = int(
            (cls.SCREEN_HEIGHT / cls.ZOOM_Y) - (cls.BOTTOM_UI_BUFFER / 3)
        )

    def getScreen(cls):
        # TODO: Is there a better way to check for Project's resolution/screensize?
        # A project's resolution is also it's size?
        return Vector2(cls.SCREEN_WIDTH, cls.SCREEN_HEIGHT)

    def getScreenScaled(cls):
        return Vector2(cls.SCREEN_WIDTH_SCALED, cls.SCREEN_HEIGHT_SCALED)

    def getGridSize(cls):
        return Vector2(cls.GRID_X, cls.GRID_Y)  # the sprite's size

    def getZoom(cls):
        return Vector2(cls.ZOOM_X, cls.ZOOM_Y)

    @classmethod
    def is_position_within_screen(cls, position: Vector2) -> bool:
        return (
            position.x >= 0
            and position.x < cls.SCREEN_WIDTH_SCALED
            and position.y >= 0
            and position.y < cls.SCREEN_HEIGHT_SCALED
        )
