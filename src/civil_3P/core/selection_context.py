from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class SelectionContext:
    node_ids: set[str]
    element_1d_ids: set[str]
    element_2d_ids: set[str]
    adjacent_element_2d_ids: set[str] = field(default_factory=set)

    @property
    def all_element_2d_ids(self) -> set[str]:
        return self.element_2d_ids | self.adjacent_element_2d_ids
