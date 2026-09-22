from __future__ import annotations

from collections.abc import Callable

from civil_3P.visualization.scene import Scene


class SceneWidgetListener:
    def __init__(self) -> None:
        self._model_changed: list[Callable[[Scene], None]] = []
        self._result_changed: list[Callable[[Scene], None]] = []

    def on_model_changed(self, callback: Callable[[Scene], None]) -> None:
        self._model_changed.append(callback)

    def on_result_changed(self, callback: Callable[[Scene], None]) -> None:
        self._result_changed.append(callback)

    def notify_model_changed(self, scene: Scene) -> None:
        for callback in tuple(self._model_changed):
            callback(scene)

    def notify_result_changed(self, scene: Scene) -> None:
        for callback in tuple(self._result_changed):
            callback(scene)