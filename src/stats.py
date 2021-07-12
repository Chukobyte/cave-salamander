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
            cls.walking_timer = Timer_delta(max_time_in_seconds=0.13)
            cls.dying = False
            cls.can_walk = False
            cls.end_time = 120.0
        return cls._instance

    def reset(self):
        self.goals = 5
        self.lives = 3
        self.score = 0
        self.dying_timer.reset_timer()
        self.walking_timer.reset_timer()
        self.can_walk = False

    def check_can_walk(self, delta_time):
        if self.can_walk:
            return True

        if self.walking_timer.tick_n_check(delta_time=delta_time):
            self.can_walk = True
            return True
        return False
