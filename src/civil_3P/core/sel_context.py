from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class SelContext:
    node_ids: set[str]
    bar_ids: set[str]
    shell_ids: set[str]
    adjacent_shell_ids: set[str] = field(default_factory=set)

    @property
    def all_shell_ids(self) -> set[str]:
        return self.shell_ids | self.adjacent_shell_ids
