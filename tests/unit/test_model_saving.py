from __future__ import annotations

from civil_3P.core.model import FEMModel
from civil_3P.gui.category_controllers import FileMenuController


def test_app_controller_can_save_and_load_model(tmp_path) -> None:
    model = FEMModel.empty()
    file_path = tmp_path / "project.c3p"

    controller = FileMenuController()
    controller.save_model(model, file_path)
    loaded_model = controller.load_model_file(file_path)

    assert isinstance(loaded_model, FEMModel)
    assert set(loaded_model.tables_dict) == set(model.tables_dict)
    assert loaded_model.units_dict == model.units_dict
