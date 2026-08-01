# civil_3P - Instrucoes do Copilot

Este arquivo define o contexto geral do projeto e as regras obrigatorias para contribuicoes assistidas por IA.

## Visao Geral

O civil_3P e um aplicativo desktop para Windows voltado a:

- visualizacao 3D de modelos de elementos finitos;
- exploracao de resultados;
- execucao de tarefas de verificacao e dimensionamento em elementos selecionados.

Stack principal:

- Python 3.13+
- pandas, numpy (manipulacao de dados)
- PySide6 (GUI)
- PyVista + VTK (renderizacao 3D)
- pytest (testes)
- tipagem estatica completa

## Escopo do Produto

Incluido:

- importacao de dados tabulares (CSV) de fluxos SAP2000, MIDAS Civil e SCIA Engineer;
- conversao para um modelo interno unificado;
- visualizacao 3D, selecao de elementos e colormap de resultados;
- tabela de resultados;
- plugins de verificacao e dimensionamento para elementos 1D e 2D;
- sistema de overrides sem alterar o modelo importado original.
- processamento de resultados com politica de media em 2D no modulo de Results.

Fora de escopo:

- edicao geometrica completa do modelo original;
- suporte a elementos 3D para tarefas de verificacao/dimensionamento;
- plugins Python de usuario para tarefas de visualizacao.

## Regras Obrigatorias Para o Copilot

Nunca:

- quebrar Open/Closed;
- acoplar importadores ao dominio;
- acessar PyVista dentro do dominio;
- colocar regras de negocio na GUI;
- acessar widgets Qt fora da camada GUI.

Sempre:

- usar interfaces (protocols/classes abstratas) para contratos entre camadas;
- usar composicao em vez de heranca profunda;
- usar injecao de dependencias;
- manter alta coesao e baixo acoplamento.

## Fronteiras Arquiteturais

- Dominio (`core`) nao depende de GUI, Qt, PyVista ou VTK.
- Importadores (`importers`) convertem dados externos para o modelo interno sem impor formatos ao dominio.
- Aplicacao (`application`) orquestra casos de uso e integra adaptadores.
- GUI (`gui`) apenas apresenta estado e encaminha intencoes do usuario.
- Renderizacao (`visualization`) executa pipeline 3D e notificacoes de interacao.
- Tarefas (`tasks`) executam regras especializadas via plugins (check/design).

## Mapa da Documentacao

- [Visao Geral](architecture/00-project-overview.md)
- [Filosofia e Principios](architecture/01-guiding-principles.md)
- [Estrutura do Repositorio](architecture/02-project-structure.md)
- [Modelo de Dominio](architecture/03-domain-model.md)
- [Camada de Aplicacao](architecture/04-application-layer.md)
- [GUI PySide6](architecture/05-gui.md)
- [Renderizacao PyVista/VTK](architecture/06-rendering.md)
- [Selecao e Interacao](architecture/07-selection.md)
- [Sistema de Resultados](architecture/08-results.md)
- [Sistema de Overrides](architecture/09-overrides.md)
- [Importadores (Adapter + Factory)](architecture/10-importers.md)
- [Sistema Base de Plugins](architecture/11-plugin-system.md)
- [Visualizacoes Internas](architecture/12-visualization-tasks.md)
- [API Plugins de Verificacao](architecture/13-check-plugins.md)
- [API Plugins de Dimensionamento](architecture/14-design-plugins.md)
- [Desempenho e Escalabilidade](architecture/15-performance.md)
- [Estrategia de Testes](architecture/16-testing.md)
- [Convencoes de Codigo](architecture/17-coding-style.md)
- [Erros e Logging](architecture/18-error-handling.md)
- [Build e Deploy Windows](architecture/19-build-deployment.md)

## Checklist de Revisao Antes de Entregar Codigo

- O codigo respeita Open/Closed?
- Existe dependencia indevida entre GUI/render e dominio?
- O contrato de plugin usa interfaces tipadas?
- O caso de uso esta na camada de aplicacao?
- Ha testes unitarios/integracao cobrindo o comportamento?
