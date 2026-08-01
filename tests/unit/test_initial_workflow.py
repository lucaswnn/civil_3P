from __future__ import annotations

import pandas as pd

from civil_3P.application.services import ImportModelService, ResultQueryService, TaskExecutionService
from civil_3P.core.enums import ElementType, VisualizationMode
from civil_3P.core.results import ResultAveragingPolicy, VisualizationCriteria
from civil_3P.core.selection import SelectionContext
from civil_3P.importers.csv_importers import CsvImportProfile
from civil_3P.tasks.check_example import ExampleBarCheckPlugin
from civil_3P.tasks.design_example import ExampleShellDesignPlugin


def test_import_and_example_tasks(tmp_path) -> None:
    pd.DataFrame(
        [
            {"Joint": "N1", "X": 0.0, "Y": 0.0, "Z": 0.0},
            {"Joint": "N2", "X": 1.0, "Y": 0.0, "Z": 0.0},
            {"Joint": "N3", "X": 1.0, "Y": 1.0, "Z": 0.0},
            {"Joint": "N4", "X": 0.0, "Y": 1.0, "Z": 0.0},
        ]
    ).to_csv(tmp_path / "nodes.csv", index=False)
    pd.DataFrame(
        [
            {"Frame": "B1", "JointI": "N1", "JointJ": "N2",
                "Material": "STEEL", "Section": "S1"},
        ]
    ).to_csv(tmp_path / "elements_1d.csv", index=False)
    pd.DataFrame(
        [
            {"Shell": "P1", "N1": "N1", "N2": "N2", "N3": "N3",
                "N4": "N4", "Material": "CONC", "Thickness": 0.2},
            {"Shell": "P2", "N1": "N2", "N2": "N3", "N3": "N4",
                "N4": "N1", "Material": "CONC", "Thickness": 0.25},
        ]
    ).to_csv(tmp_path / "elements_2d.csv", index=False)
    pd.DataFrame(
        [
            {"EntityType": "element", "EntityId": "B1",
                "PropertyName": "axial_capacity", "PropertyValue": 20.0},
            {"EntityType": "element", "EntityId": "P1",
                "PropertyName": "design_strength", "PropertyValue": 10.0},
            {"EntityType": "element", "EntityId": "P2",
                "PropertyName": "design_strength", "PropertyValue": 20.0},
        ]
    ).to_csv(tmp_path / "properties.csv", index=False)
    pd.DataFrame(
        [
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
            {
                "Case": "LC1",
                "ObjectType": "1D",
                "ObjectId": "B1",
                "Node": None,
                "Station": 1.0,
                "Result": "axial_force",
                "Value": 8.0,
                "Location": "element",
            },
            {
                "Case": "LC1",
                "ObjectType": "2D",
                "ObjectId": "P1",
                "Node": "N2",
                "Station": None,
                "Result": "membrane_force",
                "Value": 12.0,
                "Location": "node",
            },
            {
                "Case": "LC1",
                "ObjectType": "2D",
                "ObjectId": "P1",
                "Node": "N3",
                "Station": None,
                "Result": "membrane_force",
                "Value": 8.0,
                "Location": "node",
            },
            {
                "Case": "LC1",
                "ObjectType": "2D",
                "ObjectId": "P2",
                "Node": "N2",
                "Station": None,
                "Result": "membrane_force",
                "Value": 20.0,
                "Location": "node",
            },
            {
                "Case": "LC1",
                "ObjectType": "2D",
                "ObjectId": "P2",
                "Node": "N3",
                "Station": None,
                "Result": "membrane_force",
                "Value": 16.0,
                "Location": "node",
            },
        ]
    ).to_csv(tmp_path / "results.csv", index=False)

    importer = ImportModelService()
    model = importer.import_model(CsvImportProfile.SAP2000, tmp_path)

    task_service = TaskExecutionService()
    result_service = ResultQueryService()

    bar_selection = SelectionContext(
        element_type=ElementType.BAR_1D,
        selected_element_ids=("B1",),
    )
    bar_result = task_service.execute(
        ExampleBarCheckPlugin(), model, bar_selection, "LC1")
    bar_view = result_service.process(
        bar_result,
        VisualizationCriteria(result_name="utilization",
                              case_id="LC1", mode=VisualizationMode.ELEMENT),
        bar_selection,
    )
    assert bar_view.iloc[0]["value"] == 0.5

    shell_selection = SelectionContext(
        element_type=ElementType.SHELL_2D,
        selected_element_ids=("P1",),
        adjacent_element_ids=("P2",),
    )
    shell_result = task_service.execute(
        ExampleShellDesignPlugin(), model, shell_selection, "LC1")
    shell_view = result_service.process(
        shell_result,
        VisualizationCriteria(
            result_name="required_thickness",
            case_id="LC1",
            mode=VisualizationMode.NODE_AVERAGED,
            averaging_policy=ResultAveragingPolicy(
                include_adjacent_for_2d_average=True),
        ),
        shell_selection,
    )
    averaged = dict(zip(shell_view["node_id"],
                    shell_view["value"], strict=False))
    assert averaged["N2"] == 1.1
    assert averaged["N3"] == 0.8
