from __future__ import annotations

import pickle
from pathlib import Path

from civil_3P.core.model import FEMModel


class FileService:
    def save(self, model: FEMModel, path: str | Path) -> None:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("wb") as f:
            pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, path: str | Path) -> FEMModel:
        file_path = Path(path)
        with file_path.open("rb") as f:
            loaded_model = pickle.load(f)

        if not isinstance(loaded_model, FEMModel):
            raise TypeError(f"File does not contain a FEMModel: {path}")

        return loaded_model
