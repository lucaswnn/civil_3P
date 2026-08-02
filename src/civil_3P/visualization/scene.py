from __future__ import annotations

from typing import Any
import numpy as np

import pandas as pd

from civil_3P.core.model import FEMModel


class VisualizationService:
    def build_scene(self, model: FEMModel) -> dict[str, dict[str, dict[str, Any]]]:
        nodes = self._build_nodes(model.nodes)
        bars = self._build_bars(model.elements_1d)
        shells = self._build_shells(model.elements_2d)

        return {
            "nodes": nodes,
            "bars": bars,
            "shells": shells,
        }

    def _build_nodes(self, nodes: pd.DataFrame) -> dict[str, dict[str, Any]]:
        return {
            str(row.node_id): 
            {
                "x": float(row.x),
                "y": float(row.y),
                "z": float(row.z),
            }
            for row in nodes.itertuples(index=False)
        }

    def _build_bars(
        self,
        elements_1d: pd.DataFrame,
    ) -> dict[str, dict[str, Any]]:
        return {
            str(row.element_id): {
                "start": str(row.node_i),
                "end": str(row.node_j),
            }
            for row in elements_1d.itertuples(index=False)
        }

    def _build_shells(
        self,
        elements_2d: pd.DataFrame,
    ) -> dict[str, dict[str, Any]]:
        return {
            str(row.element_id): {
                "nodes": [
                    str(node_id)
                    for node_id in [
                        getattr(row, "node_1", None),
                        getattr(row, "node_2", None),
                        getattr(row, "node_3", None),
                        getattr(row, "node_4", None),
                    ]
                    if node_id not in (None, "", np.nan)
                ],
            }
            for row in elements_2d.itertuples(index=False)
        }
