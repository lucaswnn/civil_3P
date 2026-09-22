from __future__ import annotations

from civil_3P.application.model_service import ModelService
from civil_3P.application.plugin_loader_service import PluginLoaderService
from civil_3P.gui.model_view_tab import ModelViewTab
from civil_3P.gui.table_view_tab import TableViewTab
from civil_3P.gui.tabs import ViewTabRegistry
from civil_3P.application.result_builder_service import ResultBuilderService
from civil_3P.core.result_builder_registry import ResultBuilderRegistry

from PySide6.QtWidgets import QApplication

from civil_3P.application.file_loader_service import FileLoaderService
from civil_3P.application.file_service import FileService
from civil_3P.application.importer_service import ImporterService
from civil_3P.application.task_service import TaskService
from civil_3P.application.view_builder_service import ViewBuilderService
from civil_3P.application.preferences_service import PreferencesService
from civil_3P.gui.file_menu_controller import FileMenuController
from civil_3P.gui.main_window import MainWindow
from civil_3P.gui.menu_categories import MenuCategoryRegistry
from civil_3P.gui.task_menu_controller import TaskMenuController
from civil_3P.gui.scene_widget import SceneWidget
from civil_3P.gui.scene_widget_controller import SceneWidgetController
from civil_3P.gui.scene_widget_listener import SceneWidgetListener
from civil_3P.gui.file_menu import FileMenu
from civil_3P.gui.task_menu import TaskMenu
from civil_3P.visualization.scene_builder_registry import SceneBuilderRegistry
from civil_3P.visualization.scene_renderer import SceneRenderer
from civil_3P.tasks.task_registry import TaskRegistry
from civil_3P.importers.importer_registry import ImporterRegistry


class Application:
    def __init__(self):
        self._qt_app = QApplication.instance() or QApplication([])
        importer_registry = ImporterRegistry()
        importer_service = ImporterService(importer_registry)
        task_registry = TaskRegistry()
        plugin_loader_service = PluginLoaderService()
        task_service = TaskService(
            task_registry=task_registry,
            plugin_loader_service=plugin_loader_service,
        )
        model_service = ModelService()
        file_service = FileService()
        preferences_service = PreferencesService()
        result_builder_registry = ResultBuilderRegistry()
        result_builder_service = ResultBuilderService(
            model_service=model_service,
            result_builder_registry=result_builder_registry,
        )
        scene_builder_registry = SceneBuilderRegistry()
        view_builder_service = ViewBuilderService(scene_builder_registry)
        file_loader_service = FileLoaderService(
            model_service=model_service,
            file_service=file_service,
            preferences_service=preferences_service,
        )
        scene_widget_listener = SceneWidgetListener()
        file_menu_controller = FileMenuController(
            importer_service=importer_service,
            task_service=task_service,
            file_loader_service=file_loader_service,
            model_service=model_service,
            preferences_service=preferences_service,
            listeners=[scene_widget_listener],
        )
        scene_widget_controller = SceneWidgetController(
            model_service=model_service,
            result_builder_service=result_builder_service,
            view_builder_service=view_builder_service,
        )
        scene_renderer = SceneRenderer()
        scene_widget = SceneWidget(
            controller=scene_widget_controller,
            renderer=scene_renderer,
        )
        file_menu = FileMenu(scene_widget, file_menu_controller)
        task_menu_controller = TaskMenuController(
            task_service=task_service,
            result_builder_service=result_builder_service,
            view_builder_service=view_builder_service,
            model_service=model_service,
            listeners=[scene_widget_listener],
        )
        task_menu = TaskMenu(scene_widget, task_menu_controller)
        menu_registry = MenuCategoryRegistry(
            [
                file_menu,
                task_menu,
            ]
        )
        model_viewtab = ModelViewTab(scene_widget)
        table_viewtab = TableViewTab()
        tab_registry = ViewTabRegistry(
            [
                model_viewtab,
                table_viewtab,
            ]
        )
        self.main_window = MainWindow(
            menu_registry=menu_registry,
            view_tab_registry=tab_registry,
            scene_widget=scene_widget,
        )

        task_service.load_plugins_from(preferences_service.get_plugins_base_path())

    def run(self):
        self.main_window.show()
        return self._qt_app.exec()
