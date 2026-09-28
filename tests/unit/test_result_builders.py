from __future__ import annotations

import pandas as pd
import pytest
from conftest import build_small_model

from civil_3P.core.bar_res_builder import BarResBuilder
from civil_3P.core.node_res_builder import NodeResBuilder
from civil_3P.core.sel_context import SelContext
from civil_3P.core.shell_isolated_res_builder import (
    ShellIsolatedResBuilder,
)
from civil_3P.core.shell_shared_res_builder import ShellSharedResBuilder
from civil_3P.core.shell_uniform_res_builder import (
    ShellUniformResBuilder,
)
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.task_res_repr import TaskBarResCols as t1d
from civil_3P.standard.task_res_repr import TaskNodeResCols as tnode
from civil_3P.standard.task_res_repr import TaskShellResCols as t2d
from civil_3P.tasks.task_metadata import TaskMetadata
from civil_3P.tasks.task_res import TaskRes

NODE_METADATA = TaskMetadata(
    identifier="node_task",
    display_name="Node task",
    supported_element_type=mc.NODES,
)
BAR_METADATA = TaskMetadata(
    identifier="1d_task",
    display_name="1D task",
    supported_element_type=mc.BARS,
)
SHELL_METADATA = TaskMetadata(
    identifier="2d_task",
    display_name="2D task",
    supported_element_type=mc.SHELLS,
)


class TestResBuilders:
    @classmethod
    def setup_class(cls) -> None:
        cls.model = build_small_model()

    def setup_method(self) -> None:
        self.full_selection_1d = SelContext(
            node_ids={"N1", "N2"},
            bar_ids={"F1"},
            shell_ids=set(),
        )
        self.full_selection_2d = SelContext(
            node_ids={"N1", "N2", "N3", "N4", "N5"},
            bar_ids=set(),
            shell_ids={"A1", "A2"},
        )

    def test_node_res_builder_filters_by_selection(self) -> None:
        res_df = pd.DataFrame(
            {
                tnode.NODE: ["N1", "N2", "N3"],
                tnode.CASE: ["DEAD", "DEAD", "DEAD"],
                tnode.VALUE: [1.0, 2.0, 3.0],
            }
        )
        task_result = TaskRes(
            metadata=NODE_METADATA,
            results=res_df,
        )
        selection = SelContext(
            node_ids={"N1", "N2"},
            bar_ids=set(),
            shell_ids=set(),
        )

        data = NodeResBuilder().process(
            task_result,
            selection,
            self.model,
        )

        assert data.element_type == mc.NODES
        assert data.nodes == {"N1", "N2"}
        assert set(data.res_df[tnode.NODE]) == {"N1", "N2"}

    def test_node_res_builder_empty_selection_returns_empty(
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
            node_ids=set(),
            bar_ids=set(),
            shell_ids=set(),
        )

        data = NodeResBuilder().process(
            task_result,
            selection,
            self.model,
        )

        assert data.nodes == set()
        assert data.res_df.empty

    def test_bar_res_builder_collects_endpoint_nodes(
        self,
    ) -> None:
        res_df = pd.DataFrame(
            {
                t1d.ELEMENT: ["F1", "F1"],
                t1d.STATION: [0.0, 1.0],
                t1d.VALUE: [5.0, -5.0],
            }
        )
        task_result = TaskRes(
            metadata=BAR_METADATA,
            results=res_df,
        )

        data = BarResBuilder().process(
            task_result,
            self.full_selection_1d,
            self.model,
        )

        assert data.element_type == mc.BARS
        assert data.elements == {"F1"}
        assert data.nodes == {"N1", "N2"}

    def test_shell_uniform_builder_averages_per_element(
        self,
    ) -> None:
        res_df = pd.DataFrame(
            {
                t2d.ELEMENT: ["A1", "A1", "A1", "A1"],
                t2d.NODE: ["N1", "N2", "N3", "N4"],
                t2d.VALUE: [2.0, 3.0, 4.0, 5.0],
            }
        )
        task_result = TaskRes(
            metadata=SHELL_METADATA,
            results=res_df,
        )

        data = ShellUniformResBuilder().process(
            task_result,
            self.full_selection_2d,
            self.model,
        )

        assert data.res_df.shape[0] == 1
        assert data.res_df[t2d.VALUE].iloc[0] == pytest.approx(3.5)

    def test_shell_shared_builder_averages_per_node(
        self,
    ) -> None:
        res_df = pd.DataFrame(
            {
                t2d.ELEMENT: ["A1", "A2"],
                t2d.NODE: ["N2", "N2"],
                t2d.VALUE: [2.0, 4.0],
            }
        )
        task_result = TaskRes(
            metadata=SHELL_METADATA,
            results=res_df,
        )

        data = ShellSharedResBuilder().process(
            task_result,
            self.full_selection_2d,
            self.model,
        )

        assert data.res_df.shape[0] == 1
        assert data.res_df[t2d.VALUE].iloc[0] == pytest.approx(3.0)

    def test_shell_isolated_builder_keeps_all_rows(
        self,
    ) -> None:
        res_df = pd.DataFrame(
            {
                t2d.ELEMENT: ["A1", "A1", "A2"],
                t2d.NODE: ["N1", "N2", "N2"],
                t2d.VALUE: [2.0, 4.0, 3.0],
            }
        )
        task_result = TaskRes(
            metadata=SHELL_METADATA,
            results=res_df,
        )

        data = ShellIsolatedResBuilder().process(
            task_result,
            self.full_selection_2d,
            self.model,
        )

        assert data.res_df.shape[0] == 3

    def test_shell_builders_with_no_matching_elements_is_empty(
        self,
    ) -> None:
        res_df = pd.DataFrame(
            {
                t2d.ELEMENT: ["UNKNOWN"],
                t2d.NODE: ["N1"],
                t2d.VALUE: [1.0],
            }
        )
        task_result = TaskRes(
            metadata=SHELL_METADATA,
            results=res_df,
        )

        data = ShellUniformResBuilder().process(
            task_result,
            self.full_selection_2d,
            self.model,
        )

        assert data.elements == set()
        assert data.res_df.empty
