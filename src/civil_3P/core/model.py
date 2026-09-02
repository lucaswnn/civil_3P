from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from civil_3P.core.selection import SelectionContext
from civil_3P.standard import model_components as mc
from civil_3P.standard import model_representation as rpr
from civil_3P.standard.model_representation import ModelTables as mt
from civil_3P.standard.units import *


@dataclass(slots=True)
class FEMModel:
    tables: dict[str, pd.DataFrame]
    units: dict[str, dict[str, str]]

    @classmethod
    def empty(cls) -> "FEMModel":
        return cls(
            units=DEFAULT_UNITS.copy(),
            tables={
                mt.NODES: pd.DataFrame(columns=[
                    rpr.NodesColumns.NODE,
                    rpr.NodesColumns.X,
                    rpr.NodesColumns.Y,
                    rpr.NodesColumns.Z,
                ]),
                mt.ELEMENTS_1D: pd.DataFrame(columns=[
                    rpr.Elements1DColumns.ELEMENT,
                    rpr.Elements1DColumns.NODE_I,
                    rpr.Elements1DColumns.NODE_J,
                    rpr.Elements1DColumns.MATERIAL,
                    rpr.Elements1DColumns.SECTION,
                ]),
                mt.ELEMENTS_2D: pd.DataFrame(columns=[
                    rpr.Elements2DColumns.ELEMENT,
                    rpr.Elements2DColumns.NODE_1,
                    rpr.Elements2DColumns.NODE_2,
                    rpr.Elements2DColumns.NODE_3,
                    rpr.Elements2DColumns.NODE_4,
                    rpr.Elements2DColumns.MATERIAL,
                    rpr.Elements2DColumns.THICKNESS,
                ]),
                mt.MATERIALS: pd.DataFrame(columns=[
                    rpr.MaterialsColumns.MATERIAL,
                    rpr.MaterialsColumns.YOUNG_MODULUS,
                    rpr.MaterialsColumns.SHEAR_MODULUS,
                    rpr.MaterialsColumns.POISSON_RATIO,
                    rpr.MaterialsColumns.THERMAL_COEFF,
                ]),
                mt.SECTIONS: pd.DataFrame(columns=[
                    rpr.SectionsColumns.SECTION,
                    rpr.SectionsColumns.AREA,
                    rpr.SectionsColumns.INERTIA_22,
                    rpr.SectionsColumns.INERTIA_33,
                ]),
                mt.ORIGIN_1D_RESULTS: pd.DataFrame(columns=[
                    rpr.Origin1DResultsColumns.ELEMENT,
                    rpr.Origin1DResultsColumns.STATION,
                    rpr.Origin1DResultsColumns.CASE,
                    rpr.Origin1DResultsColumns.NORMAL,
                    rpr.Origin1DResultsColumns.SHEAR_2,
                    rpr.Origin1DResultsColumns.SHEAR_3,
                    rpr.Origin1DResultsColumns.TORSION,
                    rpr.Origin1DResultsColumns.BENDING_2,
                    rpr.Origin1DResultsColumns.BENDING_3,
                ]),
                mt.ORIGIN_2D_RESULTS: pd.DataFrame(columns=[
                    rpr.Elements2DColumns.ELEMENT,
                    rpr.Origin2DResultsColumns.NODE,
                    rpr.Origin2DResultsColumns.CASE,
                    rpr.Origin2DResultsColumns.NORMAL_11,
                    rpr.Origin2DResultsColumns.NORMAL_22,
                    rpr.Origin2DResultsColumns.NORMAL_12,
                    rpr.Origin2DResultsColumns.BENDING_11,
                    rpr.Origin2DResultsColumns.BENDING_22,
                    rpr.Origin2DResultsColumns.BENDING_12,
                    rpr.Origin2DResultsColumns.SHEAR_13,
                    rpr.Origin2DResultsColumns.SHEAR_23,
                ]),
                mt.ORIGIN_NODE_DISPLACEMENTS: pd.DataFrame(columns=[
                    rpr.OriginNodeDisplacementsColumns.NODE,
                    rpr.OriginNodeDisplacementsColumns.CASE,
                    rpr.OriginNodeDisplacementsColumns.DX,
                    rpr.OriginNodeDisplacementsColumns.DY,
                    rpr.OriginNodeDisplacementsColumns.DZ,
                    rpr.OriginNodeDisplacementsColumns.RX,
                    rpr.OriginNodeDisplacementsColumns.RY,
                    rpr.OriginNodeDisplacementsColumns.RZ,
                ]),
                mt.ORIGIN_NODE_REACTIONS: pd.DataFrame(columns=[
                    rpr.OriginNodeReactionsColumns.NODE,
                    rpr.OriginNodeReactionsColumns.CASE,
                    rpr.OriginNodeReactionsColumns.FX,
                    rpr.OriginNodeReactionsColumns.FY,
                    rpr.OriginNodeReactionsColumns.FZ,
                    rpr.OriginNodeReactionsColumns.MX,
                    rpr.OriginNodeReactionsColumns.MY,
                    rpr.OriginNodeReactionsColumns.MZ,
                ]),
                mt.LOAD_CASES: pd.DataFrame(columns=[
                    rpr.LoadCasesColumns.CASE,
                    rpr.LoadCasesColumns.DESCRIPTION,
                ]),
                mt.TASK_1D_RESULTS: pd.DataFrame(columns=[
                    rpr.Task1DResultsColumns.ELEMENT,
                    rpr.Task1DResultsColumns.STATION,
                    rpr.Task1DResultsColumns.CASE,
                    rpr.Task1DResultsColumns.VALUE,
                ]),
                mt.TASK_2D_RESULTS: pd.DataFrame(columns=[
                    rpr.Task2DResultsColumns.ELEMENT,
                    rpr.Task2DResultsColumns.NODE,
                    rpr.Task2DResultsColumns.CASE,
                    rpr.Task2DResultsColumns.VALUE,
                ]),
                mt.TASK_NODE_RESULTS: pd.DataFrame(columns=[
                    rpr.TaskNodeResultsColumns.NODE,
                    rpr.TaskNodeResultsColumns.CASE,
                    rpr.TaskNodeResultsColumns.VALUE,
                ]),
            }
        )

    @classmethod
    def from_tables(cls,
                    tables: dict[str, pd.DataFrame],
                    units: dict[str, str],) -> "FEMModel":
        missing = [
            name for name in rpr.REQUIRED_TABLES if name not in tables.keys()]
        if missing:
            raise ValueError(f"Missing tables for FEMModel: {missing}")

        model = cls(tables={name: tables[name].copy()
                            for name in rpr.REQUIRED_TABLES},
                    units=units.copy())
        model.validate_tables()
        model.validate_units()

        return model

    def validate_units(self) -> None:
        quantities = set(self.units.keys())
        required_quantities = set(DEFAULT_UNITS.keys())

        if not required_quantities.issubset(quantities):
            raise ValueError(
                f"Missing units for quantities: {required_quantities - quantities}")

        if self.units[PhysicalQuantities.LENGTH] not in [LengthUnits.METER,
                                                         LengthUnits.MILLIMETER,
                                                         LengthUnits.CENTIMETER]:
            raise ValueError(
                f"Length unit must be either "
                f"'{LengthUnits.METER}', "
                f"'{LengthUnits.MILLIMETER}', or "
                f"'{LengthUnits.CENTIMETER}'")

        if self.units[PhysicalQuantities.FORCE] not in [ForceUnits.NEWTON,
                                                        ForceUnits.KILONEWTON,
                                                        ForceUnits.TON_FORCE,
                                                        ForceUnits.KILOGRAM_FORCE]:
            raise ValueError(
                f"Force unit must be either "
                f"'{ForceUnits.NEWTON}', "
                f"'{ForceUnits.KILONEWTON}', "
                f"'{ForceUnits.TON_FORCE}', or "
                f"'{ForceUnits.KILOGRAM_FORCE}'")

        if self.units[PhysicalQuantities.TEMPERATURE] not in [TemperatureUnits.CELSIUS,
                                                              TemperatureUnits.FAHRENHEIT]:
            raise ValueError(
                f"Temperature unit must be either "
                f"'{TemperatureUnits.CELSIUS}' or "
                f"'{TemperatureUnits.FAHRENHEIT}'")

    def validate_tables(self) -> None:
        required_nodes_columns = {col for col in rpr.NodesColumns}
        required_elements_1d_columns = {
            col for col in rpr.Elements1DColumns}
        required_elements_2d_columns = {
            col for col in rpr.Elements2DColumns}
        required_materials_columns = {
            col for col in rpr.MaterialsColumns}
        required_sections_columns = {col for col in rpr.SectionsColumns}
        required_origin_1d_results_columns = {
            col for col in rpr.Origin1DResultsColumns}
        required_origin_2d_results_columns = {
            col for col in rpr.Origin2DResultsColumns}
        required_origin_node_displacements_columns = {
            col for col in rpr.OriginNodeDisplacementsColumns}
        required_origin_reactions_node_columns = {
            col for col in rpr.OriginNodeReactionsColumns}
        required_task_1d_results_columns = {
            col for col in rpr.Task1DResultsColumns}
        required_task_2d_results_columns = {
            col for col in rpr.Task2DResultsColumns}
        required_task_node_results_columns = {
            col for col in rpr.TaskNodeResultsColumns}

        if not required_nodes_columns.issubset(self.tables[mt.NODES].columns):
            raise ValueError("nodes table is missing required columns")

        if not required_elements_1d_columns.issubset(self.tables[mt.ELEMENTS_1D].columns):
            raise ValueError("elements_1d table is missing required columns")

        if not required_elements_2d_columns.issubset(self.tables[mt.ELEMENTS_2D].columns):
            raise ValueError("elements_2d table is missing required columns")

        if not required_materials_columns.issubset(self.tables[mt.MATERIALS].columns):
            raise ValueError("materials table is missing required columns")

        if not required_sections_columns.issubset(self.tables[mt.SECTIONS].columns):
            raise ValueError("sections table is missing required columns")

        if not required_origin_1d_results_columns.issubset(
            self.tables[mt.ORIGIN_1D_RESULTS].columns
        ):
            raise ValueError(
                "origin_1d_results table is missing required columns")

        if not required_origin_2d_results_columns.issubset(
            self.tables[mt.ORIGIN_2D_RESULTS].columns
        ):
            raise ValueError(
                "origin_2d_results table is missing required columns")

        if not required_origin_node_displacements_columns.issubset(
            self.tables[mt.ORIGIN_NODE_DISPLACEMENTS].columns
        ):
            raise ValueError(
                "origin_node_displacements table is missing required columns")

        if not required_origin_reactions_node_columns.issubset(
            self.tables[mt.ORIGIN_NODE_REACTIONS].columns
        ):
            raise ValueError(
                "origin_node_reactions table is missing required columns")

        if not required_task_1d_results_columns.issubset(self.tables[mt.TASK_1D_RESULTS].columns):
            raise ValueError(
                "task_1d_results table is missing required columns")

        if not required_task_2d_results_columns.issubset(self.tables[mt.TASK_2D_RESULTS].columns):
            raise ValueError(
                "task_2d_results table is missing required columns")

        if not required_task_node_results_columns.issubset(self.tables[mt.TASK_NODE_RESULTS].columns):
            raise ValueError(
                "task_node_results table is missing required columns")

    def property_map(self,
                     entity_type: str) -> dict[tuple[str, str], Any]:
        filtered = self.overrides_df[
            self.overrides_df["entity_type"] == entity_type
        ]

        return {
            (str(row.entity_id), str(row.property_name)): row.property_value
            for row in filtered.itertuples(index=False)
        }

    def copy(self) -> FEMModel:
        return FEMModel(
            tables={name: df.copy() for name, df in self.tables.items()},
            units=self.units.copy(),
        )

    def filter_by_selection(self,
                            selection: SelectionContext) -> FEMModel:
        sel = self.copy()

        def filter_table_by_element_type(element_drop_table: str,
                                         result_drop_table: str,
                                         element_filter_table: str,
                                         result_filter_table: str) -> None:
            sel.tables[element_drop_table] = pd.DataFrame(
                columns=sel.tables[element_drop_table].columns)
            sel.tables[result_drop_table] = pd.DataFrame(
                columns=sel.tables[result_drop_table].columns)
            sel.tables[element_filter_table] = (
                sel.tables[element_filter_table]
                [
                    sel.tables[element_filter_table][rpr.Elements1DColumns.ELEMENT]
                    .isin(selection.all_element_ids)
                ]
            )
            sel.tables[result_filter_table] = (
                sel.tables[result_filter_table]
                [
                    sel.tables[result_filter_table][rpr.Origin1DResultsColumns.ELEMENT]
                    .isin(selection.all_element_ids)
                ]
            )

        if selection.element_type == mc.ModelComponents.ELEMENTS_1D:
            filter_table_by_element_type(
                element_drop_table=mt.ELEMENTS_2D,
                result_drop_table=mt.ORIGIN_2D_RESULTS,
                element_filter_table=mt.ELEMENTS_1D,
                result_filter_table=mt.ORIGIN_1D_RESULTS,
            )

        elif selection.element_type == mc.ModelComponents.ELEMENTS_2D:
            filter_table_by_element_type(
                element_drop_table=mt.ELEMENTS_1D,
                result_drop_table=mt.ORIGIN_1D_RESULTS,
                element_filter_table=mt.ELEMENTS_2D,
                result_filter_table=mt.ORIGIN_2D_RESULTS,
            )

        return sel

    def filter_by_load_case(self, load_case_id: str) -> FEMModel:
        print(load_case_id)
        sel = self.copy()

        df_1d = sel.tables[mt.ORIGIN_1D_RESULTS]
        df_2d = sel.tables[mt.ORIGIN_2D_RESULTS]
        df_node_d = sel.tables[mt.ORIGIN_NODE_DISPLACEMENTS]
        df_node_r = sel.tables[mt.ORIGIN_NODE_REACTIONS]
        df_1d = df_1d[df_1d[rpr.Task1DResultsColumns.CASE] == load_case_id]
        df_2d = df_2d[df_2d[rpr.Task2DResultsColumns.CASE] == load_case_id]
        df_node_d = df_node_d[df_node_d[rpr.TaskNodeResultsColumns.CASE]
                              == load_case_id]
        df_node_r = df_node_r[df_node_r[rpr.TaskNodeResultsColumns.CASE]
                              == load_case_id]

        sel.tables[mt.ORIGIN_1D_RESULTS] = df_1d
        sel.tables[mt.ORIGIN_2D_RESULTS] = df_2d
        sel.tables[mt.ORIGIN_NODE_DISPLACEMENTS] = df_node_d
        sel.tables[mt.ORIGIN_NODE_REACTIONS] = df_node_r

        return sel
