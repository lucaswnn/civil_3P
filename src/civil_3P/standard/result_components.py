from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

import pandas as pd

from civil_3P.standard import model_components as mc


class ResultLocation(StrEnum):
    ELEMENT = "element"
    NODE = "node"


class VisualizationMode(StrEnum):
    ELEMENT = "element"
    NODE_AVERAGED = "node_averaged"
    NODE_RAW = "node_raw"


class VisualizationContentKind(StrEnum):
    NODE_POINTS = "node_points"
    ELEMENT_1D_PROFILE = "element_1d_profile"
    ELEMENT_2D_UNIFORM = "element_2d_uniform"
    ELEMENT_2D_SHARED_NODES = "element_2d_shared_nodes"
    ELEMENT_2D_ISOLATED_NODES = "element_2d_isolated_nodes"


# Column names as actually produced by ResultProcessor/task plugins (see core/results.py).
_NODE_ITEM_COL = "node_id"
_ELEMENT_1D_ITEM_COL = "element"
_ELEMENT_1D_STATION_COL = "station"
_ELEMENT_2D_ITEM_COL = "element_id"
_ELEMENT_2D_NODE_COL = "node_id"
_VALUE_COL = "value"


@dataclass(frozen=True, slots=True)
class VisualizationData:
    kind: VisualizationContentKind
    value_range: tuple[float, float]
    node_values: dict[str, float] = field(default_factory=dict)
    element_values: dict[str, float] = field(default_factory=dict)
    element_station_values: dict[str, list[tuple[float, float]]] = field(
        default_factory=dict)
    element_node_values: dict[str, dict[str, float]] = field(
        default_factory=dict)


class VisualizationContent:
    def __init__(self,
                mode: VisualizationMode,
                component: mc.ModelComponents) -> None:
        self._mode = mode
        self._component = component

    def build(self, results: pd.DataFrame) -> VisualizationData:
        if self._component == mc.ModelComponents.NODES:
            return self._build_node_points(results)

        if self._component == mc.ModelComponents.ELEMENTS_1D:
            return self._build_element_1d_profile(results)

        if self._component == mc.ModelComponents.ELEMENTS_2D:
            if self._mode == VisualizationMode.ELEMENT:
                return self._build_element_2d_uniform(results)
            if self._mode == VisualizationMode.NODE_AVERAGED:
                return self._build_element_2d_shared_nodes(results)
            if self._mode == VisualizationMode.NODE_RAW:
                return self._build_element_2d_isolated_nodes(results)

        raise ValueError(
            f"Unsupported combination of component {self._component!r} "
            f"and mode {self._mode!r}")

    def _require_columns(self,
                         results: pd.DataFrame,
                         columns: tuple[str, ...]) -> None:
        missing = [column for column in columns if column not in results.columns]
        if missing:
            raise ValueError(
                f"Missing expected columns {missing} for component "
                f"{self._component!r} and mode {self._mode!r}")

    def _value_range(self, values: pd.Series) -> tuple[float, float]:
        if values.empty:
            return (0.0, 0.0)
        return (float(values.min()), float(values.max()))

    def _build_node_points(self, results: pd.DataFrame) -> VisualizationData:
        self._require_columns(results, (_NODE_ITEM_COL, _VALUE_COL))

        node_values = {
            str(node_id): float(value)
            for node_id, value in zip(results[_NODE_ITEM_COL],
                                      results[_VALUE_COL])
        }

        return VisualizationData(
            kind=VisualizationContentKind.NODE_POINTS,
            value_range=self._value_range(results[_VALUE_COL]),
            node_values=node_values,
        )

    def _build_element_1d_profile(self,
                                  results: pd.DataFrame) -> VisualizationData:
        self._require_columns(
            results,
            (_ELEMENT_1D_ITEM_COL, _ELEMENT_1D_STATION_COL, _VALUE_COL))

        element_station_values: dict[str, list[tuple[float, float]]] = {}
        for element_id, group in results.groupby(_ELEMENT_1D_ITEM_COL):
            ordered = group.sort_values(_ELEMENT_1D_STATION_COL)
            element_station_values[str(element_id)] = list(
                zip(ordered[_ELEMENT_1D_STATION_COL].astype(float),
                    ordered[_VALUE_COL].astype(float)))

        return VisualizationData(
            kind=VisualizationContentKind.ELEMENT_1D_PROFILE,
            value_range=self._value_range(results[_VALUE_COL]),
            element_station_values=element_station_values,
        )

    def _build_element_2d_uniform(self,
                                  results: pd.DataFrame) -> VisualizationData:
        self._require_columns(results, (_ELEMENT_2D_ITEM_COL, _VALUE_COL))

        element_values = {
            str(element_id): float(value)
            for element_id, value in zip(results[_ELEMENT_2D_ITEM_COL],
                                         results[_VALUE_COL])
        }

        return VisualizationData(
            kind=VisualizationContentKind.ELEMENT_2D_UNIFORM,
            value_range=self._value_range(results[_VALUE_COL]),
            element_values=element_values,
        )

    def _build_element_2d_shared_nodes(self,
                                       results: pd.DataFrame) -> VisualizationData:
        self._require_columns(results, (_ELEMENT_2D_NODE_COL, _VALUE_COL))

        node_values = {
            str(node_id): float(value)
            for node_id, value in zip(results[_ELEMENT_2D_NODE_COL],
                                      results[_VALUE_COL])
        }

        return VisualizationData(
            kind=VisualizationContentKind.ELEMENT_2D_SHARED_NODES,
            value_range=self._value_range(results[_VALUE_COL]),
            node_values=node_values,
        )

    def _build_element_2d_isolated_nodes(self,
                                         results: pd.DataFrame) -> VisualizationData:
        self._require_columns(
            results,
            (_ELEMENT_2D_ITEM_COL, _ELEMENT_2D_NODE_COL, _VALUE_COL))

        element_node_values: dict[str, dict[str, float]] = {}
        for element_id, group in results.groupby(_ELEMENT_2D_ITEM_COL):
            element_node_values[str(element_id)] = {
                str(node_id): float(value)
                for node_id, value in zip(group[_ELEMENT_2D_NODE_COL],
                                          group[_VALUE_COL])
            }

        return VisualizationData(
            kind=VisualizationContentKind.ELEMENT_2D_ISOLATED_NODES,
            value_range=self._value_range(results[_VALUE_COL]),
            element_node_values=element_node_values,
        )
