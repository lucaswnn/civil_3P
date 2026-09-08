from __future__ import annotations

from typing import TYPE_CHECKING

import traceback

from civil_3P.application.file_loader_service import FileLoaderService
from civil_3P.application.model_service import ModelService
from civil_3P.application.view_builder_service import ViewBuilderService
from civil_3P.core.model import FEMModel
from civil_3P.application.file_service import FileService
from civil_3P.gui.event_response import EventResponse, EventStatus
from civil_3P.standard.importer_profiles import ImporterProfiles
from civil_3P.visualization.scene import Scene

if TYPE_CHECKING:
    from pathlib import Path

    from civil_3P.application.importer_service import ImporterService
    from civil_3P.application.task_service import TaskService
    from civil_3P.application.preferences_service import UserPreferencesService


class FileMenuController:
    def __init__(
        self,
        importer_service: ImporterService,
        file_loader_service: FileLoaderService,
        task_service: TaskService,
        listeners,
    ) -> None:
        self._task_service = task_service
        self._import_service = import_model_service
        self._file_service = file_service
        self._visualization_service = visualization_service
        self._model_service = model_service
        self._preferences_service = preferences_service

    def import_model(
        self,
        profile: ImporterProfiles,
        directory: str | Path,
    ) -> EventResponse:
        try:
            model = self._import_service.import_model(profile, directory)
            self._model_service.set_model(model)

            self._task_service.load_plugins_from(
                self._preferences_service.plugins_base_path
            )

            return EventResponse(
                status=EventStatus.SUCCESS,
                message="Model imported successfully.",
            )

        except Exception as e:
            return EventResponse(
                status=EventStatus.FAILURE,
                message=str(e),
                detailed_message=traceback.format_exc(),
            )

    def load_model_file(self, path: str | Path) -> EventResponse:
        try:
            model = self._file_service.load(path)
            self._model_service.set_model(model)
            self._task_service.load_plugins_from(
                self._preferences_service.plugins_base_path
            )

            return EventResponse(
                status=EventStatus.SUCCESS,
                message="Model loaded successfully.",
            )

        except Exception as e:
            return EventResponse(
                status=EventStatus.FAILURE,
                message=str(e),
                detailed_message=traceback.format_exc(),
            )

    def save_model(self, path: str | Path) -> EventResponse:
        try:
            self._file_service.save(path)

            return EventResponse(
                status=EventStatus.SUCCESS,
                message="Model saved successfully.",
            )

        except Exception as e:
            return EventResponse(
                status=EventStatus.FAILURE,
                message=str(e),
                detailed_message=traceback.format_exc(),
            )

    def set_plugins_base_path(
        self,
        path: str | Path,
    ) -> EventResponse:
        try:
            self._preferences_service.set_plugins_base_path(path)

            return EventResponse(
                status=EventStatus.SUCCESS,
                message="Plugins base path set successfully.",
            )

        except Exception as e:
            return EventResponse(
                status=EventStatus.FAILURE,
                message=str(e),
                detailed_message=traceback.format_exc(),
            )

    def get_plugins_base_path(self) -> Path:
        return self._preferences_service.get_plugins_base_path()

    def load_plugins(self) -> list[str]:
        return self._preferences_service.load_plugins()

    def add_plugins(
            self,
            files: list[str] | list[Path],
    ) -> EventResponse:
        try:
            loaded = self._preferences_service.add_plugins(files)

            return EventResponse(
                status=EventStatus.SUCCESS,
                message=f"Loaded {len(loaded)} plugins.",
            )

        except Exception as e:
            return EventResponse(
                status=EventStatus.FAILURE,
                message=str(e),
                detailed_message=traceback.format_exc(),
            )

    def build_scene(self, model: FEMModel) -> Scene:
        return self._visualization_service.build_scene(model)
