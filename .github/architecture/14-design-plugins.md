# 14 - Design Plugins

## Objetivo

Definir API de plugins de dimensionamento para propor/avaliar secoes e parametros de projeto em elementos selecionados.

## Elegibilidade

- somente elementos 1D e 2D;
- execucao sobre contexto de selecao vigente;
- plugin declara tipos de elemento suportados.

## Contrato da Classe Abstrata

Metodos minimos esperados:

- `metadata()`
- `supports(element_type)`
- `validate_input(context)`
- `run_design(context)`
- `build_report(result)`

## Contexto de Entrada

- elementos selecionados (selecao primaria);
- elementos adjacentes quando existirem (vizinhanca candidata);
- carregamentos/casos/combinacoes relevantes;
- propriedades efetivas (incluindo overrides);
- configuracoes de dimensionamento.

Observacao: a politica de media com vizinhanca nao e decidida no plugin; essa diretriz pertence ao processamento de resultados.

## Saida Esperada

- recomendacoes de secao/espessura/parametros;
- verificacao de viabilidade por criterio;
- indicador de convergencia/sucesso;
- relatorio estruturado para tabela e exportacao.

## Restricoes

- plugin nao altera o modelo base importado;
- plugin retorna propostas e resultados, nao mutacao direta em entidades;
- integracao com UI ocorre via servicos da aplicacao.

## Ver Tambem

- [11 - Plugin System](11-plugin-system.md)
- [07 - Selection](07-selection.md)
- [08 - Results](08-results.md)
- [09 - Overrides](09-overrides.md)
