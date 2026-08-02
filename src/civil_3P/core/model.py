from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from civil_3P.core.enums import ElementType

REQUIRED_TABLES = (
    "nodes",
    "elements_1d",
    "elements_2d",
    "properties",
    "results",
    "overrides",
)


@dataclass(slots=True)
class FEMModel:
    nodes: pd.DataFrame
    elements_1d: pd.DataFrame
    elements_2d: pd.DataFrame
    properties: pd.DataFrame
    results: pd.DataFrame
    overrides: pd.DataFrame

    @classmethod
    def empty(cls) -> "FEMModel":
        return cls(
            nodes=pd.DataFrame(columns=["node_id", "x", "y", "z"]),
            elements_1d=pd.DataFrame(columns=[
                "element_id",
                "node_i",
                "node_j",
                "material_id",
                "section_id",
            ]),
            elements_2d=pd.DataFrame(columns=[
                "element_id",
                "node_1",
                "node_2",
                "node_3",
                "node_4",
                "material_id",
                "thickness",
            ]),
            properties=pd.DataFrame(columns=[
                "entity_type",
                "entity_id",
                "property_name",
                "property_value",
            ]),
            results=pd.DataFrame(columns=[
                "case_id",
                "source",
                "element_type",
                "element_id",
                "node_id",
                "station",
                "result_name",
                "value",
                "location",
            ]),
            overrides=pd.DataFrame(columns=[
                "entity_type",
                "entity_id",
                "property_name",
                "property_value",
            ]),
        )

    @classmethod
    def from_tables(cls,
                    **tables: pd.DataFrame) -> "FEMModel":
        missing = [name for name in REQUIRED_TABLES if name not in tables]
        if missing:
            raise ValueError(f"Missing tables for FEMModel: {missing}")

        model = cls(**{name: tables[name].copy() for name in REQUIRED_TABLES})
        model.validate()

        return model

    def validate(self) -> None:
        required_node_columns = {"node_id", "x", "y", "z"}
        required_1d_columns = {"element_id", "node_i", "node_j"}
        required_2d_columns = {
            "element_id",
            "node_1",
            "node_2",
            "node_3",
        }

        required_result_columns = {
            "case_id",
            "source",
            "element_type",
            "element_id",
            "node_id",
            "station",
            "result_name",
            "value",
            "location",
        }

        if not required_node_columns.issubset(self.nodes.columns):
            raise ValueError("nodes table is missing required columns")

        if not required_1d_columns.issubset(self.elements_1d.columns):
            raise ValueError("elements_1d table is missing required columns")

        if not required_2d_columns.issubset(self.elements_2d.columns):
            raise ValueError("elements_2d table is missing required columns")

        if "node_4" in self.elements_2d.columns:
            self._validate_shell_connectivity()

        if not required_result_columns.issubset(self.results.columns):
            raise ValueError("results table is missing required columns")

    def _validate_shell_connectivity(self) -> None:
        for row in self.elements_2d.itertuples(index=False):
            node_ids = [
                getattr(row, "node_1", None),
                getattr(row, "node_2", None),
                getattr(row, "node_3", None),
                getattr(row, "node_4", None),
            ]
            present_nodes = [node_id for node_id in node_ids if node_id not in (None, "")]
            if len(present_nodes) < 3:
                raise ValueError("Each 2D element must have at least 3 node references")

    def table_for(self, 
                  element_type: ElementType) -> pd.DataFrame:
        if element_type == ElementType.BAR_1D:
            return self.elements_1d

        if element_type == ElementType.SHELL_2D:
            return self.elements_2d

        raise ValueError(f"Unsupported element type: {element_type}")

    def property_map(self, 
                     entity_type: str) -> dict[tuple[str, str], Any]:
        filtered = self.properties[
            self.properties["entity_type"] == entity_type
        ]

        return {
            (str(row.entity_id), str(row.property_name)): row.property_value
            for row in filtered.itertuples(index=False)
        }
