from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import traceback

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
    QMenu,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from civil_3P.core.enums import ElementType, VisualizationMode
from civil_3P.core.results import VisualizationCriteria
from civil_3P.importers.importer import ImporterProfile
from civil_3P.gui import AppController
from civil_3P.visualization.scene import VisualizationService
from civil_3P.visualization.widget import SceneWidget

if TYPE_CHECKING:
    from civil_3P.gui.controller import AppController


class MainWindow(QMainWindow):
    def __init__(self, controller: "AppController") -> None:
        super().__init__()
        self._controller = controller
        self._model = None
        self._scene_service = VisualizationService()
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWindowTitle("civil_3P")
        self.resize(1000, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(12)

        left_panel = QWidget(self)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        file_button = QPushButton("arquivo")
        file_menu = QMenu(self)
        import_action = file_menu.addAction("Importar SAP2000")
        import_action.triggered.connect(self._import_sap2000)
        load_saved_action = file_menu.addAction("Carregar modelo")
        load_saved_action.triggered.connect(self._load_saved_model)
        save_action = file_menu.addAction("Salvar modelo")
        save_action.triggered.connect(self._save_model)
        file_button.setMenu(file_menu)
        left_layout.addWidget(
            file_button, alignment=Qt.AlignmentFlag.AlignLeft)

        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self._case_edit = QLineEdit("LC1")
        self._element_edit = QLineEdit("B1")
        self._task_combo = QLineEdit("example_bar_check")

        form_layout.addRow(QLabel("Caso"), self._case_edit)
        form_layout.addRow(QLabel("Elemento"), self._element_edit)
        form_layout.addRow(QLabel("Tarefa"), self._task_combo)

        run_button = QPushButton("Executar tarefa")
        run_button.clicked.connect(self._run_task)
        form_layout.addRow(run_button)

        left_layout.addLayout(form_layout)
        left_layout.addStretch()

        self._scene_widget = SceneWidget(self)
        self._scene_widget.setMinimumWidth(700)
        self._scene_widget.setMinimumHeight(280)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.addWidget(left_panel)
        splitter.addWidget(self._scene_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setSizes([300, 900])
        root_layout.addWidget(splitter)

    def _import_sap2000(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo do SAP2000",
            str(Path.cwd()),
            "Arquivos Excel (*.xlsx);;Todos os Arquivos (*)",
        )

        if not file_path:
            return

        try:
            self._model = self._controller.import_model(
                ImporterProfile.SAP2000,
                Path(file_path),
            )
            self._scene_widget.set_scene(
                self._scene_service.build_scene(self._model)
            )
            QMessageBox.information(
                self,
                "civil_3P",
                "Modelo carregado com sucesso.",
            )
        except Exception as exc:  # pragma: no cover - runtime feedback only
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setWindowTitle("civil_3P")
            msgbox.setText(f"Falha ao carregar o modelo: {exc}")
            msgbox.setDetailedText(traceback.format_exc())
            msgbox.exec()

    def _load_saved_model(self) -> None:
        model_path, _ = QFileDialog.getOpenFileName(
            self,
            "Carregar modelo civil_3P",
            str(Path.cwd()),
            "Arquivos civil_3P (*.c3p)",
        )

        if not model_path:
            return

        try:
            self._model = self._controller.load_model_archive(model_path)
            self._scene_widget.set_scene(
                self._scene_service.build_scene(self._model)
            )
            QMessageBox.information(
                self,
                "civil_3P",
                "Modelo salvo carregado com sucesso.",
            )
        except Exception as exc:  # pragma: no cover - runtime feedback only
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setWindowTitle("civil_3P")
            msgbox.setText(f"Falha ao carregar o modelo salvo: {exc}")
            msgbox.setDetailedText(traceback.format_exc())
            msgbox.exec()

    def _save_model(self) -> None:
        if self._model is None:
            QMessageBox.warning(
                self,
                "civil_3P",
                "Carregue um modelo antes de salvar.",
            )
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar modelo civil_3P",
            str(Path.cwd()),
            "Arquivos civil_3P (*.c3p)",
        )

        if not save_path:
            return

        file_path = Path(save_path)
        if file_path.suffix.lower() != ".c3p":
            file_path = file_path.with_suffix(".c3p")

        try:
            self._controller.save_model(self._model, file_path)
            QMessageBox.information(
                self,
                "civil_3P",
                f"Modelo salvo em: {file_path}",
            )
        except Exception as exc:  # pragma: no cover - runtime feedback only
            QMessageBox.critical(
                self,
                "civil_3P",
                f"Falha ao salvar o modelo: {exc}",
            )

    def _run_task(self) -> None:
        if self._model is None:
            QMessageBox.warning(
                self,
                "civil_3P",
                "Carregue um modelo antes de executar uma tarefa.",
            )
            return

        task_id = self._task_combo.text().strip()
        case_id = self._case_edit.text().strip() or "LC1"
        element_id = self._element_edit.text().strip() or "B1"

        try:
            selection = self._controller.create_selection(
                ElementType.BAR_1D if task_id == "example_bar_check" else ElementType.SHELL_2D,
                (element_id,),
            )

            task_result = self._controller.execute_task(
                task_id,
                self._model,
                selection,
                case_id,
            )

            self._controller.build_result_view(
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
        except Exception as exc:  # pragma: no cover - runtime feedback only
            QMessageBox.critical(
                self,
                "civil_3P",
                f"Falha ao executar a tarefa: {exc}",
            )


def main() -> int:
    app = QApplication.instance() or QApplication([])
    window = MainWindow(AppController())
    window.show()
    return app.exec()
