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
    TASK_1D_RESULTS = "task_1d_results_df"
    TASK_2D_RESULTS = "task_2d_results_df"
    TASK_NODE_RESULTS = "task_node_results_df"

REQUIRED_TABLES = {table.value for table in ModelTables}


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

class Task1DResultsColumns(StrEnum):
    ELEMENT = "element"
    STATION = "station"
    CASE = "case"
    VALUE = "value"

class Task2DResultsColumns(StrEnum):
    ELEMENT = "element"
    NODE = "node"
    CASE = "case"
    VALUE = "value"

class TaskNodeResultsColumns(StrEnum):
    NODE = "node"
    CASE = "case"
    VALUE = "value"