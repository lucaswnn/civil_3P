from __future__ import annotations

from civil_3P.tasks.plugin_loader import PluginLoader
from civil_3P.tasks.task_base import TaskMetadata
from civil_3P.tasks.task_registry import TaskRegistry
from civil_3P.standard.model_components import ModelComponents


def test_plugin_loader_ignores_missing_directory(tmp_path) -> None:
    registry = TaskRegistry()

    loaded = PluginLoader(registry).load_from(tmp_path / "missing")

    assert loaded == ()


def test_plugin_loader_registers_valid_plugin_and_skips_broken_module(tmp_path) -> None:
    (tmp_path / "valid_plugin.py").write_text(
        """
from civil_3P.tasks.task_base import TaskPlugin, TaskMetadata

class UserPlugin(TaskPlugin):
    @property
    def metadata(self):
        return TaskMetadata(
            'user_plugin', 'User plugin', ModelComponents.ELEMENTS_1D)

    def validate_input(self, context):
        pass

    def execute(self, context):
        raise NotImplementedError
""",
        encoding="utf-8",
    )
    (tmp_path / "broken_plugin.py").write_text(
        "raise RuntimeError('broken plugin')\n",
        encoding="utf-8",
    )
    registry = TaskRegistry()

    loaded = PluginLoader(registry).load_from(tmp_path)

    assert loaded == ("user_plugin",)
    assert registry.get("user_plugin").metadata.identifier == "user_plugin"
