from civil_3P.application.preferences_service import PreferencesService

class MainWindowController:
    def __init__(
        self,
        preferences_service: PreferencesService,
    ):
        self.preferences_service = preferences_service
