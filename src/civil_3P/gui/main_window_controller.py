from civil_3P.application.preferences_service import UserPreferencesService

class MainWindowController:
    def __init__(
        self,
        preferences_service: UserPreferencesService,
    ):
        self.preferences_service = preferences_service
