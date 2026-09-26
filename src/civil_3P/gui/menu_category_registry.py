from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.gui.menu_category import MenuCategory


class MenuCategoryRegistry:
    def __init__(self, categories: list[MenuCategory]) -> None:
        self._categories: dict[str, MenuCategory] = {
            category.identifier: category for category in categories
        }

    def get(self, identifier: str) -> MenuCategory:
        return self._categories[identifier]

    def all(self) -> tuple[MenuCategory, ...]:
        return tuple(self._categories.values())
