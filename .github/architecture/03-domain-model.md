# 03 - Domain Model

## Objetivo

Definir o modelo interno unificado do civil_3P para elementos, materiais, resultados e overrides, independente do software de origem.

## Principios

- o dominio nao conhece formato de origem (csv/xls/xlsx);
- importadores convertem fonte externa para representacao intermediaria e depois para o modelo central;
- o modelo central e tabular;
- regras de negocio ficam no dominio/aplicacao, nao em GUI/render/import parser.

## Entidades Centrais

- Model (agregado raiz)
- Node
- Element1D
- Element2D
- Material
- Section
- OriginResults1D
- OriginResults2D
- OriginDisplacementsNodes
- OriginReactionsNodes
- OverrideSet
- TaskResults (1D e 2D)

## Estrutura Tabular Obrigatoria

Tabelas exigidas no modelo central:

- nodes_df
- elements_1d_df
- elements_2d_df
- materials_df
- sections_df
- origin_1d_results_df
- origin_2d_results_df
- origin_node_displacements_df
- origin_node_reactions_df
- overrides_df
- task_1d_results_df
- task_2d_results_df
- task_node_results_df

## Representacao Intermediaria de Importacao

A importacao deve passar por um contrato intermediario unico antes de criar o modelo central.

Fluxo obrigatorio:

1. fonte externa (sap/midas/scia)
2. IntermediateRepresentation
3. FEMModel

A IntermediateRepresentation deve conter o mesmo conjunto logico de tabelas do modelo central para simplificar validacao e mapeamento.

## Convencoes FEM

### Tipos de Elemento Suportados

- 1D: barras/vigas com conectividade linear
- 2D: placas/cascas com representacao superficial

### Identificacao Interna

- id estavel por no e elemento;
- classificacao por ElementType;
- campos obrigatorios de material, secao e espessura conforme tipo.

### Resultados

- 1D: amostras ao longo do elemento;
- 2D: valores por no do elemento;
- metadados de caso/combinacao e localizacao sempre presentes.

## Regras de Normalizacao

- cada entidade deve ter chave estavel;
- relacoes entre entidades devem ser explicitas;
- evitar duplicacao de atributo quando houver referencia natural;
- importadores mapeiam nomenclaturas externas para as tabelas internas.

## Regras de Dominio

- elementos de tarefas: somente 1D e 2D;
- resultados 1D guardam amostras do inicio ao fim do elemento;
- resultados 2D guardam valores nos nos dos elementos;
- resultados 2D solicitados por elemento sao calculados;
- overrides nao alteram o estado de importacao original.

## Contratos Relevantes

- ElementType
- ResultLocation
- TaskEligibility

## Fora de Escopo

- renderizacao 3D
- widgets/eventos Qt
- parser concreto de csv/xls
- descoberta dinamica de plugins

## Ver Tambem

- [04 - Application Layer](04-application-layer.md)
- [08 - Results](08-results.md)
- [09 - Overrides](09-overrides.md)
- [10 - Importers](10-importers.md)
