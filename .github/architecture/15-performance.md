# 15 - Performance

## Objetivo

Definir diretrizes para manter interacao fluida e execucao previsivel em modelos de pequeno a grande porte.

## Metas

- tempo de resposta de interacao visual baixo para operacoes comuns;
- atualizacao incremental de cena e resultados;
- custo controlado de execucao de plugins em lotes grandes.

## Estrategias

- cache de dados de resultados por caso/combinacao;
- atualizacao parcial de atores/meshes no renderer;
- filtros de selecao eficientes por indice;
- processamento em background para tarefas demoradas;
- profiling periodico dos caminhos criticos.

## Gargalos Esperados

- parsing de CSV extensos;
- remapeamento repetitivo de colormap;
- relatorios de plugins sobre selecoes muito grandes.

## Boas Praticas

- evitar copia desnecessaria de arrays volumosos;
- usar estruturas imutaveis para snapshots de selecao;
- registrar metricas de tempo por caso de uso.

## Ver Tambem

- [06 - Rendering](06-rendering.md)
- [08 - Results](08-results.md)
- [16 - Testing](16-testing.md)
