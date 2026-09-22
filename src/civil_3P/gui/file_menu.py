from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from PySide6.QtWidgets import (
    QFileDialog,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from typing import TYPE_CHECKING

import traceback

from civil_3P.standard.gui_components import GuiMenuComponents
from civil_3P.standard.importer_profiles import ImporterProfiles
from civil_3P.utils.gui_messages import GuiMessages as gm

if TYPE_CHECKING:
    from civil_3P.gui.file_menu_controller import FileMenuController
    from civil_3P.gui.scene_widget import SceneWidget


class FileMenuButtonLabels(StrEnum):
    ADD_PLUGINS = "Adicionar plugins"
    IMPORT_SAP2000 = "Importar SAP2000"
    LOAD_MODEL = "Carregar modelo"
    SAVE_MODEL = "Salvar modelo"
    SET_PLUGINS_FOLDER = "Definir pasta de plugins"


class FileMenu:
    def __init__(
        self,
        scene_widget: SceneWidget,
        file_menu_controller: FileMenuController,
    ) -> None:
        self._controller = file_menu_controller
        self._scene_widget = scene_widget
        self._panel: QWidget | None = None

    @property
    def identifier(self) -> str:
        return GuiMenuComponents.FILE_MENU

    @property
    def display_name(self) -> str:
        return GuiMenuComponents.FILE_MENU_NAME

    def build_panel(self, parent: QWidget) -> QWidget:
        panel = QWidget(parent)
        self._panel = panel
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        import_button = QPushButton(FileMenuButtonLabels.IMPORT_SAP2000)
        import_button.clicked.connect(self._import_sap2000)
        load_button = QPushButton(FileMenuButtonLabels.LOAD_MODEL)
        load_button.clicked.connect(self._load_saved_model)
        save_button = QPushButton(FileMenuButtonLabels.SAVE_MODEL)
        save_button.clicked.connect(self._save_model)
        folder_plugins_button = QPushButton(
            FileMenuButtonLabels.SET_PLUGINS_FOLDER
        )
        folder_plugins_button.clicked.connect(self._set_plugins_folder)
        add_plugins_button = QPushButton(
            FileMenuButtonLabels.ADD_PLUGINS
        )
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

            res = self._controller.add_plugins(files)
            res.display_message(self._panel)

        except Exception as exc:  # pragma: no cover - runtime feedback only
            gm.display_error(
                self._panel,
                message=f"Falha ao carregar plugins: {exc}",
                detailed_message=traceback.format_exc(),
            )

    def _import_sap2000(self) -> None:
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self._panel,
                "Selecionar arquivo do SAP2000",
                str(Path.cwd()),
                "Arquivos Excel (*.xlsx);;Todos os Arquivos (*)",
            )

            if not file_path:
                return

            res = self._controller.import_model(
                ImporterProfiles.SAP2000,
                Path(file_path),
            )
            self._scene_widget.set_scene()
            res.display_message(self._panel)

        except Exception as exc:  # pragma: no cover - runtime feedback only
            gm.display_error(
                self._panel,
                message=f"Falha ao importar o modelo: {exc}",
                detailed_message=traceback.format_exc(),
            )

    def _load_saved_model(self) -> None:
        try:
            model_path, _ = QFileDialog.getOpenFileName(
                self._panel,
                "Carregar modelo civil_3P",
                str(Path.cwd()),
                "Arquivos civil_3P (*.c3p)",
            )

            if not model_path:
                return

            res = self._controller.load_model_file(model_path)
            self._scene_widget.set_scene()
            res.display_message(self._panel)

        except Exception as exc:  # pragma: no cover - runtime feedback only
            gm.display_error(
                self._panel,
                message=f"Falha ao carregar o modelo salvo: {exc}",
                detailed_message=traceback.format_exc(),
            )

    def _save_model(self) -> None:
        try:
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

            res = self._controller.save_model(file_path)
            res.display_message(self._panel)

        except Exception as exc:  # pragma: no cover - runtime feedback only
            gm.display_error(
                self._panel,
                message=f"Falha ao salvar o modelo: {exc}",
                detailed_message=traceback.format_exc(),
            )

    def _set_plugins_folder(self) -> None:
        try:
            directory = QFileDialog.getExistingDirectory(
                self._panel,
                "Definir pasta de plugins",
                str(self._controller.get_plugins_base_path()),
            )

            if not directory:
                return

            res = self._controller.set_plugins_base_path(
                directory
            )
            res.display_message(self._panel)

        except Exception as exc:  # pragma: no cover - runtime feedback only
            gm.display_error(
                self._panel,
                message=f"Falha ao definir a pasta de plugins: {exc}",
                detailed_message=traceback.format_exc(),
            )
