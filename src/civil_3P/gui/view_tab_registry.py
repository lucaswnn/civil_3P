from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.gui.view_tab import ViewTab


class ViewTabRegistry:
    def __init__(self, tabs: list[ViewTab]) -> None:
        self._tabs: dict[str, ViewTab] = {
            tab.identifier: tab
            for tab in tabs
        }

    def get(self, identifier: str) -> ViewTab:
        return self._tabs[identifier]

    def all(self) -> tuple[ViewTab, ...]:
        return tuple(self._tabs.values())
