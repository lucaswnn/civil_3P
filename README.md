# civil_3P

`civil_3P` é um aplicativo desktop de visualização e processamento de resultados de elementos finitos.

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

## Como Rodar os Testes

```powershell
python -m pytest -q
```

## TODO

### Refatoração

- Refatorar enums, inspecionar serviços e controles e suas responsabilidades
- Separar tabelas de task para outra classe, com colunas obrigatórias e com tipo de elemento e critério de exibição
- Classe abstrata para critério de exibição, com 3 subclasses (nó, barra e placa)
- Substituir dicts primitivos dos elementos e resultados a serem exibidos por uma classe para o pyvista

### Funcionalidades

- Criar exemplo de plugin de placa e de nós (1)
- Criar seleção com o pyvista
- Serviço de seleção
- Listener de seleção
- Controller de seleção (3D e tabela)
- Tabela
- Modos de exibição (habilitar/desabilitar elementos, cores, espessuras)
- Realocar legenda e colocar em container (2)
- Modos de exibição da legenda