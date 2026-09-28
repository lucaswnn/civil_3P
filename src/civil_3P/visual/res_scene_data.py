from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.standard.res_components import ResSceneKind
    from civil_3P.visual.res_element_scene_data import ResElementSceneData


@dataclass(frozen=True, slots=True)
class ResSceneData:
    kind: ResSceneKind
    value_range: tuple[float, float]
    data: ResElementSceneData

    def __repr__(self):
        return (
            f"ResSceneData\n" f"Kind: {self.kind}\n" f"Value range: {self.value_range}"
        )
