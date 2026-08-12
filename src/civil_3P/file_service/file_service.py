from __future__ import annotations

import pickle
from pathlib import Path

from civil_3P.core.model import FEMModel


class ModelArchiveService:
    def save(self, model: FEMModel, path: str | Path) -> None:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("wb") as archive_file:
            pickle.dump(model, archive_file, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, path: str | Path) -> FEMModel:
        file_path = Path(path)
        with file_path.open("rb") as archive_file:
            loaded_model = pickle.load(archive_file)

        if not isinstance(loaded_model, FEMModel):
            raise TypeError(f"Archive does not contain a FEMModel: {path}")

        return loaded_model
