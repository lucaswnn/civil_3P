from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


@dataclass(frozen=True, slots=True)
class ResData:
    element_type: str
    res_df: pd.DataFrame
    elements: set[str]
    nodes: set[str]

    def __repr__(self):
        return (
            "ResData\n"
            f"Element type: {self.element_type}\n"
            f"Element count: {len(self.elements)}\n"
            f"Node count: {len(self.nodes)}"
        )
