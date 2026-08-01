# 07 - Selection

## Objetivo

Definir como o usuario seleciona elementos no ambiente 3D e como essa selecao vira contexto para tarefas e consultas.

## Operacoes de Selecao

- clique simples para selecionar elemento unico;
- multisselecao por modificadores;
- filtros por tipo de elemento (1D/2D);
- limpar/inverter selecao;
- selecao por criterio (material, grupo, faixa de resultado).

## Contrato de Selecao

O contexto de selecao deve expor:

- ids de elementos selecionados (selecao primaria);
- ids de elementos adjacentes quando existirem (vizinhanca candidata);
- tipo dos elementos;
- elegibilidade para cada tarefa;
- snapshot imutavel para execucao de plugin.

Este modulo nao decide regra de media. Ele apenas fornece dados de selecao e vizinhanca para os modulos consumidores.

## Regras

- plugins check/design atuam apenas em elementos 1D/2D selecionados;
- selecao nao deve depender de widgets Qt para existir no `application`;
- renderer informa picks por porta de evento.
- o uso da vizinhanca em media 2D e decidido em `08-results`.

## Fluxo Resumido

1. Renderer detecta pick.
2. Adaptador transforma em evento de selecao.
3. `SelectionService` atualiza contexto (selecao primaria + vizinhanca candidata).
4. GUI atualiza paineis e habilitacao de comandos.

## Ver Tambem

- [04 - Application Layer](04-application-layer.md)
- [08 - Results](08-results.md)
- [11 - Plugin System](11-plugin-system.md)
- [13 - Check Plugins](13-check-plugins.md)
- [14 - Design Plugins](14-design-plugins.md)
