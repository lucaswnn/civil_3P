from PySide6.QtWidgets import QWidget
from civil_3P.gui.scene_widget import SceneWidget


class ModelViewTab:
    identifier = "modelo"
    display_name = "Modelo"

    def __init__(self, scene_widget: SceneWidget) -> None:
        self._scene_widget = scene_widget

    def build_content(self, parent: QWidget) -> QWidget:
        return self._scene_widget