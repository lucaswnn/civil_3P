from __future__ import annotations

import os
from pathlib import Path

from civil_3P.visualization.config import SceneViewerConfig


def default_plugins_path() -> Path:
    app_data = os.environ.get("APPDATA")
    base = Path(app_data) if app_data else Path.home() / "AppData" / "Roaming"
    return base / "civil_3P" / "plugins"


class UserPreferencesService:
    def __init__(
        self,
        plugins_base_path: str | Path | None = None,
        scene_viewer_config: SceneViewerConfig | None = None,
    ) -> None:
        self._plugins_base_path = Path(
            plugins_base_path or default_plugins_path())
        self.scene_viewer_config = scene_viewer_config or SceneViewerConfig()

    @property
    def plugins_base_path(self) -> Path:
        return self._plugins_base_path

    def set_plugins_base_path(self, path: str | Path) -> Path:
        normalized = Path(path).expanduser().resolve()
        if not normalized.is_dir():
            raise NotADirectoryError(f"Plugin path is not a directory: {path}")
        self._plugins_base_path = normalized
        return normalized

    def snapshot(self) -> dict[str, object]:
        return {
            "plugins_base_path": str(self._plugins_base_path),
            "scene_viewer_config": self.scene_viewer_config.to_dict(),
        }

    def restore(self, values: dict[str, object]) -> None:
        plugin_path = values.get("plugins_base_path")
        if isinstance(plugin_path, str):
            self._plugins_base_path = Path(plugin_path)

        config = values.get("scene_viewer_config")
        if isinstance(config, dict):
            restored = SceneViewerConfig.from_dict(config)
            for name, value in restored.to_dict().items():
                setattr(self.scene_viewer_config, name, value)
