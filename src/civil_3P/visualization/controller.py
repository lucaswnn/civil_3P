from __future__ import annotations

from typing import Any

from civil_3P.visualization.scene import VisualizationService


class VisualizationController:
    def __init__(self, service: VisualizationService | None = None) -> None:
        self._service = service or VisualizationService()

    def build_scene(self, model: Any) -> dict[str, list[dict[str, Any]]]:
        return self._service.build_scene(model)

    def create_viewer(self, scene: dict[str, dict[str, dict[str, Any]]]) -> Any:
        from civil_3P.visualization.scene_viewer import PyVistaViewer

        return PyVistaViewer(scene)
