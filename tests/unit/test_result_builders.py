from __future__ import annotations

import pandas as pd
import pytest
from conftest import build_small_model

from civil_3P.core.element_1d_result_builder import Element1DResultBuilder
from civil_3P.core.element_2d_isolated_result_builder import (
    Element2DIsolatedResultBuilder,
)
from civil_3P.core.element_2d_shared_result_builder import Element2DSharedResultBuilder
from civil_3P.core.element_2d_uniform_result_builder import (
    Element2DUniformResultBuilder,
)
from civil_3P.core.node_result_builder import NodeResultBuilder
from civil_3P.core.selection_context import SelectionContext
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.task_result_representation import Task1DResultsColumns as t1d
from civil_3P.standard.task_result_representation import Task2DResultsColumns as t2d
from civil_3P.standard.task_result_representation import TaskNodeResultsColumns as tnode
from civil_3P.tasks.task_metadata import TaskMetadata
from civil_3P.tasks.task_result import TaskResult

NODE_METADATA = TaskMetadata(
    identifier="node_task",
    display_name="Node task",
    supported_element_type=mc.NODES,
)
ELEMENT_1D_METADATA = TaskMetadata(
    identifier="1d_task",
    display_name="1D task",
    supported_element_type=mc.ELEMENTS_1D,
)
ELEMENT_2D_METADATA = TaskMetadata(
    identifier="2d_task",
    display_name="2D task",
    supported_element_type=mc.ELEMENTS_2D,
)


class TestResultBuilders:
    @classmethod
    def setup_class(cls) -> None:
        cls.model = build_small_model()

    def setup_method(self) -> None:
        self.full_selection_1d = SelectionContext(
            node_ids={"N1", "N2"},
            element_1d_ids={"F1"},
            element_2d_ids=set(),
        )
        self.full_selection_2d = SelectionContext(
            node_ids={"N1", "N2", "N3", "N4", "N5"},
            element_1d_ids=set(),
            element_2d_ids={"A1", "A2"},
        )

    def test_node_result_builder_filters_by_selection(self) -> None:
        result_df = pd.DataFrame(
            {
                tnode.NODE: ["N1", "N2", "N3"],
                tnode.CASE: ["DEAD", "DEAD", "DEAD"],
                tnode.VALUE: [1.0, 2.0, 3.0],
            }
        )
        task_result = TaskResult(
            metadata=NODE_METADATA,
            results=result_df,
        )
        selection = SelectionContext(
            node_ids={"N1", "N2"},
            element_1d_ids=set(),
            element_2d_ids=set(),
        )

        data = NodeResultBuilder().process(
            task_result,
            selection,
            self.model,
        )

        assert data.element_type == mc.NODES
        assert data.nodes == {"N1", "N2"}
        assert set(data.result_df[tnode.NODE]) == {"N1", "N2"}

    def test_node_result_builder_empty_selection_returns_empty(
        self,
    ) -> None:
        result_df = pd.DataFrame(
            {
                tnode.NODE: ["N1"],
                tnode.CASE: ["DEAD"],
                tnode.VALUE: [1.0],
            }
        )
        task_result = TaskResult(
            metadata=NODE_METADATA,
            results=result_df,
        )
        selection = SelectionContext(
            node_ids=set(),
            element_1d_ids=set(),
            element_2d_ids=set(),
        )

        data = NodeResultBuilder().process(
            task_result,
            selection,
            self.model,
        )

        assert data.nodes == set()
        assert data.result_df.empty

    def test_element_1d_result_builder_collects_endpoint_nodes(
        self,
    ) -> None:
        result_df = pd.DataFrame(
            {
                t1d.ELEMENT: ["F1", "F1"],
                t1d.STATION: [0.0, 1.0],
                t1d.VALUE: [5.0, -5.0],
            }
        )
        task_result = TaskResult(
            metadata=ELEMENT_1D_METADATA,
            results=result_df,
        )

        data = Element1DResultBuilder().process(
            task_result,
            self.full_selection_1d,
            self.model,
        )

        assert data.element_type == mc.ELEMENTS_1D
        assert data.elements == {"F1"}
        assert data.nodes == {"N1", "N2"}

    def test_element_2d_uniform_builder_averages_per_element(
        self,
    ) -> None:
        result_df = pd.DataFrame(
            {
                t2d.ELEMENT: ["A1", "A1", "A1", "A1"],
                t2d.NODE: ["N1", "N2", "N3", "N4"],
                t2d.VALUE: [2.0, 3.0, 4.0, 5.0],
            }
        )
        task_result = TaskResult(
            metadata=ELEMENT_2D_METADATA,
            results=result_df,
        )

        data = Element2DUniformResultBuilder().process(
            task_result,
            self.full_selection_2d,
            self.model,
        )

        assert data.result_df.shape[0] == 1
        assert data.result_df[t2d.VALUE].iloc[0] == pytest.approx(3.5)

    def test_element_2d_shared_builder_averages_per_node(
        self,
    ) -> None:
        result_df = pd.DataFrame(
            {
                t2d.ELEMENT: ["A1", "A2"],
                t2d.NODE: ["N2", "N2"],
                t2d.VALUE: [2.0, 4.0],
            }
        )
        task_result = TaskResult(
            metadata=ELEMENT_2D_METADATA,
            results=result_df,
        )

        data = Element2DSharedResultBuilder().process(
            task_result,
            self.full_selection_2d,
            self.model,
        )

        assert data.result_df.shape[0] == 1
        assert data.result_df[t2d.VALUE].iloc[0] == pytest.approx(3.0)

    def test_element_2d_isolated_builder_keeps_all_rows(
        self,
    ) -> None:
        result_df = pd.DataFrame(
            {
                t2d.ELEMENT: ["A1", "A1", "A2"],
                t2d.NODE: ["N1", "N2", "N2"],
                t2d.VALUE: [2.0, 4.0, 3.0],
            }
        )
        task_result = TaskResult(
            metadata=ELEMENT_2D_METADATA,
            results=result_df,
        )

        data = Element2DIsolatedResultBuilder().process(
            task_result,
            self.full_selection_2d,
            self.model,
        )

        assert data.result_df.shape[0] == 3

    def test_element_2d_builders_with_no_matching_elements_is_empty(
        self,
    ) -> None:
        result_df = pd.DataFrame(
            {
                t2d.ELEMENT: ["UNKNOWN"],
                t2d.NODE: ["N1"],
                t2d.VALUE: [1.0],
            }
        )
        task_result = TaskResult(
            metadata=ELEMENT_2D_METADATA,
            results=result_df,
        )

        data = Element2DUniformResultBuilder().process(
            task_result,
            self.full_selection_2d,
            self.model,
        )

        assert data.elements == set()
        assert data.result_df.empty
