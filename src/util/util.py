from seika.math import Vector2

TICK_RATE = 10


class Timer:
    def __init__(self, time_in_millis: int):
        self.time = time_in_millis

    def tick(self) -> None:
        self.time -= TICK_RATE


# Uses delta time
class Timer_delta:
    def __init__(self, max_time_in_seconds: float = 2):
        self.MAX_TIME = max_time_in_seconds
        self.time = self.MAX_TIME

    def reset_timer(self):
        self.time = self.MAX_TIME

    # returns True if timer is done
    def tick_n_check(self, delta_time):
        self.time -= delta_time

        if self.time <= 0:
            self.reset_timer()
            return True
        return False


# For the playable screen only (not menus)
class GameScreen:
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
