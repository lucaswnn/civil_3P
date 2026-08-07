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
