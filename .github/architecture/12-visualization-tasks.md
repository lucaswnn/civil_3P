# 12 - Visualization Tasks

## Objetivo

Definir tarefas de visualizacao internas do sistema, extensiveis para desenvolvedores do projeto sem exposicao de API de plugin para usuario final.

## Escopo

Inclui:

- modos de visualizacao;
- filtros visuais;
- consultas visuais;
- ferramentas de leitura/interpretação em cena.

Nao inclui:

- carregamento de `.py` de usuario para visualizacao.

## Open/Closed para Desenvolvedor

Novas tarefas internas devem:

- implementar interface interna de comando de visualizacao;
- ser registradas no catalogo interno de tarefas;
- manter compatibilidade com selecao e resultados existentes.

## Dependencias

- recebe dados de selecao e resultados da camada de aplicacao;
- aplica alteracoes no renderer via adaptadores de visualizacao.

## Ver Tambem

- [06 - Rendering](06-rendering.md)
- [07 - Selection](07-selection.md)
- [11 - Plugin System](11-plugin-system.md)
