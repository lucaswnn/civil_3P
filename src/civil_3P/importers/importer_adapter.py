from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from civil_3P.core.model import FEMModel
from civil_3P.standard import units
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
    tables_dict: dict[str, pd.DataFrame]
    units_dict: dict[str, dict[str, str]]

    @classmethod
    def empty(cls) -> "IntermediateRepresentation":
        model = FEMModel.empty()
        return cls(
            tables_dict={
                rpr.ModelTables.NODES: model.tables_dict[rpr.ModelTables.NODES].copy(),
                rpr.ModelTables.ELEMENTS_1D: model.tables_dict[rpr.ModelTables.ELEMENTS_1D].copy(),
                rpr.ModelTables.ELEMENTS_2D: model.tables_dict[rpr.ModelTables.ELEMENTS_2D].copy(),
                rpr.ModelTables.MATERIALS: model.tables_dict[rpr.ModelTables.MATERIALS].copy(),
                rpr.ModelTables.SECTIONS: model.tables_dict[rpr.ModelTables.SECTIONS].copy(),
                rpr.ModelTables.ORIGIN_1D_RESULTS: model.tables_dict[rpr.ModelTables.ORIGIN_1D_RESULTS].copy(),
                rpr.ModelTables.ORIGIN_2D_RESULTS: model.tables_dict[rpr.ModelTables.ORIGIN_2D_RESULTS].copy(),
                rpr.ModelTables.ORIGIN_NODE_DISPLACEMENTS: model.tables_dict[rpr.ModelTables.ORIGIN_NODE_DISPLACEMENTS].copy(),
                rpr.ModelTables.ORIGIN_NODE_REACTIONS: model.tables_dict[rpr.ModelTables.ORIGIN_NODE_REACTIONS].copy(),
                rpr.ModelTables.TASK_1D_RESULTS: model.tables_dict[rpr.ModelTables.TASK_1D_RESULTS].copy(),
                rpr.ModelTables.TASK_2D_RESULTS: model.tables_dict[rpr.ModelTables.TASK_2D_RESULTS].copy(),
                rpr.ModelTables.TASK_NODE_RESULTS: model.tables_dict[rpr.ModelTables.TASK_NODE_RESULTS].copy(),
            },
            units_dict=model.units_dict.copy(),
        )

    def to_model(self) -> FEMModel:
        model = FEMModel.empty()
        return FEMModel.from_tables(
            tables={
                rpr.ModelTables.NODES: self.tables_dict[rpr.ModelTables.NODES].copy(),
                rpr.ModelTables.ELEMENTS_1D: self.tables_dict[rpr.ModelTables.ELEMENTS_1D].copy(),
                rpr.ModelTables.ELEMENTS_2D: self.tables_dict[rpr.ModelTables.ELEMENTS_2D].copy(),
                rpr.ModelTables.MATERIALS: self.tables_dict[rpr.ModelTables.MATERIALS].copy(),
                rpr.ModelTables.SECTIONS: self.tables_dict[rpr.ModelTables.SECTIONS].copy(),
                rpr.ModelTables.ORIGIN_1D_RESULTS: self.tables_dict[rpr.ModelTables.ORIGIN_1D_RESULTS].copy(),
                rpr.ModelTables.ORIGIN_2D_RESULTS: self.tables_dict[rpr.ModelTables.ORIGIN_2D_RESULTS].copy(),
                rpr.ModelTables.ORIGIN_NODE_DISPLACEMENTS: self.tables_dict[rpr.ModelTables.ORIGIN_NODE_DISPLACEMENTS].copy(),
                rpr.ModelTables.ORIGIN_NODE_REACTIONS: self.tables_dict[rpr.ModelTables.ORIGIN_NODE_REACTIONS].copy(),
                rpr.ModelTables.TASK_1D_RESULTS: model.tables_dict[rpr.ModelTables.TASK_1D_RESULTS].copy(),
                rpr.ModelTables.TASK_2D_RESULTS: model.tables_dict[rpr.ModelTables.TASK_2D_RESULTS].copy(),
                rpr.ModelTables.TASK_NODE_RESULTS: model.tables_dict[rpr.ModelTables.TASK_NODE_RESULTS].copy(),
            },
            units=self.units_dict,
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
                      units_dict: dict[str, str],
                      ) -> None:
        print(
            f"Processing units for table with columns: {table.columns.tolist()}")
        for column, unit in units_dict.items():
            if column in table.columns:
                self.normalize_column_unit(table, column, unit)
