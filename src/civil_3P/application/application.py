from __future__ import annotations

from PySide6.QtWidgets import QApplication

from civil_3P.application.file_loader_service import FileLoaderService
from civil_3P.application.file_service import FileService
from civil_3P.application.importer_service import ImporterService
from civil_3P.application.model_service import ModelService
from civil_3P.application.plugin_loader_service import PluginLoaderService
from civil_3P.application.preferences_service import PreferencesService
from civil_3P.application.result_builder_service import ResultBuilderService
from civil_3P.application.task_service import TaskService
from civil_3P.application.view_builder_service import ViewBuilderService
from civil_3P.core.result_builder_registry import ResultBuilderRegistry
from civil_3P.gui.file_menu import FileMenu
from civil_3P.gui.file_menu_controller import FileMenuController
from civil_3P.gui.main_window import MainWindow
from civil_3P.gui.main_window_controller import MainWindowController
from civil_3P.gui.menu_category_registry import MenuCategoryRegistry
from civil_3P.gui.model_view_tab import ModelViewTab
from civil_3P.gui.scene_widget import SceneWidget
from civil_3P.gui.scene_widget_controller import SceneWidgetController
from civil_3P.gui.table_view_tab import TableViewTab
from civil_3P.gui.view_tab_registry import ViewTabRegistry
from civil_3P.gui.task_menu import TaskMenu
from civil_3P.gui.task_menu_controller import TaskMenuController
from civil_3P.importers.importer_registry import ImporterRegistry
from civil_3P.tasks.task_registry import TaskRegistry
from civil_3P.visualization.scene_builder_registry import SceneBuilderRegistry
from civil_3P.visualization.scene_renderer import SceneRenderer


class Application:
    def __init__(self):
        self._qt_app = QApplication.instance() or QApplication([])

        # --------
        # services
        # --------
        self._importer_service = self._build_importer_service()
        self._task_service = self._build_task_service()
        self._model_service = ModelService()
        self._file_service = FileService()
        self._preferences_service = PreferencesService()
        self._result_builder_service = self._build_result_builder_service()
        self._view_builder_service = self._build_view_builder_service()
        file_loader_service = FileLoaderService(
            model_service=self._model_service,
            file_service=self._file_service,
            preferences_service=self._preferences_service,
        )

        # -----------
        # controllers
        # -----------
        scene_widget_controller = SceneWidgetController(
            model_service=self._model_service,
            result_builder_service=self._result_builder_service,
            view_builder_service=self._view_builder_service,
        )
        file_menu_controller = FileMenuController(
            importer_service=self._importer_service,
            task_service=self._task_service,
            file_loader_service=file_loader_service,
            model_service=self._model_service,
            preferences_service=self._preferences_service,
            scene_widget_controller=scene_widget_controller,
        )
        task_menu_controller = TaskMenuController(
            task_service=self._task_service,
            result_builder_service=self._result_builder_service,
            view_builder_service=self._view_builder_service,
            model_service=self._model_service,
            scene_widget_controller=scene_widget_controller,
        )

        # -------------------------
        # scene widget and renderer
        # -------------------------
        scene_renderer = SceneRenderer()
        self._scene_widget = SceneWidget(
            controller=scene_widget_controller,
            renderer=scene_renderer,
        )

        # -----
        # menus
        # -----
        self._file_menu = FileMenu(file_menu_controller)
        self._task_menu = TaskMenu(task_menu_controller)

        # -----------
        # main window
        # -----------
        self.main_window = self._build_main_window()

        self._initialize()

    def _build_importer_service(self) -> ImporterService:
        importer_registry = ImporterRegistry()
        
        return ImporterService(importer_registry)

    def _build_task_service(self) -> TaskService:
        task_registry = TaskRegistry()
        plugin_loader_service = PluginLoaderService()

        return TaskService(
            task_registry=task_registry,
            plugin_loader_service=plugin_loader_service,
        )

    def _build_result_builder_service(self) -> ResultBuilderService:
        result_builder_registry = ResultBuilderRegistry()

        return ResultBuilderService(
            model_service=self._model_service,
            result_builder_registry=result_builder_registry,
        )

    def _build_view_builder_service(self) -> ViewBuilderService:
        scene_builder_registry = SceneBuilderRegistry()

        return ViewBuilderService(scene_builder_registry)

    def _build_main_window(self) -> MainWindow:
        menu_registry = MenuCategoryRegistry(
            [
                self._file_menu,
                self._task_menu,
            ]
        )
        model_viewtab = ModelViewTab(self._scene_widget)
        table_viewtab = TableViewTab()
        tab_registry = ViewTabRegistry(
            [
                model_viewtab,
                table_viewtab,
            ]
        )

        main_window_controller = MainWindowController(
            self._preferences_service
        )
        
        return MainWindow(
            menu_registry=menu_registry,
            view_tab_registry=tab_registry,
            main_window_controller=main_window_controller,
            scene_widget=self._scene_widget,
        )

    def _initialize(self):
        self._task_service.load_plugins_from(
            self
            ._preferences_service
            .get_plugins_base_path()
        )

    def run(self):
        self.main_window.show()

        return self._qt_app.exec()
