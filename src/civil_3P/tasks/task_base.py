from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd

from civil_3P.standard import model_components as mc
from civil_3P.core.model import FEMModel


@dataclass(frozen=True, slots=True)
class TaskMetadata:
    identifier: str
    display_name: str
    supported_element_type: mc.ModelComponents
    version: str = "0.1.0"


@dataclass(frozen=True, slots=True)
class TaskContext:
    full_model: FEMModel
    selection_model: FEMModel
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
                 element_type: mc.ModelComponents) -> bool:
        return self.metadata.supported_element_type == element_type

    @abstractmethod
    def validate_input(self,
                       context: TaskContext) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute(self,
                context: TaskContext) -> TaskResult:
        raise NotImplementedError
