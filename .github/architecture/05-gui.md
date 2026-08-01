# 05 - GUI

## Objetivo

Definir a camada de interface em PySide6 com separacao MVC e sem logica de negocio embutida em widgets.

## Estrutura MVC

- Model (apresentacao): estado formatado para UI (filtros, colunas, selecoes).
- View: janelas, docks, tabelas, toolbar, comandos visuais.
- Controller: converte interacoes em comandos para servicos da aplicacao.

## Componentes Esperados

- MainWindow com menu principal e barra de ferramentas.
- Dock de arvore/modelo.
- Painel de propriedades e overrides.
- Painel de tarefas (visualizacao/check/design).
- Tabela de resultados.
- Area 3D integrada ao renderer.

## Regra Fundamental

A GUI:

- nunca calcula verificacoes/dimensionamentos;
- nunca interpreta CSV;
- nunca altera diretamente entidades de dominio;
- apenas invoca servicos de aplicacao e exibe estado.

## Tabela de Resultados

Divisao de responsabilidade:

- `08-results`: logica de consulta, agregacao, media e ordenacao de dados.
- `05-gui`: renderizacao da tabela, filtros visuais e interacao do usuario.

## Qt Fora da GUI

Objetos Qt nao devem vazar para `core`, `application`, `importers` ou `tasks`.

## Ver Tambem

- [04 - Application Layer](04-application-layer.md)
- [06 - Rendering](06-rendering.md)
- [08 - Results](08-results.md)
