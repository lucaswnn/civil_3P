from __future__ import annotations

import json

import pytest
from conftest import build_small_model

from civil_3P.app.file_service import FileService
from civil_3P.standard.file_repr import FileRepr as fr


def write_json(path, payload) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f)


class TestFileServiceLoad:
    @classmethod
    def setup_class(cls) -> None:
        cls.service = FileService()

    def setup_method(self) -> None:
        self.model = build_small_model()
        self.preferences_snapshot = {
            fr.PLUGINS_BASE_PATH: "C:/plugins",
            fr.SCENE_VIEWER_CONFIG: {},
        }

    def test_load_valid_project_returns_model_and_preferences(self, tmp_path) -> None:
        target = tmp_path / "project.c3p"
        self.service.save(target, self.model, self.preferences_snapshot)

        model, preferences = self.service.load(target)

        assert model.tables["nodes_df"].shape[0] == 5
        assert preferences.plugins_base_path is not None

    def test_load_missing_file_raises_file_not_found(self, tmp_path) -> None:
        missing = tmp_path / "does_not_exist.c3p"

        with pytest.raises(FileNotFoundError):
            self.service.load(missing)

    def test_load_non_dict_root_raises_type_error(self, tmp_path) -> None:
        target = tmp_path / "project.c3p"
        write_json(target, [1, 2, 3])

        with pytest.raises(TypeError):
            self.service.load(target)

    def test_load_incompatible_format_version_raises_value_error(
        self, tmp_path
    ) -> None:
        target = tmp_path / "project.c3p"
        write_json(
            target,
            {
                fr.FORMAT_VERSION: "0.0.1",
                fr.PREFERENCES: self.preferences_snapshot,
                fr.MODEL: self.model.to_dict(),
            },
        )

        with pytest.raises(ValueError):
            self.service.load(target)

    def test_load_missing_model_key_raises_type_error(self, tmp_path) -> None:
        target = tmp_path / "project.c3p"
        write_json(
            target,
            {
                fr.FORMAT_VERSION: FileService.FORMAT_VERSION,
                fr.PREFERENCES: self.preferences_snapshot,
            },
        )

        with pytest.raises(TypeError):
            self.service.load(target)

    def test_load_missing_preferences_key_raises_type_error(self, tmp_path) -> None:
        target = tmp_path / "project.c3p"
        write_json(
            target,
            {
                fr.FORMAT_VERSION: FileService.FORMAT_VERSION,
                fr.MODEL: self.model.to_dict(),
            },
        )

        with pytest.raises(TypeError):
            self.service.load(target)
