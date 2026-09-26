from __future__ import annotations

import traceback
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from civil_3P.gui.refreshing_combo_box import RefreshingComboBox
from civil_3P.standard import model_components as mc
from civil_3P.standard import model_representation as rpr
from civil_3P.standard.gui_components import GuiMenuComponents
from civil_3P.standard.gui_texts import TaskMenuButtonLabels
from civil_3P.standard.result_components import ViewContentKind
from civil_3P.standard.gui_texts import (
    GuiLabels,
    GuiMessageTexts,
)
from civil_3P.utils.gui_messages import GuiMessages

if TYPE_CHECKING:
    from civil_3P.gui.task_menu_controller import TaskMenuController


class TaskMenu:
    def __init__(
        self,
        controller: TaskMenuController,
    ) -> None:
        self._controller = controller
        self.case_button: RefreshingComboBox | None = None
        self.task_button: RefreshingComboBox | None = None
        self.apply_to_selection_button: QPushButton | None = None
        self._panel: QWidget | None = None

    @property
    def identifier(self) -> str:
        return GuiMenuComponents.TASK_MENU

    @property
    def display_name(self) -> str:
        return GuiMenuComponents.TASK_MENU_NAME

    def build_panel(self, parent: QWidget) -> QWidget:
        panel = QWidget(parent)
        panel.setObjectName("taskMenuPanel")
        self._panel = panel
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.case_button = RefreshingComboBox(
            self._controller.get_load_case_ids,
            GuiLabels.SELECT_OPTION,
            panel,
        )
        self.case_button.setObjectName("caseCombo")
        self.task_button = RefreshingComboBox(
            self._controller.get_task_identifiers,
            GuiLabels.SELECT_OPTION,
            panel,
        )
        self.task_button.setObjectName("taskCombo")

        form_layout.addRow(
            QLabel(TaskMenuButtonLabels.CASE),
            self.case_button,
        )
        form_layout.addRow(
            QLabel(TaskMenuButtonLabels.TASK),
            self.task_button,
        )

        run_button = QPushButton(TaskMenuButtonLabels.EXECUTE_TASK)
        run_button.clicked.connect(self._run_task)
        form_layout.addRow(run_button)

        layout.addLayout(form_layout)
        layout.addStretch()

        return panel

    def _run_task(self) -> None:
        model = self._controller.current_model

        if model is None:
            GuiMessages.display_warning(
                self._panel,
                GuiMessageTexts.LOAD_MODEL_BEFORE_TASK,
            )

            return

        task_combo = self.task_button
        case_combo = self.case_button
        if task_combo is None or case_combo is None:
            return

        task_combo.refresh_options()
        case_combo.refresh_options()
        task_id = self._selected_option(task_combo)
        case_id = self._selected_option(case_combo)

        if task_id is None or case_id is None:
            GuiMessages.display_warning(
                self._panel,
                GuiMessageTexts.SELECT_TASK_AND_CASE,
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

            GuiMessages.display_info(
                self._panel,
                GuiMessageTexts.TASK_SUCCEEDED,
            )

        except Exception as exc:  # pragma: no cover - runtime feedback only
            GuiMessages.display_error(
                self._panel,
                GuiMessageTexts.TASK_FAILED.format(error=exc),
                traceback.format_exc(),
            )

    @staticmethod
    def _selected_option(combo: QComboBox) -> str | None:
        text = combo.currentText().strip()
        index = combo.findText(text, Qt.MatchFlag.MatchFixedString)
        if not text or index < 0:
            return None

        return combo.itemText(index)
