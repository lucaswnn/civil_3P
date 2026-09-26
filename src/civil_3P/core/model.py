from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd

from civil_3P.standard.file_representation import (
    DATAFRAME_DICT_CONV,
    FileRepresentation as fr,
)
from civil_3P.standard.model_representation import (
    REQUIRED_MODEL_SCHEMA,
    Elements1DColumns as rpr_1d,
    Elements2DColumns as rpr_2d,
    ModelTables as mt,
    NodesColumns as rpr_node,
    Origin1DResultsColumns as rpr_origin_1d,
    Origin2DResultsColumns as rpr_origin_2d,
    OriginNodeDisplacementsColumns as rpr_origin_node_d,
    OriginNodeReactionsColumns as rpr_origin_node_r,
)
from civil_3P.standard.units import DEFAULT_UNITS, UNITS_SCHEME
from civil_3P.utils.pandas_utils import PandasUtils

if TYPE_CHECKING:
    from civil_3P.core.selection_context import SelectionContext

DATAFRAME_DICT_CONV = "records"


@dataclass(slots=True)
class Model:
    tables: dict[str, pd.DataFrame]
    units: dict[str, dict[str, str]]

    @classmethod
    def empty(cls) -> "Model":
        return cls(
            units=DEFAULT_UNITS.copy(),
            tables={
                table_name: pd.DataFrame(columns=cols)
                for table_name, cols in REQUIRED_MODEL_SCHEMA.items()
            },
        )

    @classmethod
    def from_tables(
        cls,
        tables: dict[str, pd.DataFrame],
        units: dict[str, str],
    ) -> "Model":
        missing = [
            name for name in REQUIRED_MODEL_SCHEMA.keys() if name not in tables.keys()
        ]

        if missing:
            raise ValueError(f"Missing tables for FEMModel: {missing}")

        model = cls(
            tables={name: tables[name].copy()
                    for name in REQUIRED_MODEL_SCHEMA},
            units=units.copy(),
        )
        model.validate_tables()
        model.validate_units()

        return model

    @classmethod
    def from_dict(
        cls,
        data: dict[str, dict[str, Any]],
    ) -> Model:
        dict_tables = data.get(fr.MODEL_TABLES, {})
        units = data.get(fr.MODEL_UNITS, {})
        tables = {
            name: pd.DataFrame(data)
            for name, data in dict_tables.items()
        }

        return cls.from_tables(tables=tables, units=units)

    def validate_units(self) -> None:
        quantities = set(self.units.keys())
        required_quantities = set(DEFAULT_UNITS.keys())

        if not required_quantities.issubset(quantities):
            raise ValueError(
                f"Missing units for quantities: "
                f"{required_quantities - quantities}"
            )

        for quantity, unit in self.units.items():
            if unit not in UNITS_SCHEME[quantity]:
                raise ValueError(
                    f"Invalid unit '{unit}' for quantity '{quantity}'. "
                    f"Allowed units are: {UNITS_SCHEME[quantity]}"
                )

    def validate_tables(self) -> None:
        for name, cols in REQUIRED_MODEL_SCHEMA.items():
            PandasUtils.ensure_columns(self.tables[name], cols)

    def copy(self) -> Model:
        return Model(
            tables={name: df.copy() for name, df in self.tables.items()},
            units=self.units.copy(),
        )

    def filter_by_selection(
        self,
        selection: SelectionContext,
    ) -> Model:
        sel = self.copy()
        element_1d_df = sel.tables[mt.ELEMENTS_1D]
        element_2d_df = sel.tables[mt.ELEMENTS_2D]
        res_1d_df = sel.tables[mt.ORIGIN_1D_RESULTS]
        res_2d_df = sel.tables[mt.ORIGIN_2D_RESULTS]
        res_node_d_df = sel.tables[mt.ORIGIN_NODE_DISPLACEMENTS]
        res_node_r_df = sel.tables[mt.ORIGIN_NODE_REACTIONS]
        element_1d_df = element_1d_df[
            element_1d_df[rpr_1d.ELEMENT].isin(selection.element_1d_ids)
        ]
        element_2d_df = element_2d_df[
            element_2d_df[rpr_2d.ELEMENT].isin(selection.all_element_2d_ids)
        ]
        res_1d_df = res_1d_df[
            res_1d_df[rpr_origin_1d.ELEMENT].isin(selection.element_1d_ids)
        ]
        res_2d_df = res_2d_df[
            res_2d_df[rpr_origin_2d.ELEMENT].isin(selection.all_element_2d_ids)
        ]
        nodes: set[str] = set()
        element_1d_cols = [rpr_1d.NODE_I, rpr_1d.NODE_J]
        nodes.update(set(np.unique(element_1d_df[element_1d_cols])))
        element_2d_cols = [
            rpr_2d.NODE_1,
            rpr_2d.NODE_2,
            rpr_2d.NODE_3,
            rpr_2d.NODE_4,
        ]
        nodes.update(element_2d_df[element_2d_cols].stack().dropna().unique())
        nodes.update(selection.node_ids)
        sel.tables[mt.NODES] = sel.tables[mt.NODES][
            sel.tables[mt.NODES][rpr_node.NODE].isin(nodes)
        ]
        res_node_d_df = res_node_d_df[res_node_d_df[rpr_origin_node_d.NODE].isin(
            nodes)]
        res_node_r_df = res_node_r_df[res_node_r_df[rpr_origin_node_r.NODE].isin(
            nodes)]
        sel.tables[mt.ELEMENTS_1D] = element_1d_df
        sel.tables[mt.ELEMENTS_2D] = element_2d_df
        sel.tables[mt.ORIGIN_1D_RESULTS] = res_1d_df
        sel.tables[mt.ORIGIN_2D_RESULTS] = res_2d_df
        sel.tables[mt.ORIGIN_NODE_DISPLACEMENTS] = res_node_d_df
        sel.tables[mt.ORIGIN_NODE_REACTIONS] = res_node_r_df

        return sel

    def filter_by_selection_reversed(
        self,
        selection: SelectionContext,
    ) -> Model:
        sel = self.copy()
        element_1d_df = sel.tables[mt.ELEMENTS_1D]
        element_2d_df = sel.tables[mt.ELEMENTS_2D]
        nodes_df = sel.tables[mt.NODES]
        res_1d_df = sel.tables[mt.ORIGIN_1D_RESULTS]
        res_2d_df = sel.tables[mt.ORIGIN_2D_RESULTS]
        res_node_d_df = sel.tables[mt.ORIGIN_NODE_DISPLACEMENTS]
        res_node_r_df = sel.tables[mt.ORIGIN_NODE_REACTIONS]
        element_1d_df = element_1d_df[
            ~element_1d_df[rpr_1d.ELEMENT].isin(selection.element_1d_ids)
        ]
        element_2d_df = element_2d_df[
            ~element_2d_df[rpr_2d.ELEMENT].isin(selection.all_element_2d_ids)
        ]
        res_1d_df = res_1d_df[
            ~res_1d_df[rpr_origin_1d.ELEMENT].isin(selection.element_1d_ids)
        ]
        res_2d_df = res_2d_df[
            ~res_2d_df[rpr_origin_2d.ELEMENT].isin(
                selection.all_element_2d_ids)
        ]
        nodes_df = nodes_df[~nodes_df[rpr_node.NODE].isin(selection.node_ids)]
        nodes = set(np.unique(nodes_df[rpr_node.NODE]))
        element_1d_cols = [rpr_1d.NODE_I, rpr_1d.NODE_J]
        nodes.update(set(np.unique(element_1d_df[element_1d_cols])))
        element_2d_cols = [
            rpr_2d.NODE_1,
            rpr_2d.NODE_2,
            rpr_2d.NODE_3,
            rpr_2d.NODE_4,
        ]
        nodes.update(element_2d_df[element_2d_cols].stack().dropna().unique())
        sel.tables[mt.NODES] = sel.tables[mt.NODES][
            sel.tables[mt.NODES][rpr_node.NODE].isin(nodes)
        ]
        res_node_d_df = res_node_d_df[res_node_d_df[rpr_origin_node_d.NODE].isin(
            nodes)]
        res_node_r_df = res_node_r_df[res_node_r_df[rpr_origin_node_r.NODE].isin(
            nodes)]
        sel.tables[mt.ELEMENTS_1D] = element_1d_df
        sel.tables[mt.ELEMENTS_2D] = element_2d_df
        sel.tables[mt.ORIGIN_1D_RESULTS] = res_1d_df
        sel.tables[mt.ORIGIN_2D_RESULTS] = res_2d_df
        sel.tables[mt.ORIGIN_NODE_DISPLACEMENTS] = res_node_d_df
        sel.tables[mt.ORIGIN_NODE_REACTIONS] = res_node_r_df

        return sel

    def filter_by_load_case(self, load_case_id: str) -> Model:
        sel = self.copy()
        df_1d = sel.tables[mt.ORIGIN_1D_RESULTS]
        df_2d = sel.tables[mt.ORIGIN_2D_RESULTS]
        df_node_d = sel.tables[mt.ORIGIN_NODE_DISPLACEMENTS]
        df_node_r = sel.tables[mt.ORIGIN_NODE_REACTIONS]
        df_1d = df_1d[df_1d[rpr_origin_1d.CASE] == load_case_id]
        df_2d = df_2d[df_2d[rpr_origin_2d.CASE] == load_case_id]
        df_node_d = df_node_d[df_node_d[rpr_origin_node_d.CASE]
                              == load_case_id]
        df_node_r = df_node_r[df_node_r[rpr_origin_node_r.CASE]
                              == load_case_id]
        sel.tables[mt.ORIGIN_1D_RESULTS] = df_1d
        sel.tables[mt.ORIGIN_2D_RESULTS] = df_2d
        sel.tables[mt.ORIGIN_NODE_DISPLACEMENTS] = df_node_d
        sel.tables[mt.ORIGIN_NODE_REACTIONS] = df_node_r

        return sel

    def to_dict(self) -> dict[str, dict[str, Any]]:
        return {
            fr.MODEL_TABLES: {
                table_name: df.to_dict(orient=DATAFRAME_DICT_CONV)
                for table_name, df in self.tables.items()
            },
            fr.MODEL_UNITS: self.units.copy(),
        }

    def remove_elements(
        self,
        selection: SelectionContext,
    ) -> Model:
        model = self.copy()
        model.tables[mt.ELEMENTS_1D] = model.tables[mt.ELEMENTS_1D][
            ~model.tables[mt.ELEMENTS_1D][rpr_1d.ELEMENT].isin(
                selection.element_1d_ids)
        ]
        model.tables[mt.ELEMENTS_2D] = model.tables[mt.ELEMENTS_2D][
            ~model.tables[mt.ELEMENTS_2D][rpr_2d.ELEMENT].isin(
                selection.all_element_2d_ids
            )
        ]
        nodes = set(np.unique(model.tables[mt.ELEMENTS_1D][rpr_1d.NODE_I]))
        nodes.update(np.unique(model.tables[mt.ELEMENTS_1D][rpr_1d.NODE_J]))
        nodes.update(np.unique(model.tables[mt.ELEMENTS_2D][rpr_2d.NODE_1]))
        nodes.update(np.unique(model.tables[mt.ELEMENTS_2D][rpr_2d.NODE_2]))
        nodes.update(np.unique(model.tables[mt.ELEMENTS_2D][rpr_2d.NODE_3]))
        nodes.update(model.tables[mt.ELEMENTS_2D]
                     [rpr_2d.NODE_4].dropna().unique())
        nodes = nodes.difference(selection.node_ids)
        model.tables[mt.NODES] = model.tables[mt.NODES][
            model.tables[mt.NODES][rpr_node.NODE].isin(nodes)
        ]

        return model

    def __repr__(self):
        return (
            "FEMModel:"
            f"\nNodes count: {self.tables[mt.NODES].shape[0]}"
            f"\nBars count: {self.tables[mt.ELEMENTS_1D].shape[0]}"
            f"\nShells count: {self.tables[mt.ELEMENTS_2D].shape[0]}"
            f"\nMaterials count: {self.tables[mt.MATERIALS].shape[0]}"
            f"\nSections count: {self.tables[mt.SECTIONS].shape[0]}"
            f"\nLoad cases count: {self.tables[mt.LOAD_CASES].shape[0]}"
        )
