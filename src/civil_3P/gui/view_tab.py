from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class ViewTab(Protocol):
    @property
    def identifier(self) -> str: ...

    @property
    def display_name(self) -> str: ...

    def build_content(self, parent: QWidget) -> QWidget: ...
