from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.res_data import ResData
    from civil_3P.core.sel_context import SelContext
    from civil_3P.tasks.task_res import TaskRes


class ResBuilder(ABC):
    @abstractmethod
    def process(
        self,
        task_result: TaskRes,
        selection: SelContext,
        model: Model,
    ) -> ResData:
        raise NotImplementedError()
