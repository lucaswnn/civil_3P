from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.app.preferences_service import PreferencesService


class MainWindowController:
    def __init__(
        self,
        preferences_service: PreferencesService,
    ):
        self.preferences_service = preferences_service
