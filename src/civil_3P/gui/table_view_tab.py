from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QLabel

from civil_3P.standard.gui_texts import GuiLabels

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class TableViewTab:
    identifier = "tabela"
    display_name = GuiLabels.TABLE_TAB

    def build_content(self, parent: QWidget) -> QWidget:
        return QLabel(GuiLabels.TABLE_UNDER_CONSTRUCTION, parent)
