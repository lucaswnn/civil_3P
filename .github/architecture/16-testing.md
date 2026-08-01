# 16 - Testing

## Objetivo

Garantir confiabilidade funcional e evolucao segura da arquitetura por meio de testes automatizados com pytest.

## Pilares

- testes unitarios para regras de dominio;
- testes de integracao para importadores, aplicacao e plugins;
- testes de interface/smoke para fluxos criticos da GUI.

## Estrutura Recomendada

- `tests/unit/core`
- `tests/integration/importers`
- `tests/integration/tasks`
- `tests/e2e/gui`

## Cobertura Minima Desejada

- regras de dominio essenciais e invariantes;
- adaptadores de importacao CSV por software;
- contratos de plugins check/design;
- fluxo de selecao -> execucao de tarefa -> exibicao de resultado.

## Testes de Plugin

- validar conformidade com classe abstrata;
- validar elegibilidade por tipo de elemento;
- validar formato de relatorio de saida.

## Testes de Importador

- validar mapeamento para convencoes internas;
- validar tratamento de arquivo invalido/incompleto;
- validar consistencia de unidades e tipos.

## Qualidade Estatica

- tipagem estatica em CI;
- lint/format;
- execucao de testes como precondicao de release.

## Ver Tambem

- [17 - Coding Style](17-coding-style.md)
- [10 - Importers](10-importers.md)
- [19 - Build and Deployment](19-build-deployment.md)
