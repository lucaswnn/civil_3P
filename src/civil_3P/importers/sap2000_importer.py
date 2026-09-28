from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from civil_3P.importers.col_mapping import ColMapping
from civil_3P.importers.importer_adapter import ImporterAdapter
from civil_3P.importers.importer_spec import ImporterSpec
from civil_3P.importers.intermediate_repr import IntermediateRepr
from civil_3P.standard import model_repr as rpr
from civil_3P.standard import units
from civil_3P.standard.model_repr import ModelTables as mt
from civil_3P.utils.pandas_utils import PandasUtils as pdUtils

logger = logging.getLogger(__name__)

SAP2000_SPEC = ImporterSpec(
    tables_mapping={
        mt.NODES: ColMapping(
            rename={
                "Joint": rpr.NodeCols.NODE,
                "GlobalX": rpr.NodeCols.X,
                "GlobalY": rpr.NodeCols.Y,
                "GlobalZ": rpr.NodeCols.Z,
            },
            defaults={},
        ),
        mt.BARS: ColMapping(
            rename={
                "Frame": rpr.BarCols.ELEMENT,
                "JointI": rpr.BarCols.NODE_I,
                "JointJ": rpr.BarCols.NODE_J,
                "Material": rpr.BarCols.MATERIAL,
                "AnalSect": rpr.BarCols.SECTION,
            },
            defaults={
                rpr.BarCols.MATERIAL: None,
                rpr.BarCols.SECTION: None,
            },
        ),
        mt.SHELLS: ColMapping(
            rename={
                "Area": rpr.ShellCols.ELEMENT,
                "Joint1": rpr.ShellCols.NODE_1,
                "Joint2": rpr.ShellCols.NODE_2,
                "Joint3": rpr.ShellCols.NODE_3,
                "Joint4": rpr.ShellCols.NODE_4,
                "Material": rpr.ShellCols.MATERIAL,
                "Thickness": rpr.ShellCols.THICKNESS,
            },
            defaults={
                rpr.ShellCols.NODE_4: None,
                rpr.ShellCols.MATERIAL: None,
                rpr.ShellCols.THICKNESS: None,
            },
        ),
        mt.MATERIALS: ColMapping(
            rename={
                "Material": rpr.MaterialsCols.MATERIAL,
                "E1": rpr.MaterialsCols.YOUNG_MODULUS,
                "G12": rpr.MaterialsCols.SHEAR_MODULUS,
                "U12": rpr.MaterialsCols.POISSON_RATIO,
                "A1": rpr.MaterialsCols.THERMAL_COEFF,
            },
            defaults={
                rpr.MaterialsCols.YOUNG_MODULUS: 0.0,
                rpr.MaterialsCols.SHEAR_MODULUS: 0.0,
                rpr.MaterialsCols.POISSON_RATIO: 0.0,
                rpr.MaterialsCols.THERMAL_COEFF: 0.0,
            },
        ),
        mt.SECTIONS: ColMapping(
            rename={
                "SectionName": rpr.SectionsCols.SECTION,
                "Area": rpr.SectionsCols.AREA,
                "I22": rpr.SectionsCols.INERTIA_22,
                "I33": rpr.SectionsCols.INERTIA_33,
            },
            defaults={
                rpr.SectionsCols.AREA: 0.0,
                rpr.SectionsCols.INERTIA_22: 0.0,
                rpr.SectionsCols.INERTIA_33: 0.0,
            },
        ),
        mt.BAR_RESULTS: ColMapping(
            rename={
                "OutputCase": rpr.BarResCols.CASE,
                "Frame": rpr.BarResCols.ELEMENT,
                "Station": rpr.BarResCols.STATION,
                "P": rpr.BarResCols.NORMAL,
                "V2": rpr.BarResCols.SHEAR_2,
                "V3": rpr.BarResCols.SHEAR_3,
                "T": rpr.BarResCols.TORSION,
                "M2": rpr.BarResCols.BENDING_2,
                "M3": rpr.BarResCols.BENDING_3,
            },
            defaults={},
        ),
        mt.SHELL_RESULTS: ColMapping(
            rename={
                "OutputCase": rpr.ShellResCols.CASE,
                "Area": rpr.ShellResCols.ELEMENT,
                "Joint": rpr.ShellResCols.NODE,
                "F11": rpr.ShellResCols.NORMAL_11,
                "F22": rpr.ShellResCols.NORMAL_22,
                "F12": rpr.ShellResCols.NORMAL_12,
                "M11": rpr.ShellResCols.BENDING_11,
                "M22": rpr.ShellResCols.BENDING_22,
                "M12": rpr.ShellResCols.BENDING_12,
                "V13": rpr.ShellResCols.SHEAR_13,
                "V23": rpr.ShellResCols.SHEAR_23,
            },
            defaults={},
        ),
        mt.NODE_DISPLACEMENTS: ColMapping(
            rename={
                "OutputCase": rpr.NodeDisplacementsCols.CASE,
                "Joint": rpr.NodeDisplacementsCols.NODE,
                "U1": rpr.NodeDisplacementsCols.DX,
                "U2": rpr.NodeDisplacementsCols.DY,
                "U3": rpr.NodeDisplacementsCols.DZ,
                "R1": rpr.NodeDisplacementsCols.RX,
                "R2": rpr.NodeDisplacementsCols.RY,
                "R3": rpr.NodeDisplacementsCols.RZ,
            },
            defaults={},
        ),
        mt.NODE_REACTIONS: ColMapping(
            rename={
                "OutputCase": rpr.NodeReactionsCols.CASE,
                "Joint": rpr.NodeReactionsCols.NODE,
                "F1": rpr.NodeReactionsCols.FX,
                "F2": rpr.NodeReactionsCols.FY,
                "F3": rpr.NodeReactionsCols.FZ,
                "M1": rpr.NodeReactionsCols.MX,
                "M2": rpr.NodeReactionsCols.MY,
                "M3": rpr.NodeReactionsCols.MZ,
            },
            defaults={},
        ),
        mt.LOAD_CASES: ColMapping(
            rename={
                "Case": rpr.LoadCaseCols.CASE,
                "Notes": rpr.LoadCaseCols.DESCRIPTION,
            },
            defaults={
                rpr.LoadCaseCols.DESCRIPTION: "",
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

        self.intermediate = IntermediateRepr.empty()
        self.original_tables: dict[str, pd.DataFrame] = {}

    def read_intermediate(
        self,
        source: str | Path,
    ) -> IntermediateRepr:
        logger.info("Reading SAP2000 model from workbook")
        source_path = Path(source)

        if source_path.is_dir():
            raise ValueError(
                "Expected a file path for SAP2000 import, "
                f"but got a directory: {source_path}"
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
        table, table_units = self._get_table(table_name)

        if concat_columns_on_first:
            table[concat_columns_on_first[0]] = table[
                concat_columns_on_first[0]
            ] + table[concat_columns_on_first[1]].fillna("").apply(
                lambda x: f" - {x}" if x else ""
            )

        pdUtils.keep_columns(
            table,
            keep_columns,
        )
        self.process_units(table, table_units)
        self.map_dataframe(
            table,
            self._spec.tables_mapping[model_table],
        )
        pdUtils.ensure_columns(
            table,
            list(self.intermediate.tables[model_table].columns),
        )
        self.intermediate.tables[model_table] = table

    def _join_and_build_tables(
        self,
        main_table_name: str,
        table_key_merge_map: dict[str, str],
        keep_columns: list[str],
        main_model_table: str,
        rename_other_columns_map: dict[str, dict[str, str]] | None = None,
    ) -> None:
        main_table, main_table_units = self._get_table(main_table_name)

        for key_table_name, merge_key in table_key_merge_map.items():
            key_table, key_table_units = self._get_table(key_table_name)

            if (
                rename_other_columns_map
                and key_table_name in rename_other_columns_map.keys()
            ):
                key_table = key_table.rename(
                    columns=rename_other_columns_map[key_table_name]
                )

            if not key_table.empty:
                main_table = main_table.merge(
                    key_table,
                    on=merge_key,
                    how="left",
                )
                main_table_units.update(key_table_units)

        pdUtils.keep_columns(
            main_table,
            keep_columns,
        )
        self.process_units(main_table, main_table_units)
        self.map_dataframe(
            main_table,
            self._spec.tables_mapping[main_model_table],
        )
        pdUtils.ensure_columns(
            main_table,
            list(self.intermediate.tables[main_model_table].columns),
        )

        self.intermediate.tables[main_model_table] = main_table

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

            return [row["ComboName"]]

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
        self.map_dataframe(load_case, self._spec.tables_mapping[mt.LOAD_CASES])
        pdUtils.ensure_columns(
            load_case,
            list(self.intermediate.tables[mt.LOAD_CASES].columns),
        )
        self.intermediate.tables[mt.LOAD_CASES] = load_case

    def _build_intermediate(self) -> IntermediateRepr:
        logger.info("Building intermediate representation from SAP2000 tables")

        self._build_table(
            table_name="Joint Coordinates",
            keep_columns=[
                "Joint",
                "GlobalX",
                "GlobalY",
                "GlobalZ",
            ],
            model_table=mt.NODES,
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
            model_table=mt.MATERIALS,
        )

        self._build_table(
            table_name="Frame Props 01 - General",
            keep_columns=[
                "SectionName",
                "Area",
                "I22",
                "I33",
            ],
            model_table=mt.SECTIONS,
        )

        self._join_and_build_tables(
            main_table_name="Connectivity - Frame",
            table_key_merge_map={
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
            main_model_table=mt.BARS,
            rename_other_columns_map={
                "Frame Props 01 - General": {
                    "SectionName": "AnalSect",
                },
            },
        )

        self._join_and_build_tables(
            main_table_name="Connectivity - Area",
            table_key_merge_map={
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
            main_model_table=mt.SHELLS,
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
            model_table=mt.BAR_RESULTS,
            concat_columns_on_first=["OutputCase", "StepType"],
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
            model_table=mt.SHELL_RESULTS,
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
            model_table=mt.NODE_DISPLACEMENTS,
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
            model_table=mt.NODE_REACTIONS,
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
            logger.info(f"Successfully read {len(sheets)} sheets from workbook")
            self.original_tables = sheets

        except ImportError as exc:
            raise RuntimeError(
                "Excel engine is missing. Install xlrd/openpyxl "
                "to import SAP2000 XLS files."
            ) from exc

    def _get_table(
        self,
        name: str,
    ) -> tuple[pd.DataFrame, dict[str, str]]:
        logger.info(f"Retrieving table '{name}' from SAP2000 tables")
        table = self.original_tables.get(name).copy()

        if table is None:
            raise ValueError(f"Table '{name}' not found in the provided tables.")

        columns = table.iloc[1].to_list()
        units = table.iloc[2].to_list()
        units_dict = dict(zip(columns, units))
        table.columns = columns
        table.drop(table.index[:3], inplace=True)
        table.reset_index(drop=True, inplace=True)

        return table, units_dict
