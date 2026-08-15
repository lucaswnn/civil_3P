from __future__ import annotations

from pathlib import Path

import pandas as pd

from civil_3P.standard import model_representation as rpr
from civil_3P.utils.pandas_utils import PandasUtils as pdUtils
from civil_3P.standard import units
from civil_3P.importers.importer_adapter import (
    ImporterAdapter,
    ColumnMapping,
    ImporterSpec,
    IntermediateRepresentation,
)


SAP2000_SPEC = ImporterSpec(

    tables_mapping={
        rpr.ModelTables.NODES: ColumnMapping(
            rename={
                "Joint": rpr.NodesColumns.NODE,
                "GlobalX": rpr.NodesColumns.X,
                "GlobalY": rpr.NodesColumns.Y,
                "GlobalZ": rpr.NodesColumns.Z,
            },
            defaults={},
        ),
        rpr.ModelTables.ELEMENTS_1D: ColumnMapping(
            rename={
                "Frame": rpr.Elements1DColumns.ELEMENT,
                "JointI": rpr.Elements1DColumns.NODE_I,
                "JointJ": rpr.Elements1DColumns.NODE_J,
                "Material": rpr.Elements1DColumns.MATERIAL,
                "AnalSect": rpr.Elements1DColumns.SECTION,
            },
            defaults={
                rpr.Elements1DColumns.MATERIAL: None,
                rpr.Elements1DColumns.SECTION: None,
            },
        ),
        rpr.ModelTables.ELEMENTS_2D: ColumnMapping(
            rename={
                "Area": rpr.Elements2DColumns.ELEMENT,
                "Joint1": rpr.Elements2DColumns.NODE_1,
                "Joint2": rpr.Elements2DColumns.NODE_2,
                "Joint3": rpr.Elements2DColumns.NODE_3,
                "Joint4": rpr.Elements2DColumns.NODE_4,
                "Material": rpr.Elements2DColumns.MATERIAL,
                "Thickness": rpr.Elements2DColumns.THICKNESS,
            },
            defaults={
                rpr.Elements2DColumns.NODE_4: None,
                rpr.Elements2DColumns.MATERIAL: None,
                rpr.Elements2DColumns.THICKNESS: None,
            },
        ),
        rpr.ModelTables.MATERIALS: ColumnMapping(
            rename={
                "Material": rpr.MaterialsColumns.MATERIAL,
                "E1": rpr.MaterialsColumns.YOUNG_MODULUS,
                "G12": rpr.MaterialsColumns.SHEAR_MODULUS,
                "U12": rpr.MaterialsColumns.POISSON_RATIO,
                "A1": rpr.MaterialsColumns.THERMAL_COEFF,
            },
            defaults={
                rpr.MaterialsColumns.YOUNG_MODULUS: 0.0,
                rpr.MaterialsColumns.SHEAR_MODULUS: 0.0,
                rpr.MaterialsColumns.POISSON_RATIO: 0.0,
                rpr.MaterialsColumns.THERMAL_COEFF: 0.0,
            },
        ),
        rpr.ModelTables.SECTIONS: ColumnMapping(
            rename={
                "SectionName": rpr.SectionsColumns.SECTION,
                "Area": rpr.SectionsColumns.AREA,
                "I22": rpr.SectionsColumns.INERTIA_22,
                "I33": rpr.SectionsColumns.INERTIA_33,
            },
            defaults={
                rpr.SectionsColumns.AREA: 0.0,
                rpr.SectionsColumns.INERTIA_22: 0.0,
                rpr.SectionsColumns.INERTIA_33: 0.0,
            },
        ),
        rpr.ModelTables.ORIGIN_1D_RESULTS: ColumnMapping(
            rename={
                "OutputCase": rpr.Origin1DResultsColumns.CASE,
                "Frame": rpr.Origin1DResultsColumns.ELEMENT,
                "Station": rpr.Origin1DResultsColumns.STATION,
                "P": rpr.Origin1DResultsColumns.NORMAL,
                "V2": rpr.Origin1DResultsColumns.SHEAR_2,
                "V3": rpr.Origin1DResultsColumns.SHEAR_3,
                "T": rpr.Origin1DResultsColumns.TORSION,
                "M2": rpr.Origin1DResultsColumns.BENDING_2,
                "M3": rpr.Origin1DResultsColumns.BENDING_3,
            },
            defaults={},
        ),
        rpr.ModelTables.ORIGIN_2D_RESULTS: ColumnMapping(
            rename={
                "OutputCase": rpr.Origin2DResultsColumns.CASE,
                "Area": rpr.Origin2DResultsColumns.ELEMENT,
                "Joint": rpr.Origin2DResultsColumns.NODE,
                "F11": rpr.Origin2DResultsColumns.NORMAL_11,
                "F22": rpr.Origin2DResultsColumns.NORMAL_22,
                "F12": rpr.Origin2DResultsColumns.NORMAL_12,
                "M11": rpr.Origin2DResultsColumns.BENDING_11,
                "M22": rpr.Origin2DResultsColumns.BENDING_22,
                "M12": rpr.Origin2DResultsColumns.BENDING_12,
                "V13": rpr.Origin2DResultsColumns.SHEAR_13,
                "V23": rpr.Origin2DResultsColumns.SHEAR_23,
            },
            defaults={},
        ),
        rpr.ModelTables.ORIGIN_NODE_DISPLACEMENTS: ColumnMapping(
            rename={
                "OutputCase": rpr.OriginNodeDisplacementsColumns.CASE,
                "Joint": rpr.OriginNodeDisplacementsColumns.NODE,
                "U1": rpr.OriginNodeDisplacementsColumns.DX,
                "U2": rpr.OriginNodeDisplacementsColumns.DY,
                "U3": rpr.OriginNodeDisplacementsColumns.DZ,
                "R1": rpr.OriginNodeDisplacementsColumns.RX,
                "R2": rpr.OriginNodeDisplacementsColumns.RY,
                "R3": rpr.OriginNodeDisplacementsColumns.RZ,
            },
            defaults={},
        ),
        rpr.ModelTables.ORIGIN_NODE_REACTIONS: ColumnMapping(
            rename={
                "OutputCase": rpr.OriginNodeReactionsColumns.CASE,
                "Joint": rpr.OriginNodeReactionsColumns.NODE,
                "F1": rpr.OriginNodeReactionsColumns.FX,
                "F2": rpr.OriginNodeReactionsColumns.FY,
                "F3": rpr.OriginNodeReactionsColumns.FZ,
                "M1": rpr.OriginNodeReactionsColumns.MX,
                "M2": rpr.OriginNodeReactionsColumns.MY,
                "M3": rpr.OriginNodeReactionsColumns.MZ,
            },
            defaults={},
        ),
        rpr.ModelTables.LOAD_CASES: ColumnMapping(
            rename={
                "Case": rpr.LoadCasesColumns.CASE,
                "Notes": rpr.LoadCasesColumns.DESCRIPTION,
            },
            defaults={
                rpr.LoadCasesColumns.DESCRIPTION: "",
            },
        ),
    },
)


class Sap2000Importer(ImporterAdapter):
    def __init__(self) -> None:
        unit_map = {
            "m": units.LengthUnits.METER,
            "mm": units.LengthUnits.MILLIMETER,
            "cm": units.LengthUnits.CENTIMETER,
            "Degrees": units.AngleUnits.DEGREE,
            "Radians": units.AngleUnits.RADIAN,
            "Tonf": units.ForceUnits.TON_FORCE,
            "Tonf-m": units.MomentUnits.TON_FORCE_METER,
            "Tonf/m": units.ForcePerLengthUnits.TON_FORCE_PER_METER,
            "Tonf-m/m": units.MomentPerLengthUnits.TON_FORCE_METER_PER_METER,
            "Text": units.Unitless.NONE,
            "Tonf/m2": units.StressUnits.TON_FORCE_PER_SQUARE_METER,
            "Unitless": units.Unitless.UNITLESS,
            "1/C": units.LinearThermalExpansionUnits.PER_CELSIUS,
            "m2": units.AreaUnits.SQUARE_METER,
            "m3": units.VolumeUnits.CUBIC_METER,
            "m4": units.InertiaUnits.METER_FOURTH,
        }
        super().__init__(spec=SAP2000_SPEC, unit_map=unit_map)

        self.intermediate = IntermediateRepresentation.empty()
        self.original_tables: dict[str, pd.DataFrame] = {}

    def read_intermediate(self, source: str | Path) -> IntermediateRepresentation:
        print("Reading SAP2000 model from workbook")
        source_path = Path(source)

        if source_path.is_dir():
            raise ValueError(
                f"Expected a file path for SAP2000 import, but got a directory: {source_path}"
            )

        self._read_sap_tables_from_workbook(source_path)
        return self._build_intermediate()

    def _build_table(
            self,
            table_name: str,
            keep_columns: list[str],
            model_table: str,
            concat_columns_on_first: list[str] | None = None,
    ) -> None:
        table, table_units_dict = self._get_table(table_name)
        if concat_columns_on_first:
            table[concat_columns_on_first[0]] = (
                table[concat_columns_on_first[0]] +
                table[concat_columns_on_first[1]]
                .fillna('')
                .apply(lambda x: f" - {x}" if x else '')
            )

        pdUtils.keep_columns(
            table,
            keep_columns,
        )
        self.process_units(table, table_units_dict)
        self.map_dataframe(table, self._spec.tables_mapping[model_table])
        pdUtils.ensure_columns(
            table,
            list(self.intermediate.tables_dict[model_table].columns),
        )
        self.intermediate.tables_dict[model_table] = table

    def _join_and_build_tables(
        self,
            main_table_name: str,
            table_key_merge_mapping: dict[str, str],
            keep_columns: list[str],
            main_model_table: str,
            rename_other_tables_columns_mapping: dict[str,
                                                      dict[str, str]] | None = None,
    ) -> None:
        main_table, main_table_units_dict = self._get_table(main_table_name)

        for key_table_name, merge_key in table_key_merge_mapping.items():
            key_table, key_table_units_dict = self._get_table(key_table_name)
            if (rename_other_tables_columns_mapping
                    and key_table_name in rename_other_tables_columns_mapping.keys()):
                key_table = key_table.rename(
                    columns=rename_other_tables_columns_mapping[key_table_name]
                )

            if not key_table.empty:
                main_table = main_table.merge(
                    key_table,
                    on=merge_key,
                    how="left",
                )
                main_table_units_dict.update(key_table_units_dict)

        pdUtils.keep_columns(
            main_table,
            keep_columns,
        )
        self.process_units(main_table, main_table_units_dict)
        self.map_dataframe(
            main_table,
            self._spec.tables_mapping[main_model_table],
        )
        pdUtils.ensure_columns(
            main_table,
            list(
                self
                .intermediate
                .tables_dict[main_model_table].columns
            ),
        )

        self.intermediate.tables_dict[main_model_table] = main_table

    def _process_load_cases(self) -> None:
        load_case, load_case_units = self._get_table("Load Case Definitions")
        pdUtils.keep_columns(
            load_case,
            [
                "Case",
                "Notes",
            ],
        )
        combs, _ = self._get_table("Combination Definitions")
        combs.dropna(subset=["ComboType"], inplace=True)

        def concat_case_names(row):
            if row["ComboType"] == "Envelope":
                return [f"{row['ComboName']} - Max", f"{row['ComboName']} - Min"]

            return [row['ComboName']]

        combs["Case"] = combs.apply(concat_case_names, axis=1)

        combs = combs.explode("Case")
        pdUtils.keep_columns(
            combs,
            [
                "Case",
                "Notes",
            ],
        )
        load_case = pd.concat(
            [load_case, combs],
            ignore_index=True,
            sort=False,
        ).drop_duplicates(subset=["Case"])
        self.process_units(load_case, load_case_units)
        self.map_dataframe(
            load_case, self._spec.tables_mapping[rpr.ModelTables.LOAD_CASES])
        pdUtils.ensure_columns(
            load_case,
            list(
                self.intermediate.tables_dict[rpr.ModelTables.LOAD_CASES].columns),
        )
        self.intermediate.tables_dict[rpr.ModelTables.LOAD_CASES] = load_case

    def _build_intermediate(self) -> IntermediateRepresentation:
        print("Building intermediate representation from SAP2000 tables")

        self._build_table(
            table_name="Joint Coordinates",
            keep_columns=[
                "Joint",
                "GlobalX",
                "GlobalY",
                "GlobalZ",
            ],
            model_table=rpr.ModelTables.NODES,
        )

        self._build_table(
            table_name="MatProp 02 - Basic Mech Props",
            keep_columns=[
                "Material",
                "E1",
                "G12",
                "U12",
                "A1",
            ],
            model_table=rpr.ModelTables.MATERIALS,
        )

        self._build_table(
            table_name="Frame Props 01 - General",
            keep_columns=[
                "SectionName",
                "Area",
                "I22",
                "I33",
            ],
            model_table=rpr.ModelTables.SECTIONS,
        )

        self._join_and_build_tables(
            main_table_name="Connectivity - Frame",
            table_key_merge_mapping={
                "Frame Section Assignments": "Frame",
                "Frame Props 01 - General": "AnalSect",
            },
            keep_columns=[
                "Frame",
                "JointI",
                "JointJ",
                "Material",
                "AnalSect",
            ],
            main_model_table=rpr.ModelTables.ELEMENTS_1D,
            rename_other_tables_columns_mapping={
                "Frame Props 01 - General": {
                    "SectionName": "AnalSect",
                },
            },
        )

        self._join_and_build_tables(
            main_table_name="Connectivity - Area",
            table_key_merge_mapping={
                "Area Section Assignments": "Area",
                "Area Section Properties": "Section",
            },
            keep_columns=[
                "Area",
                "Joint1",
                "Joint2",
                "Joint3",
                "Joint4",
                "Material",
                "Thickness",
            ],
            main_model_table=rpr.ModelTables.ELEMENTS_2D,
        )

        self._build_table(
            table_name="Element Forces - Frames",
            keep_columns=[
                "Frame",
                "Station",
                "OutputCase",
                "P",
                "V2",
                "V3",
                "T",
                "M2",
                "M3",
            ],
            model_table=rpr.ModelTables.ORIGIN_1D_RESULTS,
            concat_columns_on_first=["OutputCase", "StepType"]
        )

        self._build_table(
            table_name="Element Forces - Area Shells",
            keep_columns=[
                "Area",
                "Joint",
                "OutputCase",
                "F11",
                "F22",
                "F12",
                "M11",
                "M22",
                "M12",
                "V13",
                "V23",
            ],
            model_table=rpr.ModelTables.ORIGIN_2D_RESULTS,
            concat_columns_on_first=["OutputCase", "StepType"],
        )

        self._build_table(
            table_name="Joint Displacements",
            keep_columns=[
                "OutputCase",
                "Joint",
                "U1",
                "U2",
                "U3",
                "R1",
                "R2",
                "R3",
            ],
            model_table=rpr.ModelTables.ORIGIN_NODE_DISPLACEMENTS,
            concat_columns_on_first=["OutputCase", "StepType"],
        )

        self._build_table(
            table_name="Joint Reactions",
            keep_columns=[
                "OutputCase",
                "Joint",
                "F1",
                "F2",
                "F3",
                "M1",
                "M2",
                "M3",
            ],
            model_table=rpr.ModelTables.ORIGIN_NODE_REACTIONS,
            concat_columns_on_first=["OutputCase", "StepType"],
        )

        self._process_load_cases()

        return self.intermediate

    def _read_sap_tables_from_workbook(
        self,
        workbook_path: Path,
    ) -> None:
        try:
            sheets = pd.read_excel(
                workbook_path,
                sheet_name=None,
                header=None,
                dtype=object,
                decimal=",",
            )
            print(f"Successfully read {len(sheets)} sheets from workbook")
            self.original_tables = sheets
        except ImportError as exc:
            raise RuntimeError(
                "Excel engine is missing. Install xlrd/openpyxl to import SAP2000 XLS files."
            ) from exc

    def _get_table(
        self,
        name: str,
    ) -> tuple[pd.DataFrame, dict[str, str]]:
        print(f"Retrieving table '{name}' from SAP2000 tables")
        table = self.original_tables.get(name).copy()
        if table is None:
            raise ValueError(
                f"Table '{name}' not found in the provided tables.")

        columns = table.iloc[1].to_list()
        units = table.iloc[2].to_list()
        units_dict = dict(zip(columns, units))
        table.columns = columns
        table.drop(table.index[:3], inplace=True)
        table.reset_index(drop=True, inplace=True)
        return table, units_dict
