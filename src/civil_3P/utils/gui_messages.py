from __future__ import annotations

from PySide6.QtWidgets import QMessageBox
from typing import TYPE_CHECKING

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
            "Civil 3P",
            message,
        )

    @staticmethod
    def display_warning(
        panel: QWidget,
        message: str,
    ) -> None:
        QMessageBox.warning(
            panel,
            "Civil 3P",
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
        msgbox.setWindowTitle("Civil 3P")
        msgbox.setText(message)

        if detailed_message:
            msgbox.setDetailedText(detailed_message)
            
        msgbox.exec()
