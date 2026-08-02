from __future__ import annotations

from dataclasses import dataclass, field

from civil_3P.core.enums import ElementType


@dataclass(frozen=True, slots=True)
class SelectionContext:
    element_type: ElementType
    selected_element_ids: tuple[str, ...]
    adjacent_element_ids: tuple[str, ...] = field(default_factory=tuple)

    @property
    def all_element_ids(self) -> tuple[str, ...]:
        ordered = dict.fromkeys((
            *self.selected_element_ids,
            *self.adjacent_element_ids,
        ))
        
        return tuple(ordered.keys())
