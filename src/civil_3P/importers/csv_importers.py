from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import pandas as pd

from civil_3P.core.enums import ElementType, ResultLocation
from civil_3P.core.model import FEMModel


class CsvImportProfile(StrEnum):
    SAP2000 = "sap2000"
    MIDAS_CIVIL = "midas_civil"
    SCIA_ENGINEER = "scia_engineer"


@dataclass(frozen=True, slots=True)
class ColumnMapping:
    rename: dict[str, str]
    defaults: dict[str, object]


@dataclass(frozen=True, slots=True)
class ImporterSpec:
    nodes: ColumnMapping
    elements_1d: ColumnMapping
    elements_2d: ColumnMapping
    results: ColumnMapping


class BaseCsvImporter:
    def __init__(self, spec: ImporterSpec, source_name: str) -> None:
        self._spec = spec
        self._source_name = source_name

    def import_from_directory(self, directory: str | Path) -> FEMModel:
        base_dir = Path(directory)
        nodes = self._read_csv(base_dir / "nodes.csv", self._spec.nodes)
        elements_1d = self._read_csv(
            base_dir / "elements_1d.csv", self._spec.elements_1d)
        elements_2d = self._read_csv(
            base_dir / "elements_2d.csv", self._spec.elements_2d)
        results = self._read_csv(base_dir / "results.csv", self._spec.results)
        properties = self._read_properties(base_dir / "properties.csv")
        overrides = pd.DataFrame(
            columns=["entity_type", "entity_id", "property_name", "property_value"])
        return FEMModel.from_tables(
            nodes=nodes,
            elements_1d=elements_1d,
            elements_2d=elements_2d,
            properties=properties,
            results=results,
            overrides=overrides,
        )

    def _read_csv(self, path: Path, mapping: ColumnMapping) -> pd.DataFrame:
        frame = pd.read_csv(path).rename(columns=mapping.rename)
        for key, value in mapping.defaults.items():
            if key not in frame.columns:
                frame[key] = value
        return frame

    def _read_properties(self, path: Path) -> pd.DataFrame:
        frame = pd.read_csv(path)
        return frame.rename(
            columns={
                "EntityType": "entity_type",
                "EntityId": "entity_id",
                "PropertyName": "property_name",
                "PropertyValue": "property_value",
                "ENTITY_TYPE": "entity_type",
                "ENTITY_ID": "entity_id",
                "PROPERTY_NAME": "property_name",
                "PROPERTY_VALUE": "property_value",
            }
        )


SAP2000_SPEC = ImporterSpec(
    nodes=ColumnMapping(
        rename={"Joint": "node_id", "X": "x", "Y": "y", "Z": "z"},
        defaults={},
    ),
    elements_1d=ColumnMapping(
        rename={
            "Frame": "element_id",
            "JointI": "node_i",
            "JointJ": "node_j",
            "Material": "material_id",
            "Section": "section_id",
        },
        defaults={},
    ),
    elements_2d=ColumnMapping(
        rename={
            "Shell": "element_id",
            "N1": "node_1",
            "N2": "node_2",
            "N3": "node_3",
            "N4": "node_4",
            "Material": "material_id",
            "Thickness": "thickness",
        },
        defaults={"node_4": None},
    ),
    results=ColumnMapping(
        rename={
            "Case": "case_id",
            "ObjectType": "element_type",
            "ObjectId": "element_id",
            "Node": "node_id",
            "Station": "station",
            "Result": "result_name",
            "Value": "value",
            "Location": "location",
        },
        defaults={"source": "sap2000"},
    ),
)

MIDAS_SPEC = ImporterSpec(
    nodes=ColumnMapping(
        rename={"NODE": "node_id", "X": "x", "Y": "y", "Z": "z"}, defaults={}),
    elements_1d=ColumnMapping(
        rename={"ELEM": "element_id", "NI": "node_i", "NJ": "node_j",
                "MATL": "material_id", "SECT": "section_id"},
        defaults={},
    ),
    elements_2d=ColumnMapping(
        rename={
            "ELEM": "element_id",
            "N1": "node_1",
            "N2": "node_2",
            "N3": "node_3",
            "N4": "node_4",
            "MATL": "material_id",
            "THK": "thickness",
        },
        defaults={"node_4": None},
    ),
    results=ColumnMapping(
        rename={
            "CASE": "case_id",
            "ELEMENT_TYPE": "element_type",
            "ELEMENT_ID": "element_id",
            "NODE_ID": "node_id",
            "STATION": "station",
            "RESULT_NAME": "result_name",
            "VALUE": "value",
            "LOCATION": "location",
        },
        defaults={"source": "midas_civil"},
    ),
)

SCIA_SPEC = ImporterSpec(
    nodes=ColumnMapping(
        rename={"Id": "node_id", "CoordX": "x", "CoordY": "y", "CoordZ": "z"},
        defaults={},
    ),
    elements_1d=ColumnMapping(
        rename={
            "MemberId": "element_id",
            "Node1": "node_i",
            "Node2": "node_j",
            "Material": "material_id",
            "CrossSection": "section_id",
        },
        defaults={},
    ),
    elements_2d=ColumnMapping(
        rename={
            "PlateId": "element_id",
            "Node1": "node_1",
            "Node2": "node_2",
            "Node3": "node_3",
            "Node4": "node_4",
            "Material": "material_id",
            "Thickness": "thickness",
        },
        defaults={"node_4": None},
    ),
    results=ColumnMapping(
        rename={
            "LoadCase": "case_id",
            "ElementType": "element_type",
            "ElementId": "element_id",
            "NodeId": "node_id",
            "Xi": "station",
            "ResultName": "result_name",
            "ResultValue": "value",
            "Location": "location",
        },
        defaults={"source": "scia_engineer"},
    ),
)


class ImporterRegistry:
    def __init__(self) -> None:
        self._registry = {
            CsvImportProfile.SAP2000: BaseCsvImporter(SAP2000_SPEC, "sap2000"),
            CsvImportProfile.MIDAS_CIVIL: BaseCsvImporter(MIDAS_SPEC, "midas_civil"),
            CsvImportProfile.SCIA_ENGINEER: BaseCsvImporter(SCIA_SPEC, "scia_engineer"),
        }

    def import_model(self, profile: CsvImportProfile, directory: str | Path) -> FEMModel:
        model = self._registry[profile].import_from_directory(directory)
        normalized = model.results.copy()
        normalized["element_type"] = normalized["element_type"].replace(
            {
                "1D": ElementType.BAR_1D.value,
                "2D": ElementType.SHELL_2D.value,
                "bar": ElementType.BAR_1D.value,
                "shell": ElementType.SHELL_2D.value,
            }
        )
        normalized["location"] = normalized["location"].replace(
            {"element": ResultLocation.ELEMENT.value,
                "node": ResultLocation.NODE.value}
        )
        model.results = normalized
        return model
