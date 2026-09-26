from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.standard.model_representation import (
    LoadCasesColumns as lcc,
    ModelTables as mt,
)

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.selection_context import SelectionContext


class ModelService:
    _instance: ModelService | None = None

    def __new__(cls) -> ModelService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = None

        return cls._instance

    model: Model | None

    def get_model(self) -> Model | None:
        return self.model

    def set_model(self, model: Model) -> None:
        self.model = model

    def get_load_cases(self) -> list[str]:
        if self.model is None:
            return []

        cases = self.model.tables[mt.LOAD_CASES][lcc.CASE]

        return list(dict.fromkeys(cases.astype(str)))

    def get_model_by_selection(
        self,
        selection: SelectionContext,
    ) -> Model:
        return self.model.filter_by_selection(selection)

    def get_model_by_selection_reversed(
        self,
        selection: SelectionContext,
    ) -> Model:
        return self.model.filter_by_selection_reversed(selection)

    @staticmethod
    def model_without_elements(
        model: Model,
        selection: SelectionContext,
    ) -> Model:
        return model.remove_elements(selection)

    @staticmethod
    def model_with_elements(
        model: Model,
        selection: SelectionContext,
    ) -> Model:
        return model.filter_by_selection(selection)
