from __future__ import annotations

import dataclasses

import pytest

from civil_3P.core.selection_context import SelectionContext
from civil_3P.standard.model_representation import ModelTables as mt

from conftest import build_small_model


class TestSelectionContext:
    def test_all_element_2d_ids_defaults_to_empty_adjacent(self) -> None:
        selection = SelectionContext(
            node_ids=set(),
            element_1d_ids=set(),
            element_2d_ids={"A1"},
        )

        assert selection.all_element_2d_ids == {"A1"}

    def test_all_element_2d_ids_merges_adjacent(self) -> None:
        selection = SelectionContext(
            node_ids=set(),
            element_1d_ids=set(),
            element_2d_ids={"A1"},
            adjacent_element_2d_ids={"A2"},
        )

        assert selection.all_element_2d_ids == {"A1", "A2"}

    def test_is_frozen(self) -> None:
        selection = SelectionContext(
            node_ids=set(),
            element_1d_ids=set(),
            element_2d_ids=set(),
        )

        with pytest.raises(dataclasses.FrozenInstanceError):
            selection.node_ids = {"N1"}


class TestSelectionAgainstModel:
    def setup_method(self) -> None:
        self.model = build_small_model()

    def test_filter_by_selection_with_known_ids(self) -> None:
        selection = SelectionContext(
            node_ids=set(),
            element_1d_ids={"F1"},
            element_2d_ids=set(),
        )
        filtered = self.model.filter_by_selection(selection)

        assert filtered.tables[mt.ELEMENTS_1D].shape[0] == 1

    def test_filter_by_selection_with_unknown_ids_returns_empty(self) -> None:
        selection = SelectionContext(
            node_ids=set(),
            element_1d_ids={"DOES_NOT_EXIST"},
            element_2d_ids=set(),
        )
        filtered = self.model.filter_by_selection(selection)

        assert filtered.tables[mt.ELEMENTS_1D].empty
