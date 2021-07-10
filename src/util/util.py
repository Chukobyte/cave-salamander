TICK_RATE = 10


class Timer:
    def __init__(self, time_in_millis: int):
        self.time = time_in_millis

    def tick(self) -> None:
        self.time -= TICK_RATE
