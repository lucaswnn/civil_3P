from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from civil_3P.core.model import Model
from civil_3P.standard.model_repr import ModelTables as mt


@dataclass(slots=True)
class IntermediateRepr:
    tables: dict[str, pd.DataFrame]
    units: dict[str, dict[str, str]]

    @classmethod
    def empty(cls) -> IntermediateRepr:
        model = Model.empty()

        return cls(
            tables={
                mt.NODES: model.tables[mt.NODES].copy(),
                mt.BARS: model.tables[mt.BARS].copy(),
                mt.SHELLS: model.tables[mt.SHELLS].copy(),
                mt.MATERIALS: model.tables[mt.MATERIALS].copy(),
                mt.SECTIONS: model.tables[mt.SECTIONS].copy(),
                mt.BAR_RESULTS: model.tables[mt.BAR_RESULTS].copy(),
                mt.SHELL_RESULTS: model.tables[mt.SHELL_RESULTS].copy(),
                mt.NODE_DISPLACEMENTS: model.tables[
                    mt.NODE_DISPLACEMENTS
                ].copy(),
                mt.NODE_REACTIONS: model.tables[mt.NODE_REACTIONS].copy(),
                mt.LOAD_CASES: model.tables[mt.LOAD_CASES].copy(),
            },
            units=model.units.copy(),
        )

    def to_model(self) -> Model:
        return Model.from_tables(
            tables={
                mt.NODES: self.tables[mt.NODES].copy(),
                mt.BARS: self.tables[mt.BARS].copy(),
                mt.SHELLS: self.tables[mt.SHELLS].copy(),
                mt.MATERIALS: self.tables[mt.MATERIALS].copy(),
                mt.SECTIONS: self.tables[mt.SECTIONS].copy(),
                mt.BAR_RESULTS: self.tables[mt.BAR_RESULTS].copy(),
                mt.SHELL_RESULTS: self.tables[mt.SHELL_RESULTS].copy(),
                mt.NODE_DISPLACEMENTS: self.tables[
                    mt.NODE_DISPLACEMENTS
                ].copy(),
                mt.NODE_REACTIONS: self.tables[mt.NODE_REACTIONS].copy(),
                mt.LOAD_CASES: self.tables[mt.LOAD_CASES].copy(),
            },
            units=self.units,
        )
