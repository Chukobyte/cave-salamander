from src.util.util import Timer_delta


class PlayerStats:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.goals = 5
            cls.lives = 3
            cls.score = 0
            cls.dying_timer = Timer_delta(max_time_in_seconds=0.5)
            cls.dying = False
        return cls._instance

    def reset(self):
        self.goals = 5
        self.lives = 3
        self.score = 0
        self.dying_timer.reset_timer()
