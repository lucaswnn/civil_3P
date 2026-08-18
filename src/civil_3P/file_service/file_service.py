from __future__ import annotations

import pickle
from pathlib import Path

from civil_3P.application.services import ApplicationContext
from civil_3P.core.model import FEMModel


class FileService:
    FORMAT_VERSION = 1

    def __init__(self, context: ApplicationContext | None = None) -> None:
        self._context = context or ApplicationContext()

    def save(self, path: str | Path) -> None:
        model = self._context.model_service.model
        if model is None:
            raise ValueError("Cannot save without a loaded FEMModel")

        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "format_version": self.FORMAT_VERSION,
            "model": model,
            "preferences": self._context.preferences.snapshot(),
        }
        with file_path.open("wb") as f:
            pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, path: str | Path) -> FEMModel:
        file_path = Path(path)
        with file_path.open("rb") as f:
            loaded_model = pickle.load(f)

        if isinstance(loaded_model, FEMModel):
            self._context.model_service.model = loaded_model
            return loaded_model

        if not isinstance(loaded_model, dict):
            raise TypeError(
                f"File does not contain a supported project: {path}")

        if loaded_model.get("format_version") != self.FORMAT_VERSION:
            raise ValueError(f"Unsupported project format: {path}")

        model = loaded_model.get("model")
        if not isinstance(model, FEMModel):
            raise TypeError(f"File does not contain a FEMModel: {path}")

        preferences = loaded_model.get("preferences")
        if isinstance(preferences, dict):
            self._context.preferences.restore(preferences)

        self._context.model_service.model = model
        return model
