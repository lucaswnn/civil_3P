from __future__ import annotations

import json

from conftest import build_small_model

from civil_3P.app.file_service import FileService
from civil_3P.standard.file_repr import FileRepr as fr


class TestFileServiceSave:
    @classmethod
    def setup_class(cls) -> None:
        cls.service = FileService()

    def setup_method(self) -> None:
        self.model = build_small_model()
        self.preferences_snapshot = {
            fr.PLUGINS_BASE_PATH: "C:/plugins",
            fr.SCENE_VIEWER_CONFIG: {},
        }

    def test_save_creates_missing_parent_directories(self, tmp_path) -> None:
        target = tmp_path / "sub" / "dir" / "project.c3p"

        self.service.save(target, self.model, self.preferences_snapshot)

        assert target.is_file()

    def test_save_writes_expected_top_level_keys(self, tmp_path) -> None:
        target = tmp_path / "project.c3p"

        self.service.save(target, self.model, self.preferences_snapshot)

        with target.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        assert payload[fr.FORMAT_VERSION] == FileService.FORMAT_VERSION
        assert payload[fr.PREFERENCES] == self.preferences_snapshot
        assert set(payload[fr.MODEL].keys()) == {fr.MODEL_TABLES, fr.MODEL_UNITS}

    def test_save_then_load_roundtrip_preserves_model(self, tmp_path) -> None:
        target = tmp_path / "project.c3p"

        self.service.save(target, self.model, self.preferences_snapshot)
        loaded_model, loaded_preferences = self.service.load(target)

        assert loaded_model.units == self.model.units
        assert loaded_model.tables["nodes_df"].shape[0] == 5
        assert str(loaded_preferences.plugins_base_path) == "C:\\plugins" or (
            str(loaded_preferences.plugins_base_path) == "C:/plugins"
        )

    def test_save_with_empty_preferences_snapshot_does_not_raise(
        self, tmp_path
    ) -> None:
        target = tmp_path / "project.c3p"

        self.service.save(target, self.model, {})

        with target.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        assert payload[fr.PREFERENCES] == {}
