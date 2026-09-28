from __future__ import annotations

from pathlib import Path

import pytest

from civil_3P.core.model import Model
from civil_3P.importers.sap2000_importer import Sap2000Importer
from civil_3P.standard.model_representation import (
    REQUIRED_MODEL_SCHEMA
)

FIXTURES_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "sap2000"
SAMPLE_WORKBOOK = FIXTURES_DIR / "sample_model.xlsx"


class TestSap2000ImporterFromWorkbook:
    @classmethod
    def setup_class(cls) -> None:
        cls.importer = Sap2000Importer()

    def test_import_model_returns_valid_model(self) -> None:
        model = self.importer.import_model(SAMPLE_WORKBOOK)

        assert isinstance(model, Model)

    def test_import_model_maps_columns_to_internal_names(self) -> None:
        model = self.importer.import_model(SAMPLE_WORKBOOK)

        for table_name, required_columns in REQUIRED_MODEL_SCHEMA.items():
            table_columns = set(model.tables[table_name].columns)
            assert set(required_columns).issubset(table_columns)

    def test_check_column_types(self) -> None:
        # TODO
        assert False, "Not implemented yet"


class TestSap2000ImporterErrors:
    def setup_method(self) -> None:
        self.importer = Sap2000Importer()

    def test_read_intermediate_with_directory_raises_value_error(
        self,
        tmp_path: Path,
    ) -> None:
        with pytest.raises(ValueError, match="Expected a file path"):
            self.importer.read_intermediate(tmp_path)

    def test_read_intermediate_with_missing_file_raises(
        self,
        tmp_path: Path,
    ) -> None:
        missing_file = tmp_path / "does_not_exist.xlsx"

        with pytest.raises(Exception):
            self.importer.read_intermediate(missing_file)
