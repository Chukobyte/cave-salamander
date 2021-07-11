class PlayerStats:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.lives = 3
            cls.score = 0
        return cls._instance

    def reset(self):
        self.lives = 3
        self.score = 0
