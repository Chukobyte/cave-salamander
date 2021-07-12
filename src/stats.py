from src.util.util import Timer_delta


class PlayerStats:
    _instance = None
    _MAX_GOALS = 5
    _INITIAL_LIVES = 3
    _END_TIME = 120
    MAX_LIVES = 5

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.goals = cls._MAX_GOALS
            cls.lives = cls._INITIAL_LIVES
            cls.score = 0
            cls.dying_timer = Timer_delta(max_time_in_seconds=0.5)
            cls.walking_timer = Timer_delta(max_time_in_seconds=0.13)
            cls.dying = False
            cls.can_walk = False
            cls.end_time = cls._END_TIME
        return cls._instance

    def reset(self):
        self.lives = self._INITIAL_LIVES
        self.score = 0
        self.sub_reset()

    #for when you don't want to reset lives and scores
    def sub_reset(self):
        self.goals = self._MAX_GOALS
        self.dying_timer.reset_timer()
        self.walking_timer.reset_timer()
        self.can_walk = False
        self.dying = False
        self.end_time = self._END_TIME

    def check_can_walk(self, delta_time):
        if self.can_walk:
            return True

        if self.walking_timer.tick_n_check(delta_time=delta_time):
            self.can_walk = True
            return True
        return False
