from __future__ import annotations

from civil_3P.core.model import FEMModel
from civil_3P.application.services import ApplicationContext
from civil_3P.gui.category_controllers import FileMenuController


def test_app_controller_can_save_and_load_model(tmp_path) -> None:
    model = FEMModel.empty()
    file_path = tmp_path / "project.c3p"

    controller = FileMenuController()
    ApplicationContext().model_service.model = model
    controller.save_model(file_path)
    loaded_model = controller.load_model_file(file_path)

    assert isinstance(loaded_model, FEMModel)
    assert set(loaded_model.tables_dict) == set(model.tables_dict)
    assert loaded_model.units_dict == model.units_dict


def test_file_service_round_trips_user_preferences(tmp_path) -> None:
    context = ApplicationContext()
    context.model_service.model = FEMModel.empty()
    context.preferences.scene_viewer_config.node_point_size = 7.0
    context.preferences.set_plugins_base_path(tmp_path)
    file_path = tmp_path / "preferences.c3p"

    from civil_3P.file_service.file_service import FileService

    FileService(context).save(file_path)
    context.preferences.scene_viewer_config.node_point_size = 1.0
    FileService(context).load(file_path)

    assert context.preferences.scene_viewer_config.node_point_size == 7.0
    assert context.preferences.plugins_base_path == tmp_path.resolve()
