from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.result_data import ResultData
    from civil_3P.core.selection_context import SelectionContext
    from civil_3P.tasks.task_result import TaskResult


class ResultBuilder(ABC):
    @abstractmethod
    def process(
        self,
        task_result: TaskResult,
        selection: SelectionContext,
        model: Model,
    ) -> ResultData:
        raise NotImplementedError()
