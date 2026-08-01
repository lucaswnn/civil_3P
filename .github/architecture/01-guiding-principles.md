# 01 - Guiding Principles

## Filosofia

O projeto adota Open/Closed como principio central:

- novas funcionalidades entram por extensao de contratos;
- o nucleo nao deve ser alterado para cada nova regra.

Complementos:

- SOLID pragmatica;
- composicao sobre heranca;
- contratos explicitos com tipagem;
- foco em testabilidade e rastreabilidade.

## Arquitetura Geral: Hexagonal + MVC na GUI

Hexagonal:

- dominio no centro (`core`);
- portas por interfaces;
- adaptadores para entrada/saida (CSV, render, plugins, GUI).

MVC para GUI:

- Model: estado projetado para apresentacao;
- View: widgets e eventos Qt;
- Controller: traduz eventos de interface em comandos de aplicacao.

## Regras de Dependencia

- `core` nao depende de `gui`, `visualization` ou `importers`.
- `application` depende de contratos, nao de implementacoes concretas.
- `gui` e `visualization` dependem de `application` para comportamento.
- `tasks` dependem de contratos de dominio e contexto de execucao.

## Padroes Obrigatorios

- Adapter + Factory para importadores.
- Strategy para algoritmos por tipo de elemento/tarefa.
- Observer/event bus para propagacao de selecao e estado.
- Dependency Injection para montagem de servicos.

## Open/Closed na Pratica

- Importacao: novo software = novo adapter, sem alterar o `core`.
- Plugins: nova verificacao/dimensionamento = nova classe plugin.
- Visualizacoes internas: nova ferramenta = novo modulo interno em `tasks`.

## Antipadroes Proibidos

- logica de negocio dentro de widgets Qt;
- chamadas diretas de PyVista no dominio;
- importador escrevendo regras de calculo de check/design;
- uso de objetos globais mutaveis entre subsistemas.

## Ver Tambem

- [03 - Domain Model](03-domain-model.md)
- [04 - Application Layer](04-application-layer.md)
- [05 - GUI](05-gui.md)
