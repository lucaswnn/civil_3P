from __future__ import annotations

from pathlib import Path
from typing import Any
from dataclasses import dataclass

import os

from civil_3P.standard.file_representation import FileRepresentation as fr
from civil_3P.visualization.config import SceneViewerConfig


@dataclass(frozen=True, slots=True)
class UserPreferences:
    plugins_base_path: Path
    scene_viewer_config: SceneViewerConfig

    @classmethod
    def from_snapshot(
        cls,
        snapshot: dict[str, Any],
    ) -> UserPreferences:
        plugins_base_path = Path(
            snapshot.get(fr.PLUGINS_BASE_PATH)
        )
        scene_viewer_config_data = snapshot.get(
            fr.SCENE_VIEWER_CONFIG
        )
        scene_viewer_config = SceneViewerConfig.from_dict(
            scene_viewer_config_data
        )

        return cls(
            plugins_base_path=plugins_base_path,
            scene_viewer_config=scene_viewer_config
        )


class PreferencesService:
    _instance: PreferencesService | None = None

    def __new__(cls) -> PreferencesService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._preferences = UserPreferences(
                plugins_base_path=Path(
                    PreferencesService.default_plugins_path()
                ),
                scene_viewer_config=SceneViewerConfig()
            )

        return cls._instance

    _preferences: UserPreferences

    @staticmethod
    def default_plugins_path() -> Path:
        app_data = os.environ.get("APPDATA")
        base = Path(app_data) if app_data else Path.home() / \
            "AppData" / "Roaming"

        return base / "civil_3P" / "plugins"

    def get_plugins_base_path(self) -> Path:
        return self._preferences.plugins_base_path

    def set_plugins_base_path(self, path: str | Path) -> None:
        normalized = Path(path).expanduser().resolve()

        if not normalized.is_dir():
            raise NotADirectoryError(
                f"Plugin path is not a directory: {path}"
            )

        self._preferences = UserPreferences(
            plugins_base_path=normalized,
            scene_viewer_config=self._preferences.scene_viewer_config
        )

    def get_scene_viewer_config(self) -> SceneViewerConfig:
        return self._preferences.scene_viewer_config

    def set_scene_viewer_config(self, config: SceneViewerConfig) -> SceneViewerConfig:
        self._preferences = UserPreferences(
            plugins_base_path=self._preferences.plugins_base_path,
            scene_viewer_config=config
        )

        return config

    def snapshot(self) -> dict[str, Any]:
        return {
            fr.PLUGINS_BASE_PATH: str(self._preferences.plugins_base_path),
            fr.SCENE_VIEWER_CONFIG: self._preferences.scene_viewer_config.to_dict(),
        }

    def reset(self) -> None:
        self._preferences = UserPreferences(
            plugins_base_path=Path(PreferencesService.default_plugins_path()),
            scene_viewer_config=SceneViewerConfig()
        )
