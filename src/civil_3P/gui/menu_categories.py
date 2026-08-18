from __future__ import annotations

import traceback
from pathlib import Path
from typing import Protocol, Sequence

from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from civil_3P.core.results import VisualizationCriteria
from civil_3P.gui.category_controllers import FileMenuController, TaskController
from civil_3P.standard import model_components as mc
from civil_3P.standard.result_components import VisualizationMode
from civil_3P.standard.importer_profiles import ImporterProfiles
from civil_3P.visualization.widget import SceneWidget


class MenuCategory(Protocol):
    @property
    def identifier(self) -> str: ...

    @property
    def display_name(self) -> str: ...

    def build_panel(self, parent: QWidget) -> QWidget: ...


class FileMenuCategory:
    identifier = "arquivo"
    display_name = "Arquivo"

    def __init__(self, scene_widget: SceneWidget) -> None:
        self._controller = FileMenuController()
        self._scene_widget = scene_widget
        self._panel: QWidget | None = None

    def build_panel(self, parent: QWidget) -> QWidget:
        panel = QWidget(parent)
        self._panel = panel
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        import_button = QPushButton("Importar SAP2000")
        import_button.clicked.connect(self._import_sap2000)
        load_button = QPushButton("Carregar modelo")
        load_button.clicked.connect(self._load_saved_model)
        save_button = QPushButton("Salvar modelo")
        save_button.clicked.connect(self._save_model)
        plugins_button = QPushButton("Definir pasta de plugins")
        plugins_button.clicked.connect(self._set_plugins_folder)

        layout.addWidget(import_button)
        layout.addWidget(load_button)
        layout.addWidget(save_button)
        layout.addWidget(plugins_button)
        layout.addStretch()

        return panel

    def _import_sap2000(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self._panel,
            "Selecionar arquivo do SAP2000",
            str(Path.cwd()),
            "Arquivos Excel (*.xlsx);;Todos os Arquivos (*)",
        )

        if not file_path:
            return

        try:
            model = self._controller.import_model(
                ImporterProfiles.SAP2000,
                Path(file_path),
            )
            self._scene_widget.set_scene(self._controller.build_scene(model))
            QMessageBox.information(
                self._panel,
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
            self._panel,
            "Carregar modelo civil_3P",
            str(Path.cwd()),
            "Arquivos civil_3P (*.c3p)",
        )

        if not model_path:
            return

        try:
            model = self._controller.load_model_file(model_path)
            self._scene_widget.set_scene(self._controller.build_scene(model))
            QMessageBox.information(
                self._panel,
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
        model = self._controller.current_model
        if model is None:
            QMessageBox.warning(
                self._panel,
                "civil_3P",
                "Carregue um modelo antes de salvar.",
            )
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self._panel,
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
            self._controller.save_model(file_path)
            QMessageBox.information(
                self._panel,
                "civil_3P",
                f"Modelo salvo em: {file_path}",
            )
        except Exception as exc:  # pragma: no cover - runtime feedback only
            QMessageBox.critical(
                self._panel,
                "civil_3P",
                f"Falha ao salvar o modelo: {exc}",
            )

    def _set_plugins_folder(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self._panel,
            "Definir pasta de plugins",
            str(self._controller.preferences.plugins_base_path),
        )
        if not directory:
            return

        try:
            plugin_path = self._controller.set_plugins_base_path(directory)
            loaded = self._controller.load_plugins()
            QMessageBox.information(
                self._panel,
                "civil_3P",
                f"Pasta de plugins definida: {plugin_path}\n"
                f"Plugins carregados: {len(loaded)}",
            )
        except Exception as exc:  # pragma: no cover - runtime feedback only
            QMessageBox.critical(
                self._panel,
                "civil_3P",
                f"Falha ao definir a pasta de plugins: {exc}",
            )


class TaskMenuCategory:
    identifier = "tarefas"
    display_name = "Tarefas"

    def __init__(self) -> None:
        self._controller = TaskController()
        # Populated by build_panel; read by _run_task after the panel is built.
        self.case_edit: QLineEdit | None = None
        self.element_edit: QLineEdit | None = None
        self.task_edit: QLineEdit | None = None
        self._panel: QWidget | None = None

    def build_panel(self, parent: QWidget) -> QWidget:
        panel = QWidget(parent)
        self._panel = panel
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.case_edit = QLineEdit("LC1")
        self.element_edit = QLineEdit("B1")
        self.task_edit = QLineEdit("example_bar_check")

        form_layout.addRow(QLabel("Caso"), self.case_edit)
        form_layout.addRow(QLabel("Elemento"), self.element_edit)
        form_layout.addRow(QLabel("Tarefa"), self.task_edit)

        run_button = QPushButton("Executar tarefa")
        run_button.clicked.connect(self._run_task)
        form_layout.addRow(run_button)

        layout.addLayout(form_layout)
        layout.addStretch()

        return panel

    def _run_task(self) -> None:
        model = self._controller.current_model
        if model is None:
            QMessageBox.warning(
                self._panel,
                "civil_3P",
                "Carregue um modelo antes de executar uma tarefa.",
            )
            return

        task_id = self.task_edit.text().strip()
        case_id = self.case_edit.text().strip() or "LC1"
        element_id = self.element_edit.text().strip() or "B1"

        try:
            selection = self._controller.create_selection(
                mc.ModelComponents.ELEMENTS_1D if task_id == "example_bar_check" else mc.ModelComponents.ELEMENTS_2D,
                (element_id,),
            )

            task_result = self._controller.execute_task(
                task_id,
                model,
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
                self._panel,
                "civil_3P",
                f"Falha ao executar a tarefa: {exc}",
            )


class MenuCategoryRegistry:
    def __init__(self, categories: Sequence[MenuCategory]) -> None:
        self._categories: dict[str, MenuCategory] = {
            category.identifier: category for category in categories
        }

    def get(self, identifier: str) -> MenuCategory:
        return self._categories[identifier]

    def all(self) -> tuple[MenuCategory, ...]:
        return tuple(self._categories.values())
