from __future__ import annotations

from typing import Protocol

from PySide6.QtWidgets import QWidget


class ViewTab(Protocol):
    @property
    def identifier(self) -> str: ...

    @property
    def display_name(self) -> str: ...

    def build_content(self, parent: QWidget) -> QWidget: ...


class ViewTabRegistry:
    def __init__(self, tabs: list[ViewTab]) -> None:
        self._tabs: dict[str, ViewTab] = {tab.identifier: tab for tab in tabs}

    def get(self, identifier: str) -> ViewTab:
        return self._tabs[identifier]

    def all(self) -> tuple[ViewTab, ...]:
        return tuple(self._tabs.values())
