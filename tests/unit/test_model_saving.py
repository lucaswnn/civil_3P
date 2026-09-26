from __future__ import annotations

from civil_3P.core.model import Model
from civil_3P.application.application_context import ApplicationContext
from civil_3P.gui.file_menu_controller import FileMenuController


def test_app_controller_can_save_and_load_model(tmp_path) -> None:
    model = Model.empty()
    file_path = tmp_path / "project.c3p"

    controller = FileMenuController()
    ApplicationContext()._model_service.model = model
    controller.save_model(file_path)
    loaded_model = controller.load_model_file(file_path)

    assert isinstance(loaded_model, Model)
    assert set(loaded_model.tables) == set(model.tables)
    assert loaded_model.units == model.units


def test_file_service_round_trips_user_preferences(tmp_path) -> None:
    context = ApplicationContext()
    context._model_service.model = Model.empty()
    context._preferences_service.scene_viewer_config.node_point_size = 7.0
    context._preferences_service.set_plugins_base_path(tmp_path)
    file_path = tmp_path / "preferences.c3p"

    from civil_3P.application.file_service import FileService

    FileService(context).save(file_path)
    context._preferences_service.scene_viewer_config.node_point_size = 1.0
    FileService(context).load(file_path)

    assert context._preferences_service.scene_viewer_config.node_point_size == 7.0
    assert context._preferences_service.plugins_base_path == tmp_path.resolve()
