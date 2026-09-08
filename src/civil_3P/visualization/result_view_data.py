from dataclasses import dataclass, field
from civil_3P.standard.result_components import ViewContentKind
import numpy as np

@dataclass(frozen=True, slots=True)
class ResultElementViewData:
    nodes: np.ndarray
    values: np.ndarray
    connection: np.ndarray | None = None
    element_type: np.ndarray | None = None


@dataclass(frozen=True, slots=True)
class ResultViewData:
    kind: ViewContentKind
    value_range: tuple[float, float]
    data: ResultElementViewData
