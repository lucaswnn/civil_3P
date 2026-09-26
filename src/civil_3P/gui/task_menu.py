from __future__ import annotations

from PySide6.QtWidgets import (
    QFormLayout,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
from typing import TYPE_CHECKING

import traceback

from civil_3P.standard.gui_components import GuiMenuComponents
from civil_3P.standard import model_components as mc
from civil_3P.standard import model_representation as rpr
from civil_3P.standard.result_components import ViewContentKind

if TYPE_CHECKING:
    from civil_3P.gui.task_menu_controller import TaskMenuController


class TaskMenu:
    def __init__(
        self,
        controller: TaskMenuController,
    ) -> None:
        self._controller = controller
        self.case_button: QToolButton | None = None
        self.task_button: QToolButton | None = None
        self.apply_to_selection_button: QPushButton | None = None
        self._selected_case_id: str | None = None
        self._selected_task_id: str | None = None
        self._panel: QWidget | None = None

    @property
    def identifier(self) -> str:
        return GuiMenuComponents.TASK_MENU

    @property
    def display_name(self) -> str:
        return GuiMenuComponents.TASK_MENU_NAME

    def build_panel(self, parent: QWidget) -> QWidget:
        panel = QWidget(parent)
        self._panel = panel
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.case_button = QToolButton(panel)
        self.case_button.setText("Selecione")
        self.case_button.setPopupMode(QToolButton.InstantPopup)
        case_menu = QMenu(self.case_button)
        case_menu.aboutToShow.connect(
            lambda: self._refresh_case_menu(case_menu)
        )
        self.case_button.setMenu(case_menu)

        self.task_button = QToolButton(panel)
        self.task_button.setText("Selecione")
        self.task_button.setPopupMode(QToolButton.InstantPopup)
        task_menu = QMenu(self.task_button)
        task_menu.aboutToShow.connect(
            lambda: self._refresh_task_menu(task_menu)
        )
        self.task_button.setMenu(task_menu)

        form_layout.addRow(QLabel("Caso"), self.case_button)
        form_layout.addRow(QLabel("Tarefa"), self.task_button)

        self.apply_to_selection_button = QPushButton(panel)
        self.apply_to_selection_button.setCheckable(True)
        apply_to_selection_label = QLabel("Aplicar na seleção")
        form_layout.addRow(
            self.apply_to_selection_button,
            apply_to_selection_label,
        )

        run_button = QPushButton("Executar tarefa")
        run_button.clicked.connect(self._run_task)
        form_layout.addRow(run_button)

        layout.addLayout(form_layout)
        layout.addStretch()

        return panel

    def _refresh_case_menu(self, menu: QMenu) -> None:
        menu.clear()

        for case_id in self._controller.get_load_case_ids():
            action = menu.addAction(case_id)
            action.triggered.connect(
                lambda _checked=False,
                identifier=case_id: self._select_case(identifier),
            )

    def _refresh_task_menu(self, menu: QMenu) -> None:
        menu.clear()

        for task_id in self._controller.get_task_identifiers():
            action = menu.addAction(task_id)
            action.triggered.connect(
                lambda _checked=False,
                identifier=task_id: self._select_task(identifier),
            )

    def _select_case(self, identifier: str) -> None:
        self._selected_case_id = identifier
        self.case_button.setText(identifier)

    def _select_task(self, identifier: str) -> None:
        self._selected_task_id = identifier
        self.task_button.setText(identifier)

    def _run_task(self) -> None:
        model = self._controller.current_model

        if model is None:
            QMessageBox.warning(
                self._panel,
                "civil_3P",
                "Carregue um modelo antes de executar uma tarefa.",
            )

            return

        task_id = self._selected_task_id
        case_id = self._selected_case_id

        if task_id is None or case_id is None:
            QMessageBox.warning(
                self._panel,
                "civil_3P",
                "Selecione uma tarefa e um caso antes de executar.",
            )

            return

        try:
            if task_id == "example_1d":
                view_content_kind = ViewContentKind.ELEMENT_1D_PROFILE
                element_type = mc.ModelComponents.ELEMENTS_1D
                element_ids = list(
                    model.tables[rpr.ModelTables.ELEMENTS_1D][
                        rpr.Elements1DColumns.ELEMENT
                    ].astype(str)
                )

            else:
                view_content_kind = ViewContentKind.ELEMENT_2D_SHARED_NODES
                element_type = mc.ModelComponents.ELEMENTS_2D
                element_ids = list(
                    model.tables[rpr.ModelTables.ELEMENTS_2D][
                        rpr.Elements2DColumns.ELEMENT
                    ].astype(str)
                )

            selection = self._controller.create_selection(
                element_type=element_type,
                selected_element_ids=element_ids,
            )

            task_result = self._controller.execute_task(
                task_id=task_id,
                selection=selection,
                case_id=case_id,
            )

            self._controller.set_result_scene(
                selection=selection,
                task_result=task_result,
                view_content_kind=view_content_kind,
            )

            QMessageBox.information(
                self._panel,
                "civil_3P",
                "Tarefa executada com sucesso.",
            )

        except Exception as exc:  # pragma: no cover - runtime feedback only
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setWindowTitle("civil_3P")
            msgbox.setText(f"Falha ao executar a tarefa: {exc}")
            msgbox.setDetailedText(traceback.format_exc())
            msgbox.exec()
