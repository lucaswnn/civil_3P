from __future__ import annotations

from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import TYPE_CHECKING


from civil_3P.core.result_data import ResultData
from civil_3P.standard.result_components import (
    Visualization2DMode,
)

if TYPE_CHECKING:
    from civil_3P.core.model import FEMModel
    from civil_3P.core.selection import SelectionContext
    from civil_3P.tasks.task_base import TaskResult


class ResultBuilder(ABC):

    @abstractmethod
    def process(
        self,
        task_result: TaskResult,
        selection: SelectionContext,
        model: FEMModel,
    ) -> ResultData:
        raise NotImplementedError()
