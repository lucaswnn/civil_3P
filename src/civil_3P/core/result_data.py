from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

@dataclass(frozen=True, slots=True)
class ResultData:
    element_type: str
    result_df: pd.DataFrame
    elements: set[str]
    nodes: set[str]