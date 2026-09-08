from enum import StrEnum


class ModelTables(StrEnum):
    NODES = "nodes_df"
    ELEMENTS_1D = "elements_1d_df"
    ELEMENTS_2D = "elements_2d_df"
    MATERIALS = "materials_df"
    SECTIONS = "sections_df"
    ORIGIN_1D_RESULTS = "origin_1d_results_df"
    ORIGIN_2D_RESULTS = "origin_2d_results_df"
    ORIGIN_NODE_DISPLACEMENTS = "origin_node_displacements_df"
    ORIGIN_NODE_REACTIONS = "origin_node_reactions_df"
    LOAD_CASES = "load_cases_df"


class NodesColumns(StrEnum):
    NODE = "node"
    X = "x"
    Y = "y"
    Z = "z"


class Elements1DColumns(StrEnum):
    ELEMENT = "element"
    NODE_I = "node_i"
    NODE_J = "node_j"
    MATERIAL = "material"
    SECTION = "section"


class Elements2DColumns(StrEnum):
    ELEMENT = "element"
    NODE_1 = "node_1"
    NODE_2 = "node_2"
    NODE_3 = "node_3"
    NODE_4 = "node_4"
    MATERIAL = "material"
    THICKNESS = "thickness"


class MaterialsColumns(StrEnum):
    MATERIAL = "material"
    YOUNG_MODULUS = "young_modulus"
    SHEAR_MODULUS = "shear_modulus"
    POISSON_RATIO = "poisson_ratio"
    THERMAL_COEFF = "thermal_coeff"


class SectionsColumns(StrEnum):
    SECTION = "section"
    AREA = "area"
    INERTIA_22 = "inertia_22"
    INERTIA_33 = "inertia_33"


class Origin1DResultsColumns(StrEnum):
    ELEMENT = "element"
    STATION = "station"
    CASE = "case"
    NORMAL = "normal"
    SHEAR_2 = "shear_2"
    SHEAR_3 = "shear_3"
    TORSION = "torsion"
    BENDING_2 = "bending_2"
    BENDING_3 = "bending_3"


class Origin2DResultsColumns(StrEnum):
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


class OriginNodeDisplacementsColumns(StrEnum):
    NODE = "node"
    CASE = "case"
    DX = "dx"
    DY = "dy"
    DZ = "dz"
    RX = "rx"
    RY = "ry"
    RZ = "rz"


class OriginNodeReactionsColumns(StrEnum):
    NODE = "node"
    CASE = "case"
    FX = "fx"
    FY = "fy"
    FZ = "fz"
    MX = "mx"
    MY = "my"
    MZ = "mz"


class LoadCasesColumns(StrEnum):
    CASE = "case"
    DESCRIPTION = "description"


REQUIRED_MODEL_SCHEMA = {
    ModelTables.NODES: [
        NodesColumns.NODE,
        NodesColumns.X,
        NodesColumns.Y,
        NodesColumns.Z,
    ],
    ModelTables.ELEMENTS_1D: [
        Elements1DColumns.ELEMENT,
        Elements1DColumns.NODE_I,
        Elements1DColumns.NODE_J,
        Elements1DColumns.MATERIAL,
        Elements1DColumns.SECTION,
    ],
    ModelTables.ELEMENTS_2D: [
        Elements2DColumns.ELEMENT,
        Elements2DColumns.NODE_1,
        Elements2DColumns.NODE_2,
        Elements2DColumns.NODE_3,
        Elements2DColumns.NODE_4,
        Elements2DColumns.MATERIAL,
        Elements2DColumns.THICKNESS,
    ],
    ModelTables.MATERIALS: [
        MaterialsColumns.MATERIAL,
        MaterialsColumns.YOUNG_MODULUS,
        MaterialsColumns.SHEAR_MODULUS,
        MaterialsColumns.POISSON_RATIO,
        MaterialsColumns.THERMAL_COEFF,
    ],
    ModelTables.SECTIONS: [
        SectionsColumns.SECTION,
        SectionsColumns.AREA,
        SectionsColumns.INERTIA_22,
        SectionsColumns.INERTIA_33,
    ],
    ModelTables.ORIGIN_1D_RESULTS: [
        Origin1DResultsColumns.ELEMENT,
        Origin1DResultsColumns.STATION,
        Origin1DResultsColumns.CASE,
        Origin1DResultsColumns.NORMAL,
        Origin1DResultsColumns.SHEAR_2,
        Origin1DResultsColumns.SHEAR_3,
        Origin1DResultsColumns.TORSION,
        Origin1DResultsColumns.BENDING_2,
        Origin1DResultsColumns.BENDING_3,
    ],
    ModelTables.ORIGIN_2D_RESULTS: [
        Elements2DColumns.ELEMENT,
        Origin2DResultsColumns.NODE,
        Origin2DResultsColumns.CASE,
        Origin2DResultsColumns.NORMAL_11,
        Origin2DResultsColumns.NORMAL_22,
        Origin2DResultsColumns.NORMAL_12,
        Origin2DResultsColumns.BENDING_11,
        Origin2DResultsColumns.BENDING_22,
        Origin2DResultsColumns.BENDING_12,
        Origin2DResultsColumns.SHEAR_13,
        Origin2DResultsColumns.SHEAR_23,
    ],
    ModelTables.ORIGIN_NODE_DISPLACEMENTS: [
        OriginNodeDisplacementsColumns.NODE,
        OriginNodeDisplacementsColumns.CASE,
        OriginNodeDisplacementsColumns.DX,
        OriginNodeDisplacementsColumns.DY,
        OriginNodeDisplacementsColumns.DZ,
        OriginNodeDisplacementsColumns.RX,
        OriginNodeDisplacementsColumns.RY,
        OriginNodeDisplacementsColumns.RZ,
    ],
    ModelTables.ORIGIN_NODE_REACTIONS: [
        OriginNodeReactionsColumns.NODE,
        OriginNodeReactionsColumns.CASE,
        OriginNodeReactionsColumns.FX,
        OriginNodeReactionsColumns.FY,
        OriginNodeReactionsColumns.FZ,
        OriginNodeReactionsColumns.MX,
        OriginNodeReactionsColumns.MY,
        OriginNodeReactionsColumns.MZ,
    ],
    ModelTables.LOAD_CASES: [
        LoadCasesColumns.CASE,
        LoadCasesColumns.DESCRIPTION,
    ],
}
