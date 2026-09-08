from PySide6.QtWidgets import QLabel, QWidget

class TableViewTab:
    identifier = "tabela"
    display_name = "Tabela"

    def build_content(self, parent: QWidget) -> QWidget:
        return QLabel("Tabela (em construção)", parent)