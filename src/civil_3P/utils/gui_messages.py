from __future__ import annotations

from PySide6.QtWidgets import QMessageBox
from typing import TYPE_CHECKING

from civil_3P.standard.gui_texts import GuiLabels

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class GuiMessages:
    @staticmethod
    def display_info(
        panel: QWidget,
        message: str,
    ) -> None:
        QMessageBox.information(
            panel,
            GuiLabels.APPLICATION_NAME,
            message,
        )

    @staticmethod
    def display_warning(
        panel: QWidget,
        message: str,
    ) -> None:
        QMessageBox.warning(
            panel,
            GuiLabels.APPLICATION_NAME,
            message,
        )

    @staticmethod
    def display_error(
        panel: QWidget,
        message: str,
        detailed_message: str | None = None,
    ) -> None:
        msgbox = QMessageBox(panel)
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setWindowTitle(GuiLabels.APPLICATION_NAME)
        msgbox.setText(message)

        if detailed_message:
            msgbox.setDetailedText(detailed_message)
            
        msgbox.exec()
