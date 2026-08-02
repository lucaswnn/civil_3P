from __future__ import annotations

from PySide6.QtWidgets import QApplication

from civil_3P.visualization.widget import SceneWidget


def test_scene_widget_hosts_a_widget_for_the_viewer() -> None:
    app = QApplication.instance() or QApplication([])
    widget = SceneWidget()

    widget.set_scene({"nodes": [], "bars": [], "shells": []})

    assert widget.layout().count() >= 1
    assert widget.layout().itemAt(0).widget() is not None
