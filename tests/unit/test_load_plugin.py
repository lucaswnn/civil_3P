from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from civil_3P.app.plugin_loader_service import PluginLoaderService

TASK_EXAMPLES_DIR = Path(__file__).resolve().parents[2] / "task_examples"


class TestPluginLoaderServiceLoadFrom:
    @classmethod
    def setup_class(cls) -> None:
        cls.service = PluginLoaderService()

    def test_load_from_directory_with_valid_plugins(self, tmp_path) -> None:
        shutil.copy2(TASK_EXAMPLES_DIR / "example_1d_plugin.py", tmp_path)
        shutil.copy2(TASK_EXAMPLES_DIR / "example_2d_plugin.py", tmp_path)

        plugins = self.service.load_from(tmp_path)
        identifiers = {p.metadata.identifier for p in plugins}

        assert identifiers == {"example_1d", "example_2d"}

    def test_load_from_missing_directory_returns_empty_list(self, tmp_path) -> None:
        missing_dir = tmp_path / "does_not_exist"

        plugins = self.service.load_from(missing_dir)

        assert plugins == []

    def test_load_from_ignores_module_with_syntax_error(self, tmp_path) -> None:
        (tmp_path / "broken_plugin.py").write_text(
            "this is not valid python (((", encoding="utf-8"
        )
        shutil.copy2(TASK_EXAMPLES_DIR / "example_1d_plugin.py", tmp_path)

        plugins = self.service.load_from(tmp_path)

        assert len(plugins) == 1
        assert plugins[0].metadata.identifier == "example_1d"

    def test_load_from_ignores_plugin_with_empty_identifier(self, tmp_path) -> None:
        (tmp_path / "empty_identifier_plugin.py").write_text(
            """
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.tasks.task_metadata import TaskMetadata
from civil_3P.tasks.task_plugin import TaskPlugin


class EmptyIdentifierPlugin(TaskPlugin):
    @property
    def metadata(self):
        return TaskMetadata(
            identifier="",
            display_name="Broken",
            supported_element_type=mc.NODES,
        )

    def validate_input(self, context):
        pass

    def execute(self, context):
        raise NotImplementedError
""",
            encoding="utf-8",
        )

        plugins = self.service.load_from(tmp_path)

        assert plugins == []


class TestPluginLoaderServiceAddFrom:
    @classmethod
    def setup_class(cls) -> None:
        cls.service = PluginLoaderService()

    def test_add_from_copies_and_loads_plugin(self, tmp_path) -> None:
        destiny = tmp_path / "plugins"
        destiny.mkdir()

        plugins = self.service.add_from(
            [TASK_EXAMPLES_DIR / "example_1d_plugin.py"],
            destiny,
        )

        assert (destiny / "example_1d_plugin.py").is_file()
        assert len(plugins) == 1
        assert plugins[0].metadata.identifier == "example_1d"

    def test_add_from_invalid_destiny_raises_value_error(self, tmp_path) -> None:
        invalid_destiny = tmp_path / "does_not_exist"

        with pytest.raises(ValueError):
            self.service.add_from(
                [TASK_EXAMPLES_DIR / "example_1d_plugin.py"],
                invalid_destiny,
            )

    def test_add_from_ignores_missing_source_file(self, tmp_path) -> None:
        destiny = tmp_path / "plugins"
        destiny.mkdir()

        plugins = self.service.add_from(
            [tmp_path / "does_not_exist.py"],
            destiny,
        )

        assert plugins == []
