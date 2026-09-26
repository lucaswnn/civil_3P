from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

    from civil_3P.tasks.task_metadata import TaskMetadata


@dataclass(frozen=True, slots=True)
class TaskResult:
    metadata: TaskMetadata
    results: pd.DataFrame
