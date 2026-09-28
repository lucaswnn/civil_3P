from __future__ import annotations

import pandas as pd
import pytest
from conftest import build_small_model

from civil_3P.core.res_builder_registry import ResBuilderRegistry
from civil_3P.core.sel_context import SelContext
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.res_components import ResSceneKind as vk
from civil_3P.standard.task_res_repr import TaskNodeResCols as tnode
from civil_3P.tasks.task_metadata import TaskMetadata
from civil_3P.tasks.task_res import TaskRes

NODE_METADATA = TaskMetadata(
    identifier="node_task",
    display_name="Node task",
    supported_element_type=mc.NODES,
)


class TestResBuilderRegistry:
    @classmethod
    def setup_class(cls) -> None:
        cls.model = build_small_model()
        cls.registry = ResBuilderRegistry()

    def test_dispatches_to_node_builder(self) -> None:
        res_df = pd.DataFrame(
            {
                tnode.NODE: ["N1"],
                tnode.CASE: ["DEAD"],
                tnode.VALUE: [1.0],
            }
        )
        task_result = TaskRes(
            metadata=NODE_METADATA,
            results=res_df,
        )
        selection = SelContext(
            node_ids={"N1"},
            bar_ids=set(),
            shell_ids=set(),
        )

        data = self.registry.build_result(
            task_result,
            selection,
            self.model,
            vk.NODE,
        )

        assert data.element_type == mc.NODES

    def test_unknown_view_content_kind_raises_key_error(
        self,
    ) -> None:
        res_df = pd.DataFrame(
            {
                tnode.NODE: ["N1"],
                tnode.CASE: ["DEAD"],
                tnode.VALUE: [1.0],
            }
        )
        task_result = TaskRes(
            metadata=NODE_METADATA,
            results=res_df,
        )
        selection = SelContext(
            node_ids={"N1"},
            bar_ids=set(),
            shell_ids=set(),
        )

        with pytest.raises(KeyError):
            self.registry.build_result(
                task_result,
                selection,
                self.model,
                "not_a_real_kind",
            )
