from __future__ import annotations

from pathlib import Path
from typing import Any

import json

from civil_3P.application.preferences_service import UserPreferences
from civil_3P.core.model import Model
from civil_3P.standard.file_representation import FileRepresentation as fr


class FileService:
    FORMAT_VERSION = "0.1.0"

    def save(
        self,
        path: str | Path,
        model: Model,
        preferences_snapshot: dict[str, Any],
    ) -> None:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            fr.FORMAT_VERSION: self.FORMAT_VERSION,
            fr.PREFERENCES: preferences_snapshot,
            fr.MODEL: model.to_dict(),
        }

        with file_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)

    def load(self, path: str | Path) -> tuple[Model, UserPreferences]:
        file_path = Path(path)

        with file_path.open("r", encoding="utf-8") as f:
            loaded_file = json.load(f)

        if not isinstance(loaded_file, dict):
            raise TypeError(
                f"File does not contain a supported project: {path}"
            )

        if loaded_file.get(fr.FORMAT_VERSION) != self.FORMAT_VERSION:
            raise ValueError(f"Unsupported project format: {path}")

        model_data = loaded_file.get(fr.MODEL)

        if not isinstance(model_data, dict):
            raise TypeError(f"Model data is not a dictionary: {path}")

        model = Model.from_dict(model_data)

        preferences_data = loaded_file.get(fr.PREFERENCES)

        if not isinstance(preferences_data, dict):
            raise TypeError(
                f"Preferences data is not a dictionary: {path}")

        preferences = UserPreferences.from_snapshot(preferences_data)

        return model, preferences
