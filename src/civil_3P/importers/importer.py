from enum import StrEnum

from pathlib import Path

from civil_3P.core.model import FEMModel
from civil_3P.importers.sap2000_importer import Sap2000Importer


class ImporterProfile(StrEnum):
    SAP2000 = "sap2000"


class ImporterRegistry:
    def __init__(self) -> None:
        self._registry = {ImporterProfile.SAP2000: Sap2000Importer()}

    def import_model(self, profile: ImporterProfile, source: str | Path) -> FEMModel:
        importer = self._registry[profile]
        return importer.import_model(source)
