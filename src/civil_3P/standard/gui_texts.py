from __future__ import annotations

from enum import StrEnum


class GuiLabels(StrEnum):
    APPLICATION_NAME = "Civil 3P"
    FILE_MENU_NAME = "Arquivo"
    TASK_MENU_NAME = "Tarefas"
    MODEL_TAB = "Modelo"
    TABLE_TAB = "Tabela"
    TABLE_UNDER_CONSTRUCTION = "Tabela (em construção)"
    SELECT_OPTION = "Selecione"
    CASE = "Caso"
    TASK = "Tarefa"
    EXECUTE_TASK = "Executar tarefa"


class FileMenuButtonLabels(StrEnum):
    ADD_PLUGINS = "Adicionar plugins"
    IMPORT_SAP2000 = "Importar SAP2000"
    LOAD_MODEL = "Carregar modelo"
    SAVE_MODEL = "Salvar modelo"
    SET_PLUGINS_FOLDER = "Definir pasta de plugins"


class TaskMenuButtonLabels(StrEnum):
    CASE = GuiLabels.CASE.value
    TASK = GuiLabels.TASK.value
    EXECUTE_TASK = GuiLabels.EXECUTE_TASK.value


class GuiMessageTexts(StrEnum):
    LOAD_MODEL_BEFORE_TASK = "Carregue um modelo antes de executar uma tarefa."
    SELECT_TASK_AND_CASE = "Selecione uma tarefa e um caso antes de executar."
    TASK_SUCCEEDED = "Tarefa executada com sucesso."
    TASK_FAILED = "Falha ao executar a tarefa: {error}"
    PLUGINS_LOADED = "Foram carregados {count} plugins com sucesso."
    MODEL_IMPORTED = "Modelo importado com sucesso."
    MODEL_LOADED = "Modelo carregado com sucesso."
    MODEL_SAVED = "Modelo salvo com sucesso."
    PLUGINS_FOLDER_SET = "Pasta de plugins definida com sucesso."
    LOAD_PLUGINS_FAILED = "Falha ao carregar plugins: {error}"
    IMPORT_MODEL_FAILED = "Falha ao importar o modelo: {error}"
    LOAD_MODEL_FAILED = "Falha ao carregar o modelo salvo: {error}"
    SAVE_MODEL_FAILED = "Falha ao salvar o modelo: {error}"
    SET_PLUGINS_FOLDER_FAILED = "Falha ao definir a pasta de plugins: {error}"


class GuiFileDialogTexts(StrEnum):
    SELECT_PLUGIN_FILES = "Selecionar arquivos de plugins"
    SELECT_SAP2000_FILE = "Selecionar arquivo do SAP2000"
    LOAD_MODEL = "Carregar modelo Civil 3P"
    SAVE_MODEL = "Salvar modelo Civil 3P"
    SET_PLUGINS_FOLDER = "Definir pasta de plugins"
    PYTHON_FILES_FILTER = "Arquivos Python (*.py);;Todos os Arquivos (*)"
    EXCEL_FILES_FILTER = "Arquivos Excel (*.xlsx);;Todos os Arquivos (*)"
    MODEL_FILES_FILTER = "Arquivos Civil 3P (*.c3p)"