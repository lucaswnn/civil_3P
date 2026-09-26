from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from civil_3P.core.model import Model
from civil_3P.standard.model_representation import ModelTables as mt


@dataclass(slots=True)
class IntermediateRepresentation:
    tables: dict[str, pd.DataFrame]
    units: dict[str, dict[str, str]]

    @classmethod
    def empty(cls) -> "IntermediateRepresentation":
        model = Model.empty()

        return cls(
            tables={
                mt.NODES: model.tables[mt.NODES].copy(),
                mt.ELEMENTS_1D: model.tables[mt.ELEMENTS_1D].copy(),
                mt.ELEMENTS_2D: model.tables[mt.ELEMENTS_2D].copy(),
                mt.MATERIALS: model.tables[mt.MATERIALS].copy(),
                mt.SECTIONS: model.tables[mt.SECTIONS].copy(),
                mt.ORIGIN_1D_RESULTS: model.tables[mt.ORIGIN_1D_RESULTS].copy(),
                mt.ORIGIN_2D_RESULTS: model.tables[mt.ORIGIN_2D_RESULTS].copy(),
                mt.ORIGIN_NODE_DISPLACEMENTS: model.tables[mt.ORIGIN_NODE_DISPLACEMENTS].copy(),
                mt.ORIGIN_NODE_REACTIONS: model.tables[mt.ORIGIN_NODE_REACTIONS].copy(),
                mt.LOAD_CASES: model.tables[mt.LOAD_CASES].copy(),
            },
            units=model.units.copy(),
        )

    def to_model(self) -> Model:
        return Model.from_tables(
            tables={
                mt.NODES: self.tables[mt.NODES].copy(),
                mt.ELEMENTS_1D: self.tables[mt.ELEMENTS_1D].copy(),
                mt.ELEMENTS_2D: self.tables[mt.ELEMENTS_2D].copy(),
                mt.MATERIALS: self.tables[mt.MATERIALS].copy(),
                mt.SECTIONS: self.tables[mt.SECTIONS].copy(),
                mt.ORIGIN_1D_RESULTS: self.tables[mt.ORIGIN_1D_RESULTS].copy(),
                mt.ORIGIN_2D_RESULTS: self.tables[mt.ORIGIN_2D_RESULTS].copy(),
                mt.ORIGIN_NODE_DISPLACEMENTS: self.tables[mt.ORIGIN_NODE_DISPLACEMENTS].copy(),
                mt.ORIGIN_NODE_REACTIONS: self.tables[mt.ORIGIN_NODE_REACTIONS].copy(),
                mt.LOAD_CASES: self.tables[mt.LOAD_CASES].copy(),
            },
            units=self.units,
        )
