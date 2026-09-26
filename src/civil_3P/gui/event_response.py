from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from civil_3P.gui.event_status import EventStatus
from civil_3P.utils.gui_messages import GuiMessages as gm

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


@dataclass
class EventResponse:
    status: EventStatus
    message: str
    detailed_message: str | None = None

    def display_message(self, panel: QWidget):
        if self.status == EventStatus.SUCCESS:
            gm.display_info(panel, self.message)

        elif self.status == EventStatus.WARNING:
            gm.display_warning(panel, self.message)

        elif self.status == EventStatus.FAILURE:
            gm.display_error(
                panel,
                self.message,
                self.detailed_message,
            )

        else:
            raise ValueError(f"Unknown event status: {self.status}")
