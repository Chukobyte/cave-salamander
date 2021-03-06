from seika.color import Color
from seika.node import TextLabel
from seika.math import Vector2, Rect2
from seika.renderer import Renderer

from src.stats import PlayerStats
from src.util.util import Timer


GUI_Z_INDEX = 2


class TopGUI:
    def __init__(self, score_label: TextLabel):
        self.score_label = score_label

    def update(self, player_stats: PlayerStats) -> None:
        self.score_label.text = f"{player_stats.score}"

    # a more direct update
    def update_text(self, text) -> None:
        self.score_label.text = text


class BottomGUI:
    RECT_WIDTH = 800
    RECT_HEIGHT = 60

    def __init__(self, time_label: TextLabel):
        self.position = Vector2(0, 400)
        self.time_label = time_label
        self.time = 120000
        self.timer = Timer(time_in_millis=self.time)
        self.lives_position = self.position + Vector2(60, 10)
        self.lives_size = Vector2(16, 16)
        self.lives_size_scaled = self.lives_size * Vector2(2, 2)

    def update(self, player_stats: PlayerStats) -> None:
        # BACKGROUND
        # Renderer.draw_texture(
        #     texture_path="assets/images/white_square.png",
        #     source_rect=Rect2(0, 0, 2, 2),
        #     dest_rect=Rect2(
        #         self.position.x, self.position.y, self.RECT_WIDTH, self.RECT_HEIGHT
        #     ),
        #     z_index=GUI_Z_INDEX,
        #     color=Color(0.2, 0.2, 0.2),
        # )

        # if there is time left in timer and player is not dying (currently hit), then update timer
        if self.timer.time > 0 and not player_stats.dying:
            self.timer.tick()
        self.time_label.text = f"Time: {self.timer.time / 1000}"

        # LIVES
        for life_count in range(player_stats.lives):
            Renderer.draw_texture(
                texture_path="assets/images/health.png",
                source_rect=Rect2(0, 0, self.lives_size.x, self.lives_size.y),
                dest_rect=Rect2(
                    self.lives_position.x + (life_count * 32),
                    self.lives_position.y,
                    self.lives_size_scaled.x,
                    self.lives_size_scaled.y,
                ),
                z_index=GUI_Z_INDEX + 1,
            )


class GUI:
    def __init__(
        self,
        score_label: TextLabel = None,
        time_label: TextLabel = None,
        player_stats: PlayerStats = None,
    ):
        self.top_gui = TopGUI(score_label=score_label)
        self.bottom_gui = BottomGUI(time_label=time_label)
        self.player_stats = player_stats

    def update(self) -> None:
        self.top_gui.update(player_stats=self.player_stats)
        self.bottom_gui.update(player_stats=self.player_stats)
