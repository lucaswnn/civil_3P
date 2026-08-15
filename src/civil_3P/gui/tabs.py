from __future__ import annotations

from typing import Protocol, Sequence

from PySide6.QtWidgets import QLabel, QWidget

from civil_3P.visualization.widget import SceneWidget


class ViewTab(Protocol):
    @property
    def identifier(self) -> str: ...

    @property
    def display_name(self) -> str: ...

    def build_content(self, parent: QWidget) -> QWidget: ...


class ModeloViewTab:
    identifier = "modelo"
    display_name = "Modelo"

    def __init__(self, scene_widget: SceneWidget) -> None:
        self._scene_widget = scene_widget

    def build_content(self, parent: QWidget) -> QWidget:
        return self._scene_widget


class TabelaViewTab:
    identifier = "tabela"
    display_name = "Tabela"

    def build_content(self, parent: QWidget) -> QWidget:
        return QLabel("Tabela (em construção)", parent)


class ViewTabRegistry:
    def __init__(self, tabs: Sequence[ViewTab]) -> None:
        self._tabs: dict[str, ViewTab] = {tab.identifier: tab for tab in tabs}

    def get(self, identifier: str) -> ViewTab:
        return self._tabs[identifier]

    def all(self) -> tuple[ViewTab, ...]:
        return tuple(self._tabs.values())
