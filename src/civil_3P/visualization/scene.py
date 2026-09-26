from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.visualization.result_scene_data import (
        ResultSceneData
    )
    from civil_3P.visualization.model_scene_data import (
        ModelSceneData
    )


@dataclass(frozen=True, slots=True)
class Scene:
    node_map: dict[str, int]
    model_view: ModelSceneData
    result_view: ResultSceneData | None = None

    def __repr__(self):
        return f"{self.model_view}\n-----\n{self.result_view}"
