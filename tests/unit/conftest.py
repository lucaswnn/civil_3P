from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from civil_3P.core.model import Model
from civil_3P.core.selection_context import SelectionContext
from civil_3P.standard.model_representation import Elements1DColumns as rpr_1d
from civil_3P.standard.model_representation import Elements2DColumns as rpr_2d
from civil_3P.standard.model_representation import LoadCasesColumns as rpr_lc
from civil_3P.standard.model_representation import MaterialsColumns as rpr_mat
from civil_3P.standard.model_representation import ModelTables as mt
from civil_3P.standard.model_representation import NodesColumns as rpr_node
from civil_3P.standard.model_representation import Origin1DResultsColumns as rpr_o1d
from civil_3P.standard.model_representation import Origin2DResultsColumns as rpr_o2d
from civil_3P.standard.model_representation import (
    OriginNodeDisplacementsColumns as rpr_ond,
)
from civil_3P.standard.model_representation import OriginNodeReactionsColumns as rpr_onr
from civil_3P.standard.model_representation import SectionsColumns as rpr_sec
from civil_3P.standard.units import DEFAULT_UNITS


def build_small_model() -> Model:
    """
    Model with 5 nodes, 1 frame (1D), 1 triangle (2D)
    and 1 quad (2D), 2 load cases.
    """
    nodes = pd.DataFrame(
        {
            rpr_node.NODE: ["N1", "N2", "N3", "N4", "N5"],
            rpr_node.X: [0.0, 1.0, 1.0, 0.0, 1.5],
            rpr_node.Y: [0.0, 0.0, 1.0, 1.0, 0.5],
            rpr_node.Z: [0.0, 0.0, 0.0, 0.0, 0.0],
        }
    )
    elements_1d = pd.DataFrame(
        {
            rpr_1d.ELEMENT: ["F1"],
            rpr_1d.NODE_I: ["N1"],
            rpr_1d.NODE_J: ["N2"],
            rpr_1d.MATERIAL: ["Concrete"],
            rpr_1d.SECTION: ["S1"],
        }
    )
    elements_2d = pd.DataFrame(
        {
            rpr_2d.ELEMENT: ["A1", "A2"],
            rpr_2d.NODE_1: ["N1", "N2"],
            rpr_2d.NODE_2: ["N2", "N3"],
            rpr_2d.NODE_3: ["N3", "N5"],
            rpr_2d.NODE_4: ["N4", np.nan],
            rpr_2d.MATERIAL: ["Concrete", "Concrete"],
            rpr_2d.THICKNESS: [0.2, 0.2],
        }
    )
    materials = pd.DataFrame(
        {
            rpr_mat.MATERIAL: ["Concrete"],
            rpr_mat.YOUNG_MODULUS: [30000.0],
            rpr_mat.SHEAR_MODULUS: [12500.0],
            rpr_mat.POISSON_RATIO: [0.2],
            rpr_mat.THERMAL_COEFF: [1e-5],
        }
    )
    sections = pd.DataFrame(
        {
            rpr_sec.SECTION: ["S1"],
            rpr_sec.AREA: [0.09],
            rpr_sec.INERTIA_22: [0.001],
            rpr_sec.INERTIA_33: [0.001],
        }
    )
    origin_1d_results = pd.DataFrame(
        {
            rpr_o1d.ELEMENT: ["F1", "F1"],
            rpr_o1d.STATION: [0.0, 1.0],
            rpr_o1d.CASE: ["DEAD", "DEAD"],
            rpr_o1d.NORMAL: [10.0, 10.0],
            rpr_o1d.SHEAR_2: [0.0, 0.0],
            rpr_o1d.SHEAR_3: [1.0, 1.0],
            rpr_o1d.TORSION: [0.0, 0.0],
            rpr_o1d.BENDING_2: [0.0, 0.0],
            rpr_o1d.BENDING_3: [5.0, -5.0],
        }
    )
    origin_2d_results = pd.DataFrame(
        {
            rpr_o2d.ELEMENT: ["A1", "A1", "A1", "A1", "A2", "A2", "A2"],
            rpr_o2d.NODE: ["N1", "N2", "N3", "N4", "N2", "N3", "N5"],
            rpr_o2d.CASE: ["DEAD", "DEAD", "DEAD", "DEAD", "DEAD", "DEAD", "DEAD"],
            rpr_o2d.NORMAL_11: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            rpr_o2d.NORMAL_22: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            rpr_o2d.NORMAL_12: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            rpr_o2d.BENDING_11: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            rpr_o2d.BENDING_22: [2.0, 3.0, 4.0, 5.0, 2.0, 3.0, 4.0],
            rpr_o2d.BENDING_12: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            rpr_o2d.SHEAR_13: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            rpr_o2d.SHEAR_23: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        }
    )
    origin_node_displacements = pd.DataFrame(
        {
            rpr_ond.NODE: ["N1", "N2", "N3", "N4", "N5"],
            rpr_ond.CASE: ["DEAD", "DEAD", "DEAD", "DEAD", "DEAD"],
            rpr_ond.DX: [0.0, 0.0, 0.0, 0.0, 0.01],
            rpr_ond.DY: [0.0, 0.0, 0.0, 0.0, 0.01],
            rpr_ond.DZ: [0.0, 0.0, 0.0, 0.0, 0.01],
            rpr_ond.RX: [0.0, 0.0, 0.0, 0.0, 0.01],
            rpr_ond.RY: [0.0, 0.0, 0.0, 0.0, 0.01],
            rpr_ond.RZ: [0.0, 0.0, 0.0, 0.0, 0.01],
        }
    )
    origin_node_reactions = pd.DataFrame(
        {
            rpr_onr.NODE: ["N1"],
            rpr_onr.CASE: ["DEAD"],
            rpr_onr.FX: [0.0],
            rpr_onr.FY: [0.0],
            rpr_onr.FZ: [10.0],
            rpr_onr.MX: [0.0],
            rpr_onr.MY: [0.0],
            rpr_onr.MZ: [0.0],
        }
    )
    load_cases = pd.DataFrame(
        {
            rpr_lc.CASE: ["DEAD", "LIVE"],
            rpr_lc.DESCRIPTION: ["", ""],
        }
    )

    tables = {
        mt.NODES: nodes,
        mt.ELEMENTS_1D: elements_1d,
        mt.ELEMENTS_2D: elements_2d,
        mt.MATERIALS: materials,
        mt.SECTIONS: sections,
        mt.ORIGIN_1D_RESULTS: origin_1d_results,
        mt.ORIGIN_2D_RESULTS: origin_2d_results,
        mt.ORIGIN_NODE_DISPLACEMENTS: origin_node_displacements,
        mt.ORIGIN_NODE_REACTIONS: origin_node_reactions,
        mt.LOAD_CASES: load_cases,
    }

    return Model.from_tables(tables=tables, units=DEFAULT_UNITS.copy())


@pytest.fixture
def small_model() -> Model:
    return build_small_model()


@pytest.fixture
def full_selection() -> SelectionContext:
    return SelectionContext(
        node_ids={"N1", "N2", "N3", "N4"},
        element_1d_ids={"F1"},
        element_2d_ids={"A1"},
    )
