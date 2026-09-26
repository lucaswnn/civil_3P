# Civil 3P

`Civil 3P` é um aplicativo desktop de visualização e processamento de resultados de elementos finitos feito na linguagem python.

O projeto foi pensado com foco em:

- unificação de dados de vários softwares comerciais;
- extensibilidade por meio de plugins;
- processamento de resultados 1D e 2D;
- tarefas de check e design;
- interface gráfica para uso democrático;
- expansão das funcionalidades de forma orgânica por meio da linguagem python.

## Estrutura

```text
src/
  civil_3P/
    application/
    core/
    importers/
    tasks/
tests/
.github/
```

## Dependências

Runtime:

- Python 3.13+
- pandas
- numpy
- PySide6
- pyvista
- pyvistaqt
- openpyxl

Desenvolvimento:

- pytest

## Instalação

Crie um ambiente virtual e instale o projeto com dependências de desenvolvimento:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e .[dev]
```

## Como Rodar os Testes (atualmente quebrados)

```powershell
python -m pytest -q
```

## Como executar o programa

```powershell
python -m civil_3P
```

## TODO

### Geral

- Integrar github actions
- Inspecionar testes e cobertura
- Lançar primeira versão utilizável

### Testes

- Teste para importar SAP2000
 - Modelo incompleto
 - Modelo corrompido
- Teste para arquivos em json
 - Salvar arquivo
 - Carregar arquivo
 - Carregar arquivo corrompido
- Teste de modelo
 - Conectividade
 - Falta de conectividade
 - Elementos com seções
 - Elementos com materiais
 - Integridade entre resultados e modelo
 - Teste de filtro por seleção
 - Teste de filtro por seleção complementar
 - Teste de filtro por caso de carga
 - Teste de modelo vazio
 - Teste de filtros com modelo vazio
 - Teste de modelo sem seleção

### Funcionalidades

- Criar exemplo de plugin de placa e de nós
- Criar seleção com o pyvista
- Serviço de seleção
- Listener de seleção
- Controller de seleção (3D e tabela)
- Tabela
- Modos de exibição (habilitar/desabilitar elementos, cores, espessuras)
- Realocar legenda e colocar em container
- Modos de exibição da legenda
- Botão de atualização com mais dados do modelo externo (aviso que assume que os dados sao consistentes) - dados são novos ou sobrescritos
- Possibilitar carregar modelo incompleto e alertar que faltam dados básicos (tasks só funcionam com dados básicos)
- Antes de executar task verificar dados básicos
- Ordenador da tabela
- Criar importador Midas
- Criar importador SCIA
- Criar parametrização para plugins
- Criar salvamento do projeto em binário (eficiente)
