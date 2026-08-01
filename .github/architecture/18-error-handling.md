# 18 - Error Handling

## Objetivo

Definir politica unificada de tratamento de erros, observabilidade e recuperacao em todos os subsistemas.

## Classificacao de Erros

- `DomainError`: violacao de regra de negocio/invariante.
- `ImportError`: problemas de leitura/conversao de dados externos.
- `TaskError`: falha em plugin check/design.
- `IntegrationError`: falha entre camadas/adaptadores.
- `UserInputError`: configuracao invalida de entrada na GUI.

## Principios

- erros devem ser tipados e semanticamente claros;
- mensagens para usuario devem ser acionaveis;
- stack trace completo permanece em log tecnico;
- falha de plugin isolada nao derruba a aplicacao inteira.

## Logging

Niveis recomendados:

- DEBUG: diagnostico detalhado;
- INFO: eventos de fluxo;
- WARNING: inconsistencias recuperaveis;
- ERROR: falhas com perda de operacao.

Campos minimos de log:

- timestamp
- nivel
- modulo/subsistema
- correlation_id do caso de uso
- mensagem
- excecao (quando houver)

## Fluxo de Tratamento

1. Capturar erro na fronteira do subsistema.
2. Enriquecer com contexto.
3. Classificar por tipo.
4. Registrar em log.
5. Propagar erro tipado para camada superior.
6. Converter em mensagem de UI quando aplicavel.

## GUI e Erros

- dialogos amigaveis sem detalhes sensiveis;
- opcao de abrir detalhes tecnicos quando necessario;
- instrucoes de recuperacao (ex.: validar CSV, revisar plugin, limpar override).

## Ver Tambem

- [04 - Application Layer](04-application-layer.md)
- [10 - Importers](10-importers.md)
- [11 - Plugin System](11-plugin-system.md)
- [17 - Coding Style](17-coding-style.md)
