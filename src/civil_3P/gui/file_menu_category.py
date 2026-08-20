from __future__ import annotations

import traceback
from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from civil_3P.gui.category_controllers import FileMenuController
from civil_3P.standard.importer_profiles import ImporterProfiles
from civil_3P.visualization.widget import SceneWidget


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
        folder_plugins_button = QPushButton("Definir pasta de plugins")
        folder_plugins_button.clicked.connect(self._set_plugins_folder)
        add_plugins_button = QPushButton("Adicionar plugins")
        add_plugins_button.clicked.connect(self._add_plugins)


        layout.addWidget(import_button)
        layout.addWidget(load_button)
        layout.addWidget(save_button)
        layout.addWidget(folder_plugins_button)
        layout.addWidget(add_plugins_button)
        layout.addStretch()

        return panel

    def _add_plugins(self) -> None:
        try:
            files, _ = QFileDialog.getOpenFileNames(
                self._panel,
                "Selecionar arquivos de plugins",
                str(Path.cwd()),
                "Arquivos Python (*.py);;Todos os Arquivos (*)",
            )
            if not files:
                return

            loaded = self._controller.add_plugins(files)
            QMessageBox.information(
                self._panel,
                "civil_3P",
                f"Plugins carregados: {len(loaded)}",
            )
        except Exception as exc:  # pragma: no cover - runtime feedback only
            QMessageBox.critical(
                self._panel,
                "civil_3P",
                f"Falha ao carregar plugins: {exc}",
            )

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
