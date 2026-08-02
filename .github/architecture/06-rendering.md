# 06 - Rendering

## Objetivo

Especificar o subsistema de renderizacao 3D com PyVista para exibir modelo, selecao e campos de resultados.

## Pipeline

1. Receber geometria padronizada do modelo interno.
2. Converter para estruturas de malha renderizaveis.
3. Associar arrays escalares/vetoriais de resultados.
4. Aplicar mapa de cores e legenda.
5. Renderizar com camera interativa.

## Recursos Minimos

- exibicao de elementos 1D e 2D;
- alternancia de modos de visualizacao;
- em elementos 1D: diagramas de resultados;
- em elementos 2D: diagramas de isobandas (no caso de resultados por nos) e coloracao de elementos (no caso de resultados por elemento);
- colormap configuravel;
- isolacao/highlight de selecao;
- atualizacao incremental ao trocar caso de resultado.

## Restricoes Arquiteturais

- nenhum objeto PyVista pode entrar no dominio;
- renderer recebe DTOs/adaptadores da camada de aplicacao;
- estado visual (camera/tema) e separado de estado de negocio.

## Integracao com Selecao

Picking e eventos de interacao alimentam `SelectionService` por interface dedicada, sem dependencias ciclicas.

## Desempenho

- atualizacao parcial de malhas;
- cache de mapeamento de scalars;
- nivel de detalhe para modelos grandes.

## Ver Tambem

- [07 - Selection](07-selection.md)
- [08 - Results](08-results.md)
- [15 - Performance](15-performance.md)
