from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd

from civil_3P.core.enums import ElementType, TaskType
from civil_3P.core.model import FEMModel
from civil_3P.core.selection import SelectionContext


@dataclass(frozen=True, slots=True)
class TaskMetadata:
    identifier: str
    display_name: str
    task_type: TaskType
    supported_element_type: ElementType
    version: str = "0.1.0"


@dataclass(frozen=True, slots=True)
class TaskContext:
    model: FEMModel
    selection: SelectionContext
    case_id: str


@dataclass(frozen=True, slots=True)
class TaskResult:
    metadata: TaskMetadata
    results: pd.DataFrame
    report: pd.DataFrame


class TaskPlugin(ABC):
    @property
    @abstractmethod
    def metadata(self) -> TaskMetadata:
        raise NotImplementedError

    def supports(self,
                 element_type: ElementType) -> bool:
        return self.metadata.supported_element_type == element_type

    @abstractmethod
    def validate_input(self,
                       context: TaskContext) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute(self,
                context: TaskContext) -> TaskResult:
        raise NotImplementedError
