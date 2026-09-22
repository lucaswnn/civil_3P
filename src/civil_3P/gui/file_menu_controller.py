from __future__ import annotations

import traceback
from pathlib import Path

from civil_3P.application.file_loader_service import FileLoaderService
from civil_3P.application.importer_service import ImporterService
from civil_3P.application.model_service import ModelService
from civil_3P.application.preferences_service import PreferencesService
from civil_3P.application.task_service import TaskService
from civil_3P.gui.event_response import EventResponse, EventStatus
from civil_3P.standard.importer_profiles import ImporterProfiles


class FileMenuController:
    def __init__(
        self,
        importer_service: ImporterService,
        task_service: TaskService,
        file_loader_service: FileLoaderService,
        model_service: ModelService,
        preferences_service: PreferencesService,
        listeners=None,
    ) -> None:
        self._importer_service = importer_service
        self._task_service = task_service
        self._file_loader_service = file_loader_service
        self._model_service = model_service
        self._preferences_service = preferences_service
        self._listeners = listeners or []

    def _response(
        self,
        status: EventStatus,
        message: str,
        exc: Exception | None = None,
    ) -> EventResponse:
        return EventResponse(
            status,
            message,
            traceback.format_exc() if exc else None,
        )

    def import_model(
        self,
        profile: ImporterProfiles,
        directory: str | Path,
    ) -> EventResponse:
        try:
            model = self._importer_service.import_model(
                profile,
                directory,
            )
            self._model_service.set_model(model)
            self._task_service.load_plugins_from(
                self._preferences_service.get_plugins_base_path()
            )
            return self._response(
                EventStatus.SUCCESS,
                "Model imported successfully.",
            )
        except Exception as exc:
            return self._response(EventStatus.FAILURE, str(exc), exc)

    def load_model_file(self, path: str | Path) -> EventResponse:
        try:
            self._file_loader_service.load_and_apply(path)
            return self._response(
                EventStatus.SUCCESS,
                "Model loaded successfully.",
            )
        except Exception as exc:
            return self._response(EventStatus.FAILURE, str(exc), exc)

    def save_model(self, path: str | Path) -> EventResponse:
        try:
            self._file_loader_service.save(path)
            return self._response(
                EventStatus.SUCCESS,
                "Model saved successfully.",
            )
        except Exception as exc:
            return self._response(EventStatus.FAILURE, str(exc), exc)

    def set_plugins_base_path(self, path: str | Path) -> EventResponse:
        try:
            self._preferences_service.set_plugins_base_path(path)
            return self._response(
                EventStatus.SUCCESS,
                "Plugins base path set successfully.",
            )
        except Exception as exc:
            return self._response(EventStatus.FAILURE, str(exc), exc)

    def add_plugins(self, files: list[str] | list[Path]) -> EventResponse:
        try:
            loaded = self._task_service.add_plugins_from(
                files, self._preferences_service.get_plugins_base_path()
            )
            return self._response(
                EventStatus.SUCCESS,
                f"Loaded {len(loaded)} plugins.",
            )
        except Exception as exc:
            return self._response(EventStatus.FAILURE, str(exc), exc)