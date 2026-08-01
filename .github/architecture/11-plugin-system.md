# 11 - Plugin System

## Objetivo

Definir a infraestrutura comum para descoberta, validacao e execucao de plugins de verificacao e dimensionamento.

## Contrato Base

Todo plugin deve implementar classe abstrata oficial do projeto com:

- metadados (id, nome, versao, tipo de tarefa, suporte 1D/2D);
- validacao de elegibilidade;
- metodo principal de execucao;
- estrutura de resultado padronizada.

## Contexto de Selecao Consumido por Plugins

Plugins recebem contexto de selecao com:

- elementos selecionados (selecao primaria);
- elementos adjacentes quando existirem (vizinhanca candidata para suporte a media em 2D);
- metadados de elegibilidade por tipo de elemento.

Importante: a decisao de incluir ou nao adjacentes na media e responsabilidade de `08-results`, nao do sistema base de plugins.

## Descoberta e Carregamento

- diretorio padrao de plugins de usuario no Windows: `%APPDATA%/civil_3P/plugins`;
- usuario importa arquivo `.py` pela GUI;
- aplicacao copia o arquivo para o diretorio interno de plugins;
- loader escaneia, valida contrato e registra plugin disponivel.

## Regras de Seguranca Minima

- bloquear plugins sem classe base esperada;
- bloquear versoes de API incompativeis;
- registrar erro detalhado sem interromper toda a aplicacao.

## Ciclo de Vida

1. Descobrir modulos.
2. Importar dinamicamente.
3. Validar assinatura de contrato.
4. Registrar no catalogo de tarefas.
5. Executar por contexto de selecao.

## Fronteiras

- plugin nao acessa widgets Qt diretamente;
- plugin nao manipula objetos PyVista diretamente;
- plugin atua sobre DTOs de contexto entregues pela aplicacao.

## Ver Tambem

- [07 - Selection](07-selection.md)
- [08 - Results](08-results.md)
- [13 - Check Plugins](13-check-plugins.md)
- [14 - Design Plugins](14-design-plugins.md)
- [18 - Error Handling](18-error-handling.md)
