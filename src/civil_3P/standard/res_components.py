from __future__ import annotations

from enum import StrEnum


class ResSceneKind(StrEnum):
    NODE = "node"
    BAR_PROFILE = "bar_profile"
    SHELL_UNIFORM = "shell_uniform"
    SHELL_SHARED_NODES = "shell_shared_nodes"
    SHELL_ISOLATED_NODES = "shell_isolated_nodes"
