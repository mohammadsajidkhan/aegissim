from __future__ import annotations

from aegissim.config import AppConfig


class PerformanceManager:
    def __init__(self, app, config: AppConfig):
        self.app = app
        self.config = config

    def apply(self) -> None:
        g = self.config.graphics
        self.app.setBackgroundColor(*g.background_color)
        if g.show_fps:
            self.app.setFrameRateMeter(True)
        quality = g.quality.lower()
        if quality == "low":
            self.app.render.setAntialias(False)
        elif quality == "high":
            self.app.render.setAntialias(True)
        else:
            self.app.render.setAntialias(False)

    def update(self) -> None:
        # Extend with frame-time telemetry or PStats hooks.
        return None
