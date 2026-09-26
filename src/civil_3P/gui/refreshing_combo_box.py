from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QCompleter,
    QWidget,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


class RefreshingComboBox(QComboBox):
    def __init__(
        self,
        options_provider: Callable[[], list[str]],
        placeholder_text: str,
        parent: QWidget,
    ) -> None:
        super().__init__(parent)
        self._options_provider = options_provider
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.setPlaceholderText(placeholder_text)
        self.setMaxVisibleItems(12)

        completer = QCompleter(self.model(), self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setMaxVisibleItems(12)
        completer.popup().setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.setCompleter(completer)
        self.lineEdit().textEdited.connect(self._update_suggestions)
        self.refresh_options()

    def refresh_options(self) -> None:
        current_text = self.currentText()
        options = self._options_provider()
        current_options = [
            self.itemText(index) for index in range(self.count())
        ]

        if options == current_options:
            return

        was_blocked = self.blockSignals(True)
        try:
            self.clear()
            self.addItems(options)
            current_index = self.findText(
                current_text,
                Qt.MatchFlag.MatchFixedString,
            )
            if current_index >= 0:
                self.setCurrentIndex(current_index)
            else:
                self.setCurrentIndex(-1)
                self.setEditText(current_text)
        finally:
            self.blockSignals(was_blocked)

    def showPopup(self) -> None:
        self.refresh_options()
        super().showPopup()

    def _update_suggestions(self, text: str) -> None:
        completer = self.completer()
        if completer is None:
            return

        completer.setCompletionPrefix(text)
        if text and completer.completionCount() > 0:
            completer.complete()
        else:
            completer.popup().hide()
