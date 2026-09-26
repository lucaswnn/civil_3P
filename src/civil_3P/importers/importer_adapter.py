from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

import logging
import pandas as pd

from civil_3P.core.model import Model
from civil_3P.standard import units
from civil_3P.utils.pandas_utils import PandasUtils as pdUtils

if TYPE_CHECKING:
    from civil_3P.importers.column_mapping import ColumnMapping
    from civil_3P.importers.importer_spec import ImporterSpec
    from civil_3P.importers.intermediate_representation import (
        IntermediateRepresentation
    )

logger = logging.getLogger(__name__)


class ImporterAdapter(ABC):
    def __init__(
        self,
        spec: ImporterSpec,
        unit_map: dict[str, str],
    ) -> None:
        self._spec = spec
        self._unit_map = unit_map

    def import_model(self, source: str | Path) -> Model:
        intermediate = self.read_intermediate(source)

        return intermediate.to_model()

    @abstractmethod
    def read_intermediate(self, source: str | Path) -> IntermediateRepresentation:
        raise NotImplementedError

    def map_dataframe(
        self,
        df: pd.DataFrame,
        mapping: ColumnMapping,
    ) -> None:
        logger.info(f"Mapping dataframe columns:\n"
                    f"{df.columns.tolist()} ->"
                    f"\n{[f'{k} -> {v.value}' for k, v in mapping.rename.items()]}")

        pdUtils.rename_or_add_columns(
            df,
            rename_mapping=mapping.rename,
            default_mapping=mapping.defaults,
        )

    def normalize_column_unit(
        self,
        frame: pd.DataFrame,
        column: str,
        unit: str,
    ) -> None:
        unit = self._unit_map.get(unit)

        if unit is None:
            raise ValueError(f"Unit '{unit}' not found in unit map")

        physicalquantity = units.UnitConverter.get_physical_quantity(unit)
        if unit == units.Unitless.NONE:
            logger.info(
                f"Column '{column}' is not number, skipping normalization"
            )
            frame[column] = frame[column].astype(str)

            return

        frame[column] = frame[column].astype(float)

        if unit == units.Unitless.UNITLESS:
            logger.info(
                f"Column '{column}' is unitless, skipping normalization"
            )

            return

        normalized_unit = units.DEFAULT_UNITS[physicalquantity]
        frame[column] = frame[column].apply(
            lambda x: units.UnitConverter.convert(x, unit, normalized_unit)
        )

    def process_units(
        self,
        table: pd.DataFrame,
        units: dict[str, str],
    ) -> None:
        logger.info(
            f"Processing units for table with columns: {table.columns.tolist()}")

        for column, unit in units.items():
            if column in table.columns:
                self.normalize_column_unit(table, column, unit)
