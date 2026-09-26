from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


@dataclass(frozen=True, slots=True)
class ColumnMapping:
    rename: dict[str, str]
    defaults: dict[str, Any]
