from dataclasses import dataclass, field
from civil_3P.standard.result_components import ViewContentKind
import numpy as np


@dataclass(frozen=True, slots=True)
class ResultElementSceneData:
    nodes: np.ndarray
    values: np.ndarray | None = None
    connection: np.ndarray | None = None
    element_type: np.ndarray | None = None
    block_data: list[tuple[np.ndarray, list[int], np.ndarray]] | None = None


@dataclass(frozen=True, slots=True)
class ResultSceneData:
    kind: ViewContentKind
    value_range: tuple[float, float]
    data: ResultElementSceneData

    def __repr__(self):
        return f"ResultViewData\nKind: {self.kind}\nValue range: {self.value_range}"
