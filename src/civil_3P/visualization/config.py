from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from civil_3P.utils.colors import Colors


@dataclass
class SceneViewerConfig:
    background_color: str = Colors.WHITE
    element_1d_color: str = Colors.BLUE
    element_2d_color: str = Colors.LIGHTGRAY
    edge_color: str = Colors.GRAY
    node_color: str = Colors.RED
    element_1d_line_width: float = 2.0
    element_2d_line_width: float = 1.0
    node_point_size: float = 3.5
    n_bands: int = 10
    colormap: str = "jet"
    result_node_point_size: float = 6.0
    result_element_1d_line_width: float = 4.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, values: dict[str, Any]) -> SceneViewerConfig:
        defaults = cls().to_dict()
        defaults.update(values)
        return cls(**defaults)
