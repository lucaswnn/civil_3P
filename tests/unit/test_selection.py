from __future__ import annotations

import dataclasses

import pytest
from conftest import build_small_model

from civil_3P.core.sel_context import SelContext
from civil_3P.standard.model_repr import ModelTables as mt


class TestSelectionContext:
    def test_all_shell_ids_defaults_to_empty_adjacent(self) -> None:
        selection = SelContext(
            node_ids=set(),
            bar_ids=set(),
            shell_ids={"A1"},
        )

        assert selection.all_shell_ids == {"A1"}

    def test_all_shell_ids_merges_adjacent(self) -> None:
        selection = SelContext(
            node_ids=set(),
            bar_ids=set(),
            shell_ids={"A1"},
            adjacent_shell_ids={"A2"},
        )

        assert selection.all_shell_ids == {"A1", "A2"}

    def test_is_frozen(self) -> None:
        selection = SelContext(
            node_ids=set(),
            bar_ids=set(),
            shell_ids=set(),
        )

        with pytest.raises(dataclasses.FrozenInstanceError):
            selection.node_ids = {"N1"}


class TestSelectionAgainstModel:
    def setup_method(self) -> None:
        self.model = build_small_model()

    def test_filter_by_selection_with_known_ids(self) -> None:
        selection = SelContext(
            node_ids=set(),
            bar_ids={"F1"},
            shell_ids=set(),
        )
        filtered = self.model.filter_by_selection(selection)

        assert filtered.tables[mt.BARS].shape[0] == 1

    def test_filter_by_selection_with_unknown_ids_returns_empty(self) -> None:
        selection = SelContext(
            node_ids=set(),
            bar_ids={"DOES_NOT_EXIST"},
            shell_ids=set(),
        )
        filtered = self.model.filter_by_selection(selection)

        assert filtered.tables[mt.BARS].empty
