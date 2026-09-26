from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.standard.model_components import ModelComponents


@dataclass(frozen=True, slots=True)
class TaskMetadata:
    identifier: str
    display_name: str
    supported_element_type: ModelComponents
    version: str = "0.1.0"
