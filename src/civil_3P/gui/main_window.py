from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QHBoxLayout,
    QMainWindow,
    QSplitter,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from civil_3P.standard.gui_texts import GuiLabels

if TYPE_CHECKING:
    from civil_3P.gui.main_window_controller import MainWindowController
    from civil_3P.gui.menu_category_registry import MenuCategoryRegistry
    from civil_3P.gui.scene_widget import SceneWidget
    from civil_3P.gui.view_tab_registry import ViewTabRegistry


class MainWindow(QMainWindow):
    def __init__(
        self,
        menu_registry: MenuCategoryRegistry,
        view_tab_registry: ViewTabRegistry,
        main_window_controller: MainWindowController,
        scene_widget: SceneWidget,
    ) -> None:
        super().__init__()
        self._menu_registry = menu_registry
        self._view_tab_registry = view_tab_registry
        self._main_window_controller = main_window_controller
        self._scene_widget = scene_widget
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setObjectName("mainWindow")
        self.setWindowTitle(GuiLabels.APPLICATION_NAME)
        self.resize(1000, 600)

        central_widget = QWidget(self)
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setSpacing(12)

        right_panel = self._build_right_panel()
        left_panel = self._build_left_panel()

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(6)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setSizes([30, 90])
        root_layout.addWidget(splitter)

    def _build_right_panel(self) -> QWidget:
        right_panel = QWidget(self)
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(4)

        self._scene_widget.setMinimumWidth(700)
        self._scene_widget.setMinimumHeight(280)

        self._tab_registry = self._view_tab_registry

        self._view_stack = QStackedWidget(right_panel)
        self._tab_index: dict[str, int] = {}

        for tab in self._tab_registry.all():
            index = self._view_stack.addWidget(tab.build_content(self._view_stack))
            self._tab_index[tab.identifier] = index

        tab_bar = QWidget(right_panel)
        tab_bar.setObjectName("viewTabBar")
        tab_bar_layout = QHBoxLayout(tab_bar)
        tab_bar_layout.setSpacing(4)

        tab_group = QButtonGroup(tab_bar)
        tab_group.setExclusive(True)

        for tab in self._tab_registry.all():
            tab_button = QToolButton(tab_bar)
            tab_button.setText(tab.display_name)
            tab_button.setCheckable(True)
            tab_button.clicked.connect(
                lambda _checked=False, identifier=tab.identifier: self._select_tab(
                    identifier
                ),
            )
            tab_group.addButton(tab_button)
            tab_bar_layout.addWidget(tab_button)

        tab_bar_layout.addStretch()
        first_button = tab_group.buttons()[0]
        first_button.setChecked(True)

        right_layout.addWidget(tab_bar)
        right_layout.addWidget(self._view_stack)

        self._select_tab(self._tab_registry.all()[0].identifier)

        return right_panel

    def _build_left_panel(self) -> QWidget:
        left_panel = QWidget(self)
        left_panel.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(12)

        self._category_registry = self._menu_registry

        self._category_stack = QStackedWidget(left_panel)
        self._category_stack.setObjectName("categoryStack")
        self._category_index: dict[str, int] = {}

        for category in self._category_registry.all():
            index = self._category_stack.addWidget(
                category.build_panel(self._category_stack)
            )
            self._category_index[category.identifier] = index

        self._category_button = QComboBox(left_panel)
        self._category_button.setObjectName("categorySelector")
        self._category_button.setEditable(False)
        self._category_button.view().setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        for category in self._category_registry.all():
            self._category_button.addItem(
                category.display_name,
                category.identifier,
            )

        self._category_button.activated.connect(
            lambda index: self._select_category(self._category_button.itemData(index))
        )

        left_layout.addWidget(
            self._category_button,
            alignment=Qt.AlignmentFlag.AlignLeft,
        )
        left_layout.addWidget(self._category_stack)

        self._select_category(self._category_registry.all()[0].identifier)

        return left_panel

    def _select_category(self, identifier: str) -> None:
        self._category_button.setCurrentIndex(
            self._category_button.findData(identifier)
        )
        self._category_stack.setCurrentIndex(self._category_index[identifier])

    def _select_tab(self, identifier: str) -> None:
        self._view_stack.setCurrentIndex(self._tab_index[identifier])
