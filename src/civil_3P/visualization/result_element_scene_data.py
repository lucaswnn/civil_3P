from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


@dataclass(frozen=True, slots=True)
class ResultElementSceneData:
    nodes: np.ndarray
    values: np.ndarray | None = None
    connection: np.ndarray | None = None
    element_type: np.ndarray | None = None
    block_data: list[tuple[np.ndarray, list[int], np.ndarray]] | None = None
