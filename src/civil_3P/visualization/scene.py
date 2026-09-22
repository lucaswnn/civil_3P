from dataclasses import dataclass

from civil_3P.visualization.result_view_data import ResultViewData
from civil_3P.visualization.model_view_data import ModelViewData

@dataclass(frozen=True, slots=True)
class Scene:
    node_map: dict[str, int]
    model_view: ModelViewData
    result_view: ResultViewData | None = None