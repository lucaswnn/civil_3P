from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.importers.importer_registry import ImporterRegistry

if TYPE_CHECKING:
    from pathlib import Path

    from civil_3P.core.model import FEMModel
    from civil_3P.standard.importer_profiles import ImporterProfiles


class ImporterService:
    _instance: ImporterService | None = None

    def __new__(cls) -> ImporterService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._registry = ImporterRegistry()
        return cls._instance

    def import_model(
        self,
        profile: ImporterProfiles,
        directory: str | Path,
    ) -> FEMModel:
        return self._registry.import_model(profile, directory)
