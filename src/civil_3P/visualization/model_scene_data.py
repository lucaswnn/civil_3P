from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


@dataclass(frozen=True, slots=True)
class ModelSceneData:
    nodes: np.ndarray
    elements_1d_connection: np.ndarray
    elements_1d_type: np.ndarray
    elements_2d_connection: np.ndarray
    elements_2d_type: np.ndarray

    def __repr__(self):
        return f"ModelViewData:\n{len(self.nodes)} nodes"
