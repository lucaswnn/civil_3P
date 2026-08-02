from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from civil_3P.core.enums import ElementType, VisualizationMode
from civil_3P.core.results import VisualizationCriteria
from civil_3P.importers.csv_importers import CsvImportProfile
from civil_3P.gui import AppController
from civil_3P.visualization.scene import VisualizationService
from civil_3P.visualization.widget import SceneWidget

if TYPE_CHECKING:
    from civil_3P.gui.controller import AppController


class MainWindow(QMainWindow):
    def __init__(self,
                 controller: "AppController") -> None:
        super().__init__()
        self._controller = controller
        self._model = None
        self._scene_service = VisualizationService()
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWindowTitle("civil_3P")
        self.resize(900, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        form_layout = QFormLayout()
        self._directory_edit = QLineEdit()
        self._directory_edit.setPlaceholderText(
            "Caminho para a pasta com os CSVs"
        )

        browse_button = QPushButton("Procurar")
        browse_button.clicked.connect(self._browse_directory)

        directory_row = QHBoxLayout()
        directory_row.addWidget(self._directory_edit)
        directory_row.addWidget(browse_button)
        form_layout.addRow(QLabel("Diretório"), directory_row)

        self._case_edit = QLineEdit("LC1")
        self._element_edit = QLineEdit("B1")
        self._task_combo = QLineEdit("example_bar_check")

        form_layout.addRow(QLabel("Caso"), self._case_edit)
        form_layout.addRow(QLabel("Elemento"), self._element_edit)
        form_layout.addRow(QLabel("Tarefa"), self._task_combo)

        load_button = QPushButton("Carregar modelo")
        load_button.clicked.connect(self._load_model)
        run_button = QPushButton("Executar tarefa")
        run_button.clicked.connect(self._run_task)

        button_row = QHBoxLayout()
        button_row.addWidget(load_button)
        button_row.addWidget(run_button)
        form_layout.addRow(button_row)

        layout.addLayout(form_layout)

        self._scene_widget = SceneWidget(self)
        self._scene_widget.setMinimumHeight(220)
        layout.addWidget(self._scene_widget)

        self._table = QTableWidget()
        self._table.setAlternatingRowColors(True)
        layout.addWidget(self._table)

    def _browse_directory(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self,
            "Selecionar pasta com os CSVs",
            str(Path.cwd())
        )

        if directory:
            self._directory_edit.setText(directory)

    def _load_model(self) -> None:
        directory = self._directory_edit.text().strip()
        if not directory:
            QMessageBox.warning(self,
                                "civil_3P",
                                "Selecione um diretório primeiro.")

            return

        try:
            self._model = self._controller.import_model(
                CsvImportProfile.SAP2000,
                Path(directory),
            )
            
            self._scene_widget.set_scene(
                self._scene_service.build_scene(self._model)
            )

            QMessageBox.information(self,
                                    "civil_3P",
                                    "Modelo carregado com sucesso.")

        except Exception as exc:  # pragma: no cover - runtime feedback only
            QMessageBox.critical(self,
                                 "civil_3P",
                                 f"Falha ao carregar o modelo: {exc}")

    def _run_task(self) -> None:
        if self._model is None:
            QMessageBox.warning(
                self,
                "civil_3P",
                "Carregue um modelo antes de executar uma tarefa."
            )

            return

        task_id = self._task_combo.text().strip()
        case_id = self._case_edit.text().strip() or "LC1"
        element_id = self._element_edit.text().strip() or "B1"

        try:
            if task_id == "example_bar_check":
                selection = self._controller.create_selection(
                    ElementType.BAR_1D,
                    (element_id,),
                )

            else:
                selection = self._controller.create_selection(
                    ElementType.SHELL_2D,
                    (element_id,),
                )

            task_result = self._controller.execute_task(
                task_id,
                self._model,
                selection,
                case_id,
            )

            view = self._controller.build_result_view(
                selection,
                VisualizationCriteria(
                    result_name="utilization"
                    if task_id == "example_bar_check"
                    else "required_thickness",
                    case_id=case_id,
                    mode=VisualizationMode.ELEMENT
                    if task_id == "example_bar_check"
                    else VisualizationMode.NODE_AVERAGED,
                ),
                task_result,
            )
            self._show_results(view)
        except Exception as exc:  # pragma: no cover - runtime feedback only
            QMessageBox.critical(
                self, "civil_3P", f"Falha ao executar a tarefa: {exc}")

    def _show_results(self, view) -> None:
        self._table.setSortingEnabled(False)
        self._table.setRowCount(len(view))
        self._table.setColumnCount(len(view.columns))
        self._table.setHorizontalHeaderLabels(list(view.columns))

        for row_index, row in enumerate(view.itertuples(index=False)):
            for column_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(
                    int(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft))
                self._table.setItem(row_index, column_index, item)

        self._table.resizeColumnsToContents()
        self._table.setSortingEnabled(True)


def main() -> int:
    app = QApplication.instance() or QApplication([])
    window = MainWindow(AppController())
    window.show()
    return app.exec()
