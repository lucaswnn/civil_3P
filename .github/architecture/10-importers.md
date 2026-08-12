# 10 - Importers

## Objetivo

Definir um pipeline de importacao extensivel para converter fontes heterogeneas (csv, xls, xlsx e futuras) no modelo interno, sem acoplar parser de origem ao dominio.

Pipeline obrigatorio:

1. fonte externa -> 2. representacao intermediaria -> 3. modelo central.

## Fontes Alvo

- SAP2000
- MIDAS Civil
- SCIA Engineer

## Principio de Extensibilidade

Cada nova fonte deve implementar apenas duas responsabilidades:

- ler/parsing da fonte para uma representacao intermediaria tipada;
- mapeamento da representacao intermediaria para o contrato do modelo central.

Com isso, a variacao de formato de origem (csv/xls/etc) fica encapsulada no importador da fonte.

## Arquitetura

- ImporterAdapter: porta de entrada da importacao.
- IntermediateRepresentation: contrato intermediario unificado entre parser de origem e modelo central.
- BaseIntermediateImporter: utilitarios de mapeamento e orquestracao comum.
- Source Importers:
- Sap2000Importer
- MidasImporter (futuro)
- SciaImporter (futuro)
- ImporterRegistry (factory): resolve o importador correto por perfil.

## Fluxo de Dados

1. ImporterRegistry seleciona o importador por perfil.
2. Importador le a fonte externa e produz IntermediateRepresentation.
3. Importador converte IntermediateRepresentation em FEMModel.
4. Aplicacao usa apenas FEMModel, sem conhecer parser de origem.

## SAP2000

Entrada preferencial:

- workbook de modelo: sap2000_model.xls ou sap2000_model.xlsx;
- workbook de resultados: sap2000_results.xls ou sap2000_results.xlsx.

Observacoes:

- O export SAP2000 pode conter multiplas tabelas no mesmo sheet.
- Cada tabela e detectada por bloco: titulo, cabecalho, linha de unidades e linhas de dados.
- Em fase de transicao, pode existir fallback csv quando os workbooks nao estiverem presentes.

## Tabelas SAP2000 (referencia)

Modelo:

- Joint Coordinates
- Connectivity - Frame
- Connectivity - Area
- Frame Section Assignments
- Frame Section Properties 01 - General
- Area Section Assignments
- Area Section Properties
- Material Properties 02 - Basic Mechanical Properties

Resultados:

- Element Forces - Frames
- Element Forces - Area Shells
- Joint Displacements
- Joint Reactions

## Responsabilidades

- parser de origem:
- isolar detalhes de formato (csv/xls/xlsx)
- detectar e extrair tabelas
- reportar inconsistencias de leitura

- conversao para intermediario:
- normalizar nomes de colunas de origem
- preencher defaults minimos
- preservar semantica de caso/combinacao e localizacao

- conversao para modelo central:
- montar tabelas exigidas pelo dominio
- validar colunas obrigatorias
- aplicar normalizacoes finais de tipo/localizacao

Tabelas de saida devem seguir nomenclatura exata do dominio:

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

## Restricoes

- importador nao executa regras de check/design;
- importador nao acessa GUI;
- importador nao acopla visualizacao;
- importador nao manipula diretamente casos de uso de aplicacao.

## Tratamento de Erro

- erro de engine excel ausente deve ser explicito (ex.: xlrd/openpyxl);
- erro de tabela obrigatoria ausente deve apontar nome da tabela;
- erro de coluna obrigatoria ausente deve apontar coluna e tabela.

## Contrato com o Dominio

A saida do importador deve respeitar o esquema definido em [03 - Domain Model](03-domain-model.md), sem bypass de validacao do FEMModel.

## Ver Tambem

- [03 - Domain Model](03-domain-model.md)
- [04 - Application Layer](04-application-layer.md)
- [18 - Error Handling](18-error-handling.md)
