from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.core.bar_res_builder import BarResBuilder
from civil_3P.core.node_res_builder import NodeResBuilder
from civil_3P.core.shell_isolated_res_builder import (
    ShellIsolatedResBuilder,
)
from civil_3P.core.shell_shared_res_builder import ShellSharedResBuilder
from civil_3P.core.shell_uniform_res_builder import (
    ShellUniformResBuilder,
)
from civil_3P.standard.res_components import ResSceneKind as vk

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.res_builder import ResBuilder
    from civil_3P.core.res_data import ResData
    from civil_3P.core.sel_context import SelContext
    from civil_3P.tasks.task_res import TaskRes


class ResBuilderRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, ResBuilder] = {
            vk.NODE: NodeResBuilder(),
            vk.BAR_PROFILE: BarResBuilder(),
            vk.SHELL_UNIFORM: ShellUniformResBuilder(),
            vk.SHELL_SHARED_NODES: ShellSharedResBuilder(),
            vk.SHELL_ISOLATED_NODES: ShellIsolatedResBuilder(),
        }

    def build_result(
        self,
        task_result: TaskRes,
        selection: SelContext,
        model: Model,
        view_content_kind: vk,
    ) -> ResData:
        builder = self._registry[view_content_kind]

        return builder.process(
            task_result=task_result,
            selection=selection,
            model=model,
        )
