from __future__ import annotations

from enum import StrEnum


class ModelTables(StrEnum):
    NODES = "nodes_df"
    BARS = "bars_df"
    SHELLS = "shells_df"
    MATERIALS = "materials_df"
    SECTIONS = "sections_df"
    BAR_RESULTS = "bar_results_df"
    SHELL_RESULTS = "shell_results_df"
    NODE_DISPLACEMENTS = "node_displacements_df"
    NODE_REACTIONS = "node_reactions_df"
    LOAD_CASES = "load_cases_df"


class NodeCols(StrEnum):
    NODE = "node"
    X = "x"
    Y = "y"
    Z = "z"


class BarCols(StrEnum):
    ELEMENT = "element"
    NODE_I = "node_i"
    NODE_J = "node_j"
    MATERIAL = "material"
    SECTION = "section"


class ShellCols(StrEnum):
    ELEMENT = "element"
    NODE_1 = "node_1"
    NODE_2 = "node_2"
    NODE_3 = "node_3"
    NODE_4 = "node_4"
    MATERIAL = "material"
    THICKNESS = "thickness"


class MaterialsCols(StrEnum):
    MATERIAL = "material"
    YOUNG_MODULUS = "young_modulus"
    SHEAR_MODULUS = "shear_modulus"
    POISSON_RATIO = "poisson_ratio"
    THERMAL_COEFF = "thermal_coeff"


class SectionsCols(StrEnum):
    SECTION = "section"
    AREA = "area"
    INERTIA_22 = "inertia_22"
    INERTIA_33 = "inertia_33"


class BarResCols(StrEnum):
    ELEMENT = "element"
    STATION = "station"
    CASE = "case"
    NORMAL = "normal"
    SHEAR_2 = "shear_2"
    SHEAR_3 = "shear_3"
    TORSION = "torsion"
    BENDING_2 = "bending_2"
    BENDING_3 = "bending_3"


class ShellResCols(StrEnum):
    ELEMENT = "element"
    NODE = "node"
    CASE = "case"
    NORMAL_11 = "normal_11"
    NORMAL_22 = "normal_22"
    NORMAL_12 = "normal_12"
    BENDING_11 = "bending_11"
    BENDING_22 = "bending_22"
    BENDING_12 = "bending_12"
    SHEAR_13 = "shear_13"
    SHEAR_23 = "shear_23"


class NodeDisplacementsCols(StrEnum):
    NODE = "node"
    CASE = "case"
    DX = "dx"
    DY = "dy"
    DZ = "dz"
    RX = "rx"
    RY = "ry"
    RZ = "rz"


class NodeReactionsCols(StrEnum):
    NODE = "node"
    CASE = "case"
    FX = "fx"
    FY = "fy"
    FZ = "fz"
    MX = "mx"
    MY = "my"
    MZ = "mz"


class LoadCaseCols(StrEnum):
    CASE = "case"
    DESCRIPTION = "description"


REQUIRED_MODEL_SCHEMA = {
    ModelTables.NODES: [
        NodeCols.NODE,
        NodeCols.X,
        NodeCols.Y,
        NodeCols.Z,
    ],
    ModelTables.BARS: [
        BarCols.ELEMENT,
        BarCols.NODE_I,
        BarCols.NODE_J,
        BarCols.MATERIAL,
        BarCols.SECTION,
    ],
    ModelTables.SHELLS: [
        ShellCols.ELEMENT,
        ShellCols.NODE_1,
        ShellCols.NODE_2,
        ShellCols.NODE_3,
        ShellCols.NODE_4,
        ShellCols.MATERIAL,
        ShellCols.THICKNESS,
    ],
    ModelTables.MATERIALS: [
        MaterialsCols.MATERIAL,
        MaterialsCols.YOUNG_MODULUS,
        MaterialsCols.SHEAR_MODULUS,
        MaterialsCols.POISSON_RATIO,
        MaterialsCols.THERMAL_COEFF,
    ],
    ModelTables.SECTIONS: [
        SectionsCols.SECTION,
        SectionsCols.AREA,
        SectionsCols.INERTIA_22,
        SectionsCols.INERTIA_33,
    ],
    ModelTables.BAR_RESULTS: [
        BarResCols.ELEMENT,
        BarResCols.STATION,
        BarResCols.CASE,
        BarResCols.NORMAL,
        BarResCols.SHEAR_2,
        BarResCols.SHEAR_3,
        BarResCols.TORSION,
        BarResCols.BENDING_2,
        BarResCols.BENDING_3,
    ],
    ModelTables.SHELL_RESULTS: [
        ShellCols.ELEMENT,
        ShellResCols.NODE,
        ShellResCols.CASE,
        ShellResCols.NORMAL_11,
        ShellResCols.NORMAL_22,
        ShellResCols.NORMAL_12,
        ShellResCols.BENDING_11,
        ShellResCols.BENDING_22,
        ShellResCols.BENDING_12,
        ShellResCols.SHEAR_13,
        ShellResCols.SHEAR_23,
    ],
    ModelTables.NODE_DISPLACEMENTS: [
        NodeDisplacementsCols.NODE,
        NodeDisplacementsCols.CASE,
        NodeDisplacementsCols.DX,
        NodeDisplacementsCols.DY,
        NodeDisplacementsCols.DZ,
        NodeDisplacementsCols.RX,
        NodeDisplacementsCols.RY,
        NodeDisplacementsCols.RZ,
    ],
    ModelTables.NODE_REACTIONS: [
        NodeReactionsCols.NODE,
        NodeReactionsCols.CASE,
        NodeReactionsCols.FX,
        NodeReactionsCols.FY,
        NodeReactionsCols.FZ,
        NodeReactionsCols.MX,
        NodeReactionsCols.MY,
        NodeReactionsCols.MZ,
    ],
    ModelTables.LOAD_CASES: [
        LoadCaseCols.CASE,
        LoadCaseCols.DESCRIPTION,
    ],
}
