from __future__ import annotations

from civil_3P.core.model import FEMModel
from civil_3P.gui.controller import AppController


def test_app_controller_can_save_and_load_model(tmp_path) -> None:
    model = FEMModel.empty()
    archive_path = tmp_path / "project.c3p"

    controller = AppController()
    controller.save_model(model, archive_path)
    loaded_model = controller.load_model_archive(archive_path)

    assert isinstance(loaded_model, FEMModel)
    assert set(loaded_model.tables_dict) == set(model.tables_dict)
    assert loaded_model.units_dict == model.units_dict
