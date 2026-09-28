from __future__ import annotations

import pandas as pd
import pytest
from conftest import build_small_model

from civil_3P.core.result_builder_registry import ResultBuilderRegistry
from civil_3P.core.selection_context import SelectionContext
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.result_components import ViewContentKind as vk
from civil_3P.standard.task_result_representation import TaskNodeResultsColumns as tnode
from civil_3P.tasks.task_metadata import TaskMetadata
from civil_3P.tasks.task_result import TaskResult

NODE_METADATA = TaskMetadata(
    identifier="node_task",
    display_name="Node task",
    supported_element_type=mc.NODES,
)


class TestResultBuilderRegistry:
    @classmethod
    def setup_class(cls) -> None:
        cls.model = build_small_model()
        cls.registry = ResultBuilderRegistry()

    def test_dispatches_to_node_builder(self) -> None:
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
            node_ids={"N1"},
            element_1d_ids=set(),
            element_2d_ids=set(),
        )

        data = self.registry.build_result(
            task_result,
            selection,
            self.model,
            vk.NODE_POINTS,
        )

        assert data.element_type == mc.NODES

    def test_unknown_view_content_kind_raises_key_error(
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
            node_ids={"N1"},
            element_1d_ids=set(),
            element_2d_ids=set(),
        )

        with pytest.raises(KeyError):
            self.registry.build_result(
                task_result,
                selection,
                self.model,
                "not_a_real_kind",
            )
