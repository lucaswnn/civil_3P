from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QSplitter,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from civil_3P.gui.menu_categories import MenuCategoryRegistry
from civil_3P.gui.task_menu_category import TaskMenuCategory
from civil_3P.gui.file_menu_category import FileMenuCategory
from civil_3P.gui.tabs import ModeloViewTab, TabelaViewTab, ViewTabRegistry
from civil_3P.visualization.widget import SceneWidget
from civil_3P.application.services import ApplicationContext


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._context = ApplicationContext()
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWindowTitle("civil_3P")
        self.resize(1000, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(12)

        # Right panel builds scene_widget, needed by the left panel's File category.
        right_panel = self._build_right_panel()
        left_panel = self._build_left_panel()

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setSizes([300, 900])
        root_layout.addWidget(splitter)

    def _build_left_panel(self) -> QWidget:
        left_panel = QWidget(self)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        self._category_registry = MenuCategoryRegistry((
            FileMenuCategory(self._scene_widget),
            TaskMenuCategory(self._scene_widget),
        ))

        self._category_stack = QStackedWidget(left_panel)
        self._category_index: dict[str, int] = {}
        for category in self._category_registry.all():
            index = self._category_stack.addWidget(
                category.build_panel(self._category_stack))
            self._category_index[category.identifier] = index

        self._category_button = QToolButton(left_panel)
        self._category_button.setPopupMode(QToolButton.InstantPopup)
        category_menu = QMenu(self._category_button)
        for category in self._category_registry.all():
            action = category_menu.addAction(category.display_name)
            action.triggered.connect(
                lambda _checked=False, identifier=category.identifier: self._select_category(identifier))
        self._category_button.setMenu(category_menu)

        left_layout.addWidget(
            self._category_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        left_layout.addWidget(self._category_stack)

        self._select_category(self._category_registry.all()[0].identifier)

        return left_panel

    def _select_category(self, identifier: str) -> None:
        category = self._category_registry.get(identifier)
        self._category_button.setText(category.display_name)
        self._category_stack.setCurrentIndex(self._category_index[identifier])

    def _build_right_panel(self) -> QWidget:
        right_panel = QWidget(self)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(4)

        self._scene_widget = SceneWidget(
            right_panel,
            config=self._context.preferences.scene_viewer_config,
        )
        self._scene_widget.setMinimumWidth(700)
        self._scene_widget.setMinimumHeight(280)

        self._tab_registry = ViewTabRegistry((
            ModeloViewTab(self._scene_widget),
            TabelaViewTab(),
        ))

        self._view_stack = QStackedWidget(right_panel)
        self._tab_index: dict[str, int] = {}
        for tab in self._tab_registry.all():
            index = self._view_stack.addWidget(
                tab.build_content(self._view_stack))
            self._tab_index[tab.identifier] = index

        tab_bar = QWidget(right_panel)
        tab_bar.setFixedHeight(28)
        tab_bar_layout = QHBoxLayout(tab_bar)
        tab_bar_layout.setContentsMargins(4, 0, 4, 0)
        tab_bar_layout.setSpacing(4)

        tab_group = QButtonGroup(tab_bar)
        tab_group.setExclusive(True)
        for tab in self._tab_registry.all():
            tab_button = QToolButton(tab_bar)
            tab_button.setText(tab.display_name)
            tab_button.setCheckable(True)
            tab_button.clicked.connect(
                lambda _checked=False, identifier=tab.identifier: self._select_tab(identifier))
            tab_group.addButton(tab_button)
            tab_bar_layout.addWidget(tab_button)
        tab_bar_layout.addStretch()
        first_button = tab_group.buttons()[0]
        first_button.setChecked(True)

        right_layout.addWidget(tab_bar)
        right_layout.addWidget(self._view_stack)

        self._select_tab(self._tab_registry.all()[0].identifier)

        return right_panel

    def _select_tab(self, identifier: str) -> None:
        self._view_stack.setCurrentIndex(self._tab_index[identifier])


def show_gui() -> int:
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()
    return app.exec()
