from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.core.model import Model


@dataclass(frozen=True, slots=True)
class TaskInputContext:
    full_model: Model
    selection_model: Model
    case_id: str
