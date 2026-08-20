from __future__ import annotations

from typing import Protocol, Sequence

from PySide6.QtWidgets import QWidget


class MenuCategory(Protocol):
    @property
    def identifier(self) -> str: ...

    @property
    def display_name(self) -> str: ...

    def build_panel(self, parent: QWidget) -> QWidget: ...


class MenuCategoryRegistry:
    def __init__(self, categories: Sequence[MenuCategory]) -> None:
        self._categories: dict[str, MenuCategory] = {
            category.identifier: category for category in categories
        }

    def get(self, identifier: str) -> MenuCategory:
        return self._categories[identifier]

    def all(self) -> tuple[MenuCategory, ...]:
        return tuple(self._categories.values())
