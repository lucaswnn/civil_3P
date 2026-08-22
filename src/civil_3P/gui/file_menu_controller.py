from __future__ import annotations

from pathlib import Path
from typing import Any

from civil_3P.application.services import (
    ApplicationContext,
    ImportModelService,
    ModelService,
    VisualizationService,
)
from civil_3P.application.preferences import UserPreferencesService
from civil_3P.core.model import FEMModel
from civil_3P.file_service.file_service import FileService
from civil_3P.standard.importer_profiles import ImporterProfiles


class FileMenuController:
    def __init__(
        self,
        import_model_service: ImportModelService | None = None,
        file_service: FileService | None = None,
        visualization_service: VisualizationService | None = None,
        model_service: ModelService | None = None,
        context: ApplicationContext | None = None,
    ) -> None:
        self._context = context or ApplicationContext()
        self._import_service = import_model_service or ImportModelService()
        self._file_service = file_service or FileService(context=self._context)
        self._visualization_service = visualization_service or VisualizationService()
        self._model_service = model_service or self._context.model_service

    @property
    def current_model(self) -> FEMModel | None:
        return self._model_service.model

    def import_model(
        self,
        profile: ImporterProfiles,
        directory: str | Path,
    ) -> FEMModel:
        model = self._import_service.import_model(profile, directory)
        self._model_service.model = model
        self._context.load_plugins()
        return model

    def load_model_file(self, path: str | Path) -> FEMModel:
        model = self._file_service.load(path)
        self._model_service.model = model
        self._context.load_plugins()
        return model

    def save_model(self, path: str | Path) -> None:
        self._file_service.save(path)

    @property
    def preferences(self) -> UserPreferencesService:
        return self._context.preferences

    def set_plugins_base_path(self, path: str | Path) -> Path:
        return self.preferences.set_plugins_base_path(path)

    def load_plugins(self) -> list[str]:
        return self._context.load_plugins()

    def add_plugins(self, files: list[str] | list[Path]) -> list[str]:
        return self._context.add_plugins(files)

    def build_scene(self, model: FEMModel) -> dict[str, Any]:
        return self._visualization_service.build_scene(model)

