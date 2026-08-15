from __future__ import annotations

import pandas as pd

from civil_3P.core.model import FEMModel
from civil_3P.visualization.scene import VisualizationBuilder


def test_visualization_service_builds_scene_data() -> None:
    model = FEMModel.empty()
    model.nodes_df = pd.DataFrame([
        {"node_id": "N1", "x": 0.0, "y": 0.0, "z": 0.0},
        {"node_id": "N2", "x": 1.0, "y": 0.0, "z": 0.0},
        {"node_id": "N3", "x": 1.0, "y": 1.0, "z": 0.0},
    ])
    model.elements_1d_df = pd.DataFrame([
        {"element_id": "B1", "node_i": "N1", "node_j": "N2",
            "material_id": "S", "section_id": "A"},
    ])
    model.elements_2d_df = pd.DataFrame([
        {"element_id": "P1", "node_1": "N1", "node_2": "N2", "node_3": "N3",
            "node_4": "N1", "material_id": "C", "thickness": 0.2},
    ])

    scene = VisualizationBuilder().build_scene(model)

    assert scene["nodes"]["N1"]["x"] == 0.0
    assert scene["bars"]["B1"]["start"] == "N1"
    assert scene["shells"]["P1"]["nodes"] == ["N1", "N2", "N3", "N1"]


def test_visualization_service_handles_triangular_shells() -> None:
    model = FEMModel.empty()
    model.nodes_df = pd.DataFrame([
        {"node_id": "N1", "x": 0.0, "y": 0.0, "z": 0.0},
        {"node_id": "N2", "x": 1.0, "y": 0.0, "z": 0.0},
        {"node_id": "N3", "x": 0.0, "y": 1.0, "z": 0.0},
    ])
    model.elements_2d_df = pd.DataFrame([
        {"element_id": "T1", "node_1": "N1", "node_2": "N2", "node_3": "N3",
            "node_4": None, "material_id": "C", "thickness": 0.2},
    ])

    scene = VisualizationBuilder().build_scene(model)

    shell = scene["shells"]["T1"]
    assert shell["nodes"] == ["N1", "N2", "N3"]
