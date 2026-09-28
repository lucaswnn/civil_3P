from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.visual.model_scene_data import ModelSceneData
    from civil_3P.visual.res_scene_data import ResSceneData


@dataclass(frozen=True, slots=True)
class Scene:
    node_map: dict[str, int]
    model_view: ModelSceneData
    res_view: ResSceneData | None = None

    def __repr__(self):
        return f"{self.model_view}\n-----\n{self.res_view}"
