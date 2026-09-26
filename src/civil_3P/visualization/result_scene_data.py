from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.standard.result_components import ViewContentKind
    from civil_3P.visualization.result_element_scene_data import (
        ResultElementSceneData
    )


@dataclass(frozen=True, slots=True)
class ResultSceneData:
    kind: ViewContentKind
    value_range: tuple[float, float]
    data: ResultElementSceneData

    def __repr__(self):
        return (
            f"ResultViewData\n"
            f"Kind: {self.kind}\n"
            f"Value range: {self.value_range}"
        )
