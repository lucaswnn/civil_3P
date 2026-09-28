from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


@dataclass(frozen=True, slots=True)
class ModelSceneData:
    nodes: np.ndarray
    bars_connection: np.ndarray
    bars_type: np.ndarray
    shells_connection: np.ndarray
    shells_type: np.ndarray

    def __repr__(self):
        return f"ModelSceneData:\n{len(self.nodes)} nodes"
