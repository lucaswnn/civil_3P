from __future__ import annotations

from typing import TYPE_CHECKING
from civil_3P.application.model_service import ModelService
from civil_3P.application.plugin_loader_service import PluginLoaderService
from civil_3P.gui.tabs import ModeloViewTab, TabelaViewTab, ViewTabRegistry

from PySide6.QtWidgets import QApplication

from civil_3P.application.file_loader_service import FileLoaderService
from civil_3P.application.file_service import FileService
from civil_3P.application.importer_service import ImporterService
from civil_3P.application.task_service import TaskService
from civil_3P.application.preferences_service import UserPreferencesService
from civil_3P.gui.file_menu import FileMenuCategory
from civil_3P.gui.task_menu import TaskMenuCategory
from civil_3P.gui.file_menu_controller import FileMenuController
from civil_3P.gui.main_window import MainWindow
from civil_3P.gui.menu_categories import MenuCategoryRegistry
from civil_3P.gui.task_menu_controller import TaskMenuController
from civil_3P.gui.scene_widget import SceneWidget


class Application:
    def __init__(self):
        importer_service = ImporterService()
        plugin_loader_service = PluginLoaderService()
        task_service = TaskService(plugin_loader_service)
        model_service = ModelService()
        file_service = FileService()
        preferences_service = UserPreferencesService()
        result_builder = None
        result_builder_service = ResultBuilderService(
            model_service=model_service,
            result_builder=result_builder,
        )
        scene_builder = None
        view_builder_service = ViewBuilderService(scene_builder)
        file_loader_service = FileLoaderService(
            model_service=model_service,
            file_service=file_service,
            preferences_service=preferences_service,
        )
        scene_widget_listener = None
        file_menu_controller = FileMenuController(
            importer_service=importer_service,
            task_service=task_service,
            file_loader_service=file_loader_service,
            listeners=[scene_widget_listener],
        )
        file_menu = FileMenuCategory(file_menu_controller)
        task_menu_controller = TaskMenuController(
            task_service=task_service,
            listeners=[scene_widget_listener],
        )
        task_menu = TaskMenuCategory(task_menu_controller)
        menu_registry = MenuCategoryRegistry(
            [
                file_menu,
                task_menu,
            ]
        )
        scene_widget_listener = None
        scene_widget_controller = SceneWidgetController(
            model_service=model_service,
            result_builder_service=result_builder_service,
            view_builder_service=view_builder_service,
            scene_widget_listener=scene_widget_listener,
        )
        scene_renderer = None
        scene_widget = SceneWidget(
            controller=scene_widget_controller,
            renderer=scene_renderer,
        )
        model_viewtab = ModeloViewTab(scene_widget)
        table_viewtab = TabelaViewTab()
        tab_registry = ViewTabRegistry(
            [
                model_viewtab,
                table_viewtab
            ]
        )
        self.main_window = MainWindow(
            menu_registry=menu_registry,
            tab_registry=tab_registry,
            scene_widget=scene_widget,
        )

    def run(self):
        app = QApplication.instance() or QApplication([])
        self.main_window.show()
        return app.exec()
