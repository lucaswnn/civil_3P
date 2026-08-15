from __future__ import annotations

from typing import Any
import pandas as pd

from civil_3P.core.model import FEMModel
from civil_3P.standard import model_representation as rpr
from civil_3P.standard import model_components as mc


class VisualizationBuilder:
    def build_scene(self, model: FEMModel) -> dict[str, dict[str, dict[str, Any]]]:
        nodes = self._build_nodes(model.tables_dict[rpr.ModelTables.NODES])
        bars = self._build_bars(model.tables_dict[rpr.ModelTables.ELEMENTS_1D])
        shells = self._build_shells(
            model.tables_dict[rpr.ModelTables.ELEMENTS_2D])

        return {
            mc.ModelComponents.NODES: nodes,
            mc.ModelComponents.ELEMENTS_1D: bars,
            mc.ModelComponents.ELEMENTS_2D: shells,
        }

    def _build_nodes(self, nodes: pd.DataFrame) -> dict[str, dict[str, Any]]:
        return {
            str(getattr(row, rpr.NodesColumns.NODE)): {
                mc.ModelNodeComponents.NODE_X: float(getattr(row, rpr.NodesColumns.X)),
                mc.ModelNodeComponents.NODE_Y: float(getattr(row, rpr.NodesColumns.Y)),
                mc.ModelNodeComponents.NODE_Z: float(getattr(row, rpr.NodesColumns.Z)),
            }
            for row in nodes.itertuples(index=False)
        }

    def _build_bars(
        self,
        elements_1d: pd.DataFrame,
    ) -> dict[str, dict[str, Any]]:
        return {
            str(getattr(row, rpr.Elements1DColumns.ELEMENT)): {
                mc.ModelElement1DComponents.ELEMENT_1D_START_NODE: str(getattr(row, rpr.Elements1DColumns.NODE_I)),
                mc.ModelElement1DComponents.ELEMENT_1D_END_NODE: str(getattr(row, rpr.Elements1DColumns.NODE_J)),
            }
            for row in elements_1d.itertuples(index=False)
        }

    def _build_shells(
        self,
        elements_2d: pd.DataFrame,
    ) -> dict[str, dict[str, Any]]:
        return {
            str(getattr(row, rpr.Elements2DColumns.ELEMENT)): {
                mc.ModelElement2DComponents.ELEMENT_2D_NODES: [
                    str(node_id)
                    for node_id in [
                        getattr(row, rpr.Elements2DColumns.NODE_1, None),
                        getattr(row, rpr.Elements2DColumns.NODE_2, None),
                        getattr(row, rpr.Elements2DColumns.NODE_3, None),
                        getattr(row, rpr.Elements2DColumns.NODE_4, None),
                    ]
                    if not pd.isna(node_id)
                ],
            }
            for row in elements_2d.itertuples(index=False)
        }
