from seika.node import TextLabel
from seika.math import Vector2, Rect2
from seika.renderer import Renderer

from src.stats import PlayerStats
from src.util.util import Timer


class BottomGUI:
    def __init__(self, time_label: TextLabel):
        self.time_label = time_label
        self.timer = Timer(time_in_millis=120000)
        self.time = 120000
        self.lives_position = Vector2(500, 550)
        self.lives_size = Vector2(16, 16)
        self.lives_size_scaled = self.lives_size * Vector2(2, 2)

    def update(self, player_stats: PlayerStats) -> None:
        # TIME
        self.timer.tick()
        self.time_label.text = f"Time: {self.timer.time / 1000}"

        # LIVES
        for life_count in range(player_stats.lives):
            Renderer.draw_texture(
                texture_path="assets/images/frog/frog.png",
                source_rect=Rect2(0, 0, self.lives_size.x, self.lives_size.y),
                dest_rect=Rect2(
                    self.lives_position.x + (life_count * 32),
                    self.lives_position.y,
                    self.lives_size_scaled.x,
                    self.lives_size_scaled.y,
                ),
            )
