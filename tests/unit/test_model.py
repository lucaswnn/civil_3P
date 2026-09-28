from __future__ import annotations

import pandas as pd
import pytest
from conftest import build_small_model

from civil_3P.core.model import Model
from civil_3P.core.sel_context import SelContext
from civil_3P.standard.model_repr import ModelTables as mt
from civil_3P.standard.units import DEFAULT_UNITS


class TestModel:
    @classmethod
    def setup_class(cls) -> None:
        cls.valid_units = DEFAULT_UNITS.copy()

    def setup_method(self) -> None:
        self.model = build_small_model()

    def test_empty_has_required_tables_and_units(self) -> None:
        model = Model.empty()

        assert set(model.tables.keys()) == set(mt)
        assert all(df.empty for df in model.tables.values())
        assert model.units == DEFAULT_UNITS

    def test_from_tables_success(self) -> None:
        model = Model.from_tables(
            tables=self.model.tables,
            units=self.valid_units,
        )

        assert model.tables[mt.NODES].shape[0] == 5
        assert model.tables[mt.BARS].shape[0] == 1
        assert model.tables[mt.SHELLS].shape[0] == 2

    def test_from_tables_missing_table_raises(self) -> None:
        incomplete_tables = {
            k: v for k, v in self.model.tables.items() if k != mt.SECTIONS
        }

        with pytest.raises(ValueError, match="Missing tables"):
            Model.from_tables(tables=incomplete_tables, units=self.valid_units)

    def test_from_tables_missing_unit_raises(self) -> None:
        units_missing_length = {
            k: v for k, v in self.valid_units.items() if k != "length"
        }

        with pytest.raises(ValueError, match="Missing units"):
            Model.from_tables(
                tables=self.model.tables,
                units=units_missing_length,
            )

    def test_from_tables_invalid_unit_raises(self) -> None:
        invalid_units = self.valid_units.copy()
        invalid_units["length"] = "not-a-unit"

        with pytest.raises(ValueError, match="Invalid unit"):
            Model.from_tables(tables=self.model.tables, units=invalid_units)

    def test_to_dict_from_dict_roundtrip(self) -> None:
        data = self.model.to_dict()
        rebuilt = Model.from_dict(data)

        pd.testing.assert_frame_equal(
            rebuilt.tables[mt.NODES].reset_index(drop=True),
            self.model.tables[mt.NODES].reset_index(drop=True),
        )
        assert rebuilt.units == self.model.units

    def test_copy_is_independent_from_original(self) -> None:
        copied = self.model.copy()
        copied.tables[mt.NODES] = copied.tables[mt.NODES].iloc[0:0]

        assert self.model.tables[mt.NODES].shape[0] == 5
        assert copied.tables[mt.NODES].shape[0] == 0

    def test_filter_by_selection_keeps_only_selected(self) -> None:
        selection = SelContext(
            node_ids={"N1", "N2"},
            bar_ids={"F1"},
            shell_ids=set(),
        )
        filtered = self.model.filter_by_selection(selection)

        assert filtered.tables[mt.BARS].shape[0] == 1
        assert filtered.tables[mt.SHELLS].shape[0] == 0

    def test_filter_by_selection_reversed_keeps_complement(self) -> None:
        selection = SelContext(
            node_ids=set(),
            bar_ids={"F1"},
            shell_ids=set(),
        )
        filtered = self.model.filter_by_selection_reversed(selection)

        assert filtered.tables[mt.BARS].shape[0] == 0
        assert filtered.tables[mt.SHELLS].shape[0] == 2

    def test_filter_by_selection_with_unknown_ids_is_empty(self) -> None:
        selection = SelContext(
            node_ids={"UNKNOWN"},
            bar_ids={"UNKNOWN"},
            shell_ids={"UNKNOWN"},
        )
        filtered = self.model.filter_by_selection(selection)

        assert filtered.tables[mt.BARS].empty
        assert filtered.tables[mt.SHELLS].empty

    def test_filter_by_load_case(self) -> None:
        filtered = self.model.filter_by_load_case("DEAD")

        assert (filtered.tables[mt.BAR_RESULTS]["case"] == "DEAD").all()
        assert filtered.tables[mt.SHELL_RESULTS].shape[0] == 7

    def test_filter_by_unknown_load_case_is_empty(self) -> None:
        filtered = self.model.filter_by_load_case("UNKNOWN")

        assert filtered.tables[mt.BAR_RESULTS].empty
        assert filtered.tables[mt.SHELL_RESULTS].empty

    def test_remove_elements_drops_orphan_nodes(self) -> None:
        selection = SelContext(
            node_ids=set(),
            bar_ids=set(),
            shell_ids={"A2"},
        )
        result = self.model.remove_elements(selection)

        assert result.tables[mt.SHELLS].shape[0] == 1

        remaining_nodes = set(result.tables[mt.NODES]["node"])
        assert remaining_nodes == {"N1", "N2", "N3", "N4"}
