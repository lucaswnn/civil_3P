from __future__ import annotations

from enum import StrEnum

from civil_3P.standard.gui_texts import GuiLabels


class GuiMenuComponents(StrEnum):
    FILE_MENU = "file_menu"
    FILE_MENU_NAME = GuiLabels.FILE_MENU_NAME.value
    TASK_MENU = "task_menu"
    TASK_MENU_NAME = GuiLabels.TASK_MENU_NAME.value
