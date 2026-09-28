from __future__ import annotations

import dataclasses

import pandas as pd
import pytest
from conftest import build_small_model

from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.task_res_repr import TaskBarResCols as t1d
from civil_3P.tasks.task_input_context import TaskInputContext
from civil_3P.tasks.task_metadata import TaskMetadata
from civil_3P.tasks.task_plugin import TaskPlugin
from civil_3P.tasks.task_registry import TaskRegistry
from civil_3P.tasks.task_res import TaskRes

METADATA_1D = TaskMetadata(
    identifier="dummy_1d",
    display_name="Dummy 1D",
    supported_element_type=mc.BARS,
)


class Dummy1DPlugin(TaskPlugin):
    """Returns a well-formed 1D result for every station in the selection."""

    def __init__(self, columns: list[str] | None = None) -> None:
        self._columns = columns or [t1d.ELEMENT, t1d.STATION, t1d.VALUE]

    @property
    def metadata(self) -> TaskMetadata:
        return METADATA_1D

    def validate_input(self, context: TaskInputContext) -> None:
        if context.selection_model.tables["bars_df"].empty:
            raise ValueError("No 1D elements selected")

    def execute(self, context: TaskInputContext) -> TaskRes:
        res_df = pd.DataFrame({col: [1.0] for col in self._columns})

        return TaskRes(metadata=self.metadata, results=res_df)


class UnsupportedPlugin(TaskPlugin):
    """Plugin whose metadata targets no known element type."""

    @property
    def metadata(self) -> TaskMetadata:
        return TaskMetadata(
            identifier="unsupported",
            display_name="Unsupported",
            supported_element_type="not_a_real_type",
        )

    def validate_input(self, context: TaskInputContext) -> None:
        pass

    def execute(self, context: TaskInputContext) -> TaskRes:
        return TaskRes(
            metadata=self.metadata,
            results=pd.DataFrame({"anything": [1]}),
        )


class TestTaskRes:
    def test_is_frozen(self) -> None:
        result = TaskRes(metadata=METADATA_1D, results=pd.DataFrame())

        with pytest.raises(dataclasses.FrozenInstanceError):
            result.metadata = None


class TestTaskPlugin:
    @classmethod
    def setup_class(cls) -> None:
        cls.model = build_small_model()

    def test_supports_matches_metadata_element_type(self) -> None:
        plugin = Dummy1DPlugin()

        assert plugin.supports(mc.BARS) is True
        assert plugin.supports(mc.SHELLS) is False

    def test_get_task_res_returns_validated_result(self) -> None:
        plugin = Dummy1DPlugin()
        context = TaskInputContext(
            full_model=self.model,
            selection_model=self.model,
            case_id="DEAD",
        )

        result = plugin.get_task_result(context)

        assert result.metadata.identifier == "dummy_1d"

    def test_get_task_res_with_wrong_columns_raises_value_error(self) -> None:
        plugin = Dummy1DPlugin(columns=[t1d.ELEMENT, "unexpected_column"])
        context = TaskInputContext(
            full_model=self.model,
            selection_model=self.model,
            case_id="DEAD",
        )

        with pytest.raises(ValueError, match="Columns do not match"):
            plugin.get_task_result(context)

    def test_validate_output_with_unsupported_element_type_raises(self) -> None:
        plugin = UnsupportedPlugin()
        context = TaskInputContext(
            full_model=self.model,
            selection_model=self.model,
            case_id="DEAD",
        )
        result = plugin.execute(context)

        with pytest.raises(ValueError, match="Unsupported element type"):
            plugin.validate_output(result)


class TestTaskRegistry:
    def setup_method(self) -> None:
        self.registry = TaskRegistry()

    def test_register_and_get_plugin(self) -> None:
        plugin = Dummy1DPlugin()
        self.registry.register_or_replace(plugin)

        assert self.registry.get("dummy_1d") is plugin
        assert self.registry.get_task_identifiers() == ["dummy_1d"]

    def test_register_or_replace_overwrites_existing_identifier(self) -> None:
        first = Dummy1DPlugin()
        second = Dummy1DPlugin()
        self.registry.register_or_replace(first)
        self.registry.register_or_replace(second)

        assert self.registry.get("dummy_1d") is second
        assert len(self.registry.all()) == 1

    def test_get_unknown_identifier_raises_key_error(self) -> None:
        with pytest.raises(KeyError):
            self.registry.get("unknown")

    def test_clear_plugins_empties_registry(self) -> None:
        self.registry.register_or_replace(Dummy1DPlugin())
        self.registry.clear_plugins()

        assert self.registry.get_task_identifiers() == []
