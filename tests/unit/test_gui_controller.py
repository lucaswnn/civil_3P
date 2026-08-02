from __future__ import annotations

import pandas as pd

from civil_3P.core.enums import ElementType, VisualizationMode
from civil_3P.core.results import VisualizationCriteria
from civil_3P.gui.controller import AppController
from civil_3P.importers.csv_importers import CsvImportProfile


def test_gui_controller_can_import_and_prepare_results(tmp_path) -> None:
    pd.DataFrame([
        {"Joint": "N1", "X": 0.0, "Y": 0.0, "Z": 0.0},
        {"Joint": "N2", "X": 1.0, "Y": 0.0, "Z": 0.0},
    ]).to_csv(tmp_path / "nodes.csv", index=False)

    pd.DataFrame([
        {
            "Frame": "B1",
            "JointI": "N1",
            "JointJ": "N2",
            "Material": "STEEL",
            "Section": "S1",
        },
    ]).to_csv(tmp_path / "elements_1d.csv", index=False)

    pd.DataFrame([{"Shell": "P1", "N1": "N1", "N2": "N2", "N3": "N2", "N4": "N1", "Material": "CONC", "Thickness": 0.2}]).to_csv(tmp_path / "elements_2d.csv", index=False)

    pd.DataFrame([
        {
            "EntityType": "element",
            "EntityId": "B1",
            "PropertyName": "axial_capacity",
            "PropertyValue": 20.0,
        },
    ]).to_csv(tmp_path / "properties.csv", index=False)

    pd.DataFrame([
        {
            "Case": "LC1",
            "ObjectType": "1D",
            "ObjectId": "B1",
            "Node": None,
            "Station": 0.0,
            "Result": "axial_force",
            "Value": 10.0,
            "Location": "element",
        },
    ]).to_csv(tmp_path / "results.csv", index=False)

    controller = AppController()
    model = controller.import_model(CsvImportProfile.SAP2000, tmp_path)
    selection = controller.create_selection(ElementType.BAR_1D, ("B1",))

    task_result = controller.execute_task(
        "example_bar_check",
        model,
        selection,
        "LC1",
    )
    view = controller.build_result_view(
        selection,
        VisualizationCriteria(
            result_name="utilization",
            case_id="LC1",
            mode=VisualizationMode.ELEMENT,
        ),
        task_result,
    )

    assert view.iloc[0]["value"] == 0.5
