# 10 - Importers

## Objetivo

Definir o mecanismo de importacao baseado em Adapter + Factory para converter CSV de diferentes fontes FEM para o modelo interno.

## Fontes Alvo

- SAP2000
- MIDAS Civil
- SCIA Engineer

## Formato de Entrada

- SAP2000: planilha Excel (xls)
- demais softwares: CSV como formato inicial padrao.

## Tabelas SAP2000

- Area Section Assignments (Area|Section)
- Area Section Properties (Section|Material|Thickness)
- Combination Definitions (ComboName|ComboType)
- Connectivity - Area (Area|NumJoints|Joint1|Joint2|Joint3|Joint4)
- Connectivity - Frame (Frame|JointI|JointJ)
- Element Forces - Area Shells (Area|Joint|OutputCase|F11|F22|F12|M11|M22|M12|V13|V23)
- Element Forces - Frames (Frame|Station|OutputCase|CaseType|P|V2|V3|T|M2|M3)
- Frame Section Assignments (Frame|AnalSect)
- Frame Section Properties 01 - General (SectionName|Material|Area|I33|I22)
- Joint Coordinates (Joint|GlobalX|GlobalY|GlobalZ)
- Joint Displacements (Joint|OutputCase|CaseType|StepType|U1|U2|U3|R1|R2|R3)
- Joint Reactions (Joint|OutputCase|CaseType|StepType|F1|F2|F3|M1|M2|M3)
- Load Case Definitions (Case)
- Material Properties 02 - Basic Mechanical Properties (Material|E1|G12|U12|A1)

## Formato SAP2000

- varias tabelas em um unico arquivo;
- cada tabela possui um titulo (coluna 1, linha 1);
- cada tabela possui colunas de atributos (linha 2);
- para cada atributo, existe a unidade correspondente (linha 3) (Exemplo: unidade de força: tonf. Texto: text).

## Arquitetura

- `ImporterAdapter` (porta): contrato unico de leitura/conversao.
- `Sap2000CsvAdapter`, `MidasCsvAdapter`, `SciaCsvAdapter`: implementacoes.
- `ImporterFactory`: escolhe adapter por metadado/perfil de importacao.

## Responsabilidades

- parsear tabelas de geometria, propriedades e resultados;
- validar campos obrigatorios;
- mapear para convencao interna 1D/2D;
- reportar inconsistencias com erros tipados.

## Restricoes

- importador nao executa regra de verificacao/dimensionamento;
- importador nao acessa GUI;
- importador nao acopla tipos concretos do dominio alem dos contratos de entrada.

## Conversao para Modelo Interno

Mapeamentos devem obedecer [03 - Domain Model](03-domain-model.md), incluindo:

- nomenclatura de elementos;
- campos de espessura/secao/material;
- representacao de resultados 1D/2D.

## Pressupostos

- Elementos 2D podem ter 3 nos ou 4 nos nos dados de origem. O programa deve levar isso em conta.

## Ver Tambem

- [03 - Domain Model](03-domain-model.md)
- [18 - Error Handling](18-error-handling.md)
