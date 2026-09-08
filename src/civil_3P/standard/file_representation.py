from enum import StrEnum

DATAFRAME_DICT_CONV = "records"

class FileRepresentation(StrEnum):
    FORMAT_VERSION = "format_version"
    PREFERENCES = "preferences"
    PLUGINS_BASE_PATH = "plugins_base_path"
    SCENE_VIEWER_CONFIG = "scene_viewer_config"
    MODEL = "model"
    MODEL_UNITS = "units"
    MODEL_TABLES = "tables"
