from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from civil_3P.core.model import FEMModel
from civil_3P.standard import units
from civil_3P.standard.model_representation import ModelTables as mt
from civil_3P.standard import model_representation as rpr
from civil_3P.utils.pandas_utils import PandasUtils as pdUtils


@dataclass(frozen=True, slots=True)
class ColumnMapping:
    rename: dict[str, str]
    defaults: dict[str, object]


@dataclass(frozen=True, slots=True)
class ImporterSpec:
    tables_mapping: dict[str, ColumnMapping]


@dataclass(slots=True)
class IntermediateRepresentation:
    tables: dict[str, pd.DataFrame]
    units: dict[str, dict[str, str]]

    @classmethod
    def empty(cls) -> "IntermediateRepresentation":
        model = FEMModel.empty()
        return cls(
            tables={
                mt.NODES: model.tables[mt.NODES].copy(),
                mt.ELEMENTS_1D: model.tables[mt.ELEMENTS_1D].copy(),
                mt.ELEMENTS_2D: model.tables[mt.ELEMENTS_2D].copy(),
                mt.MATERIALS: model.tables[mt.MATERIALS].copy(),
                mt.SECTIONS: model.tables[mt.SECTIONS].copy(),
                mt.ORIGIN_1D_RESULTS: model.tables[mt.ORIGIN_1D_RESULTS].copy(),
                mt.ORIGIN_2D_RESULTS: model.tables[mt.ORIGIN_2D_RESULTS].copy(),
                mt.ORIGIN_NODE_DISPLACEMENTS: model.tables[mt.ORIGIN_NODE_DISPLACEMENTS].copy(),
                mt.ORIGIN_NODE_REACTIONS: model.tables[mt.ORIGIN_NODE_REACTIONS].copy(),
                mt.LOAD_CASES: model.tables[mt.LOAD_CASES].copy(),
                mt.TASK_1D_RESULTS: model.tables[mt.TASK_1D_RESULTS].copy(),
                mt.TASK_2D_RESULTS: model.tables[mt.TASK_2D_RESULTS].copy(),
                mt.TASK_NODE_RESULTS: model.tables[mt.TASK_NODE_RESULTS].copy(),
            },
            units=model.units.copy(),
        )

    def to_model(self) -> FEMModel:
        model = FEMModel.empty()
        return FEMModel.from_tables(
            tables={
                mt.NODES: self.tables[mt.NODES].copy(),
                mt.ELEMENTS_1D: self.tables[mt.ELEMENTS_1D].copy(),
                mt.ELEMENTS_2D: self.tables[mt.ELEMENTS_2D].copy(),
                mt.MATERIALS: self.tables[mt.MATERIALS].copy(),
                mt.SECTIONS: self.tables[mt.SECTIONS].copy(),
                mt.ORIGIN_1D_RESULTS: self.tables[mt.ORIGIN_1D_RESULTS].copy(),
                mt.ORIGIN_2D_RESULTS: self.tables[mt.ORIGIN_2D_RESULTS].copy(),
                mt.ORIGIN_NODE_DISPLACEMENTS: self.tables[mt.ORIGIN_NODE_DISPLACEMENTS].copy(),
                mt.ORIGIN_NODE_REACTIONS: self.tables[mt.ORIGIN_NODE_REACTIONS].copy(),
                mt.LOAD_CASES: self.tables[mt.LOAD_CASES].copy(),
                mt.TASK_1D_RESULTS: model.tables[mt.TASK_1D_RESULTS].copy(),
                mt.TASK_2D_RESULTS: model.tables[mt.TASK_2D_RESULTS].copy(),
                mt.TASK_NODE_RESULTS: model.tables[mt.TASK_NODE_RESULTS].copy(),
            },
            units=self.units,
        )


class ImporterAdapter(ABC):
    def __init__(self,
                 spec: ImporterSpec,
                 unit_map: dict[str, str],
                 ) -> None:
        self._spec = spec
        self._unit_map = unit_map

    def import_model(self, source: str | Path) -> FEMModel:
        intermediate = self.read_intermediate(source)
        return intermediate.to_model()

    @abstractmethod
    def read_intermediate(self, source: str | Path) -> IntermediateRepresentation:
        raise NotImplementedError

    def map_dataframe(self, df: pd.DataFrame, mapping: ColumnMapping) -> None:
        print(f"Mapping dataframe columns:\n"
              f"{df.columns.tolist()} ->"
              f"\n{[f'{k} -> {v.value}' for k, v in mapping.rename.items()]}")

        pdUtils.rename_or_add_columns(
            df,
            rename_mapping=mapping.rename,
            default_mapping=mapping.defaults,
        )

    def normalize_column_unit(self,
                              frame: pd.DataFrame,
                              column: str,
                              unit: str,
                              ) -> None:
        unit = self._unit_map.get(unit)
        if unit is None:
            raise ValueError(f"Unit '{unit}' not found in unit map")

        physicalquantity = units.UnitConverter.get_physical_quantity(unit)
        if unit == units.Unitless.NONE:
            print(f"Column '{column}' is not number, skipping normalization")
            frame[column] = frame[column].astype(str)
            return

        frame[column] = frame[column].astype(float)
        if unit == units.Unitless.UNITLESS:
            print(f"Column '{column}' is unitless, skipping normalization")
            return

        normalized_unit = units.DEFAULT_UNITS[physicalquantity]
        frame[column] = frame[column].apply(
            lambda x: units.UnitConverter.convert(x, unit, normalized_unit))

    def process_units(self,
                      table: pd.DataFrame,
                      units: dict[str, str],
                      ) -> None:
        print(
            f"Processing units for table with columns: {table.columns.tolist()}")
        for column, unit in units.items():
            if column in table.columns:
                self.normalize_column_unit(table, column, unit)
