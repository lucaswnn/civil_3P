from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from civil_3P.standard.file_representation import FileRepresentation as fr

if TYPE_CHECKING:
    from civil_3P.application.file_service import FileService
    from civil_3P.application.model_service import ModelService
    from civil_3P.application.preferences_service import UserPreferencesService


class FileLoaderService:
    def __init__(
        self,
        file_service: FileService,
        model_service: ModelService,
        preferences_service: UserPreferencesService,
    ):
        self._file_service = file_service
        self._model_service = model_service
        self._preferences_service = preferences_service

    def save(self, path: str | Path) -> None:
        model = self._model_service.get_model()
        preferences_snapshot = self._preferences_service.snapshot()
        self._file_service.save(path, model, preferences_snapshot)

    def load_and_apply(self, path: str | Path) -> None:
        model, preferences = self._file_service.load(path)
        self._model_service.set_model(model)

        plugin_path = preferences.get(fr.PLUGINS_BASE_PATH)
        scene_viewer_config = preferences.get(fr.SCENE_VIEWER_CONFIG)
        self._preferences_service.set_plugins_base_path(plugin_path)
        self._preferences_service.set_scene_viewer_config(scene_viewer_config)
