from __future__ import annotations

from civil_3P.standard.result_components import ViewContentKind as vk
from civil_3P.core.result_builder import ResultBuilder
from civil_3P.core.node_result_builder import NodeResultBuilder
from civil_3P.core.element_1d_result_builder import Element1DResultBuilder
from civil_3P.core.element_2d_uniform_result_builder import (
    Element2DUniformResultBuilder,
)
from civil_3P.core.element_2d_shared_result_builder import Element2DSharedResultBuilder
from civil_3P.core.element_2d_isolated_result_builder import (
    Element2DIsolatedResultBuilder,
)
from civil_3P.tasks.task_base import TaskResult
from civil_3P.core.model import FEMModel
from civil_3P.core.selection import SelectionContext
from civil_3P.core.result_data import ResultData


class ResultBuilderRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, ResultBuilder] = {
            vk.NODE_POINTS: NodeResultBuilder(),
            vk.ELEMENT_1D_PROFILE: Element1DResultBuilder(),
            vk.ELEMENT_2D_UNIFORM: Element2DUniformResultBuilder(),
            vk.ELEMENT_2D_SHARED_NODES: Element2DSharedResultBuilder(),
            vk.ELEMENT_2D_ISOLATED_NODES: Element2DIsolatedResultBuilder(),
        }

    def build_result(
        self,
        task_result: TaskResult,
        selection: SelectionContext,
        model: FEMModel,
        view_content_kind: vk,
    ) -> ResultData:
        builder = self._registry[view_content_kind]
        return builder.process(
            task_result=task_result,
            selection=selection,
            model=model,
        )
