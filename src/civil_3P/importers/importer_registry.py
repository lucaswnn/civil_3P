from pathlib import Path

from civil_3P.core.model import FEMModel
from civil_3P.importers.sap2000_importer import Sap2000Importer
from civil_3P.standard.importer_profiles import ImporterProfiles


class ImporterRegistry:
    def __init__(self) -> None:
        self._registry = {ImporterProfiles.SAP2000: Sap2000Importer()}

    def import_model(self, profile: ImporterProfiles, source: str | Path) -> FEMModel:
        importer = self._registry[profile]
        return importer.import_model(source)
