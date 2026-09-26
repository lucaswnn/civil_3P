from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from civil_3P.standard.file_representation import (
    FileRepresentation as fr
)
from civil_3P.visualization.scene_viewer_config import SceneViewerConfig

if TYPE_CHECKING:
    from typing import Any


@dataclass(frozen=True, slots=True)
class UserPreferences:
    plugins_base_path: Path
    scene_viewer_config: SceneViewerConfig

    @classmethod
    def from_snapshot(
        cls,
        snapshot: dict[str, Any],
    ) -> UserPreferences:
        plugins_base_path = Path(
            snapshot.get(fr.PLUGINS_BASE_PATH)
        )
        scene_viewer_config_data = snapshot.get(
            fr.SCENE_VIEWER_CONFIG
        )
        scene_viewer_config = SceneViewerConfig.from_dict(
            scene_viewer_config_data
        )

        return cls(
            plugins_base_path=plugins_base_path,
            scene_viewer_config=scene_viewer_config
        )
