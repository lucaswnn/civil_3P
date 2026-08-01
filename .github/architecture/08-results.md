# 08 - Results

## Objetivo

Definir como resultados gerados por tarefas/plugins sao processados para visualizacao (colormap) e tabela.

Este modulo nao define a logica de calculo dos plugins. Ele apenas processa os dados de saida das tarefas conforme criterios de visualizacao.

## Modos de Visualizacao

- 1D: somente por elemento.
- 2D: por elemento.
- 2D: por no com media.
- 2D: por no sem media.

## Pressuposto de Entrada

- 1D: os resultados chegam amostrados em pontos intervalados do inicio ao fim do elemento.
- 2D: os resultados chegam nos nos de cada elemento.

## Contrato de Consulta

Entradas:

- resultados das tarefas/plugins;
- criterio de visualizacao (modo 1D por elemento ou modo 2D por elemento/no);
- contexto de selecao (selecao primaria);
- vizinhanca candidata (elementos adjacentes quando houver);
- politica de media (aplicar ou nao adjacentes no modo 2D por no com media).

Saidas:

- serie tipada para colormap;
- tabela normalizada para GUI;
- metadados de unidade, minimo/maximo e validade.

## Politica de Media e Coesao

A diretriz de incluir ou nao vizinhanca na media deve ficar neste modulo de Results, encapsulada em uma politica de agregacao (por exemplo, `ResultAveragingPolicy`).

Motivo de coesao:

- media e agregacao sao responsabilidades de pos-processamento de resultados;
- `Selection` deve apenas fornecer selecao primaria + vizinhanca candidata;
- `Application` deve orquestrar, sem carregar regra numerica de agregacao.

## Integracao

- rendering consome arrays preparados para colormap;
- GUI consome visao tabular paginada/filtravel;
- plugins produzem resultados e consomem contexto de selecao.

## Responsabilidades

- `08-results`: agregacao, media, normalizacao e conversao para formatos de visualizacao.
- `04-application-layer`: orquestrar execucao de tarefa e consulta processada de resultados.
- `05-gui`: apenas apresentacao da tabela e interacao visual.

## Ver Tambem

- [04 - Application Layer](04-application-layer.md)
- [06 - Rendering](06-rendering.md)
- [05 - GUI](05-gui.md)
- [07 - Selection](07-selection.md)
- [11 - Plugin System](11-plugin-system.md)
- [13 - Check Plugins](13-check-plugins.md)
- [14 - Design Plugins](14-design-plugins.md)
