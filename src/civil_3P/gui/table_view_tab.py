from __future__ import annotations

from PySide6.QtWidgets import QLabel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class TableViewTab:
    identifier = "tabela"
    display_name = "Tabela"

    def build_content(self, parent: QWidget) -> QWidget:
        return QLabel("Tabela (em construção)", parent)
