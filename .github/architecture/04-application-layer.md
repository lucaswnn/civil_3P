# 04 - Application Layer

## Objetivo

Orquestrar fluxos de uso entre dominio, importadores, renderizacao, GUI e plugins sem concentrar regra de negocio na interface.

## Servicos da Aplicacao

- `ImportModelService`: carrega dados via importador e popula o `Model` interno.
- `SelectionService`: controla selecao atual e fornece selecao primaria + vizinhanca candidata.
- `ResultQueryService`: processa resultados de tarefas para tabela/colormap com criterios de visualizacao e politica de media.
- `OverrideService`: aplica e persiste overrides locais.
- `TaskExecutionService`: executa plugins check/design com contexto tipado e gera resultados de tarefa.
- `VisualizationCommandService`: aplica operacoes internas de visualizacao.

## Casos de Uso Principais

1. Importar modelo e resultados CSV.
2. Renderizar modelo e habilitar interacao 3D.
3. Selecionar elementos e filtrar por tipo.
4. Consultar resultados nodais/elemento com ou sem media.
5. Executar verificacao ou dimensionamento por plugin.
6. Salvar e reaplicar overrides.

## Fluxo de Resultados

1. `TaskExecutionService` executa a tarefa/plugin e gera resultados.
2. `ResultQueryService` recebe resultados da tarefa + criterios de visualizacao.
3. `ResultQueryService` aplica politica de media (com ou sem vizinhanca candidata em 2D).
4. Saida processada segue para rendering (colormap) e GUI (tabela).

## Regras da Camada

- depende de interfaces e DTOs, nao de widgets;
- valida precondicoes de casos de uso;
- retorna erros de dominio/aplicacao com classificacao tipada;
- emite eventos de estado para GUI/render sem acoplamento direto.

## Dependencias Permitidas

- `application -> core`
- `application -> contracts/ports`
- `application -> infrastructure` (logging/config/persistencia)

Nao permitido:

- `application -> widgets Qt`
- `application -> chamadas diretas PyVista`

## Ver Tambem

- [03 - Domain Model](03-domain-model.md)
- [05 - GUI](05-gui.md)
- [07 - Selection](07-selection.md)
- [08 - Results](08-results.md)
- [11 - Plugin System](11-plugin-system.md)
