from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.importers.col_mapping import ColMapping


@dataclass(frozen=True, slots=True)
class ImporterSpec:
    tables_mapping: dict[str, ColMapping]
