# 03 - Domain Model

## Objetivo

Definir o modelo interno unificado que representa elementos finitos, propriedades, resultados e overrides de forma agnostica a software de origem.

Este documento tambem concentra as convencoes FEM do projeto e a diretriz de padronizacao tabular das entidades, para que o dominio tenha uma unica fonte de verdade.

## Entidades Centrais

As entidades sao gerenciadas por um banco de dados normalizado, com uso de dataframes da biblioteca pandas.

- `Model`: agregado raiz contendo elementos, nos, materiais, casos de carga, combinacoes e resultados.
- `Node`: coordenadas e metadados estruturais.
- `Element1D`: barra/viga com conectividade, secao, material e outras propriedades.
- `Element2D`: placa/casca com geometria, espessura, material e outras propriedades.
- `Material`: propriedades fisico-mecanicas.
- `Section`: propriedades de secao para elementos 1D.
- `OriginResults1D`: serie de resultados nos pontos intervalados dos elementos 1D vindos dos modelos importados, contendo esforcos, deslocamentos etc e com caso/comb.
- `OriginResults2D`: serie de resultados nos nos dos elementos 2D vindos dos modelos importados, contendo esforcos, deslocamentos etc e com caso/comb.
- `OriginResultsNodes`: serie de resultados nos nos vidos dos modelos importados, contendo reacoes e deslocamentos com caso/comb.
- `OverrideSet`: alteracoes locais nao destrutivas para calculos, mantendo dados importados de origem para historico.
- `TaskResults`: serie de resultados das tarefas realizadas pelo pos-processamento, a partir dos dados importados de outro software e das alteracoes locais, sendo os resultados divididos em 1d e 2d.

## Modelo Interno Unificado

Principios:

- todos os dados externos sao convertidos para contratos internos tipados;
- unidades e convencoes sao normalizadas na importacao;
- o dominio nunca conhece o formato CSV original;
- a representacao interna privilegia entidades tabulares normalizadas para suportar operacoes vetorizadas.

## Convencoes FEM Integradas ao Dominio

### Tipos de Elemento Suportados

- 1D: barras/vigas com conectividade linear.
- 2D: placas/cascas com representacao superficial.

### Convencao Interna de Identificacao

- identificador unico por no e elemento;
- classificacao unificada por `ElementType`;
- propriedades obrigatorias tipadas para material, secao, espessura, orientacao e demais atributos relevantes.

### Representacao de Resultados

- 1D: resultados por pontos intervalados do elemento, do inicio ao fim;
- 2D: resultados nos nos de cada elemento;
- metadados de unidade e localizacao sempre presentes.

### Visualizacao Derivada

Com base nesse modelo interno:

- 1D permite apenas visualizacao por elemento;
- 2D permite visualizacao por elemento, por no com media e por no sem media;
- a regra de media com ou sem vizinhanca pertence ao modulo de Results.

## Entidades Tabulares e DataFrames

O programa deve padronizar seus dados em formatos de tabela, como um banco de dados normalizado representado por dataframes. Essa diretriz existe para:

- facilitar filtros, joins e agregacoes entre entidades;
- aproveitar operacoes vetorizadas com NumPy;
- reduzir transformacoes ad hoc entre importacao, dominio, results e plugins;
- permitir contratos de dados previsiveis entre modulos.

Essa padronizacao e conceitual no nivel do dominio: a documentacao define entidades tabulares normalizadas, sem impor ainda detalhes rigidos de implementacao.

Importante: mesmo que os dados sejam tabulares, devem existir classes para acesso desses dados, de forma a criar uma fachada e desacoplar em caso de mudança da biblioteca de manipulação tabular e vetorial.

### Tabelas Conceituais Minimas

- `nodes_df`: identificacao do no, coordenadas e metadados estruturais.
- `elements_1d_df`: conectividade 1D, material, secao e orientacao.
- `elements_2d_df`: conectividade 2D, material, espessura e orientacao.
- `materials_df`: propriedades dos materiais.
- `sections_df`: propriedades de secao dos elementos 1d.
- `origin_results_1d_df`: resultados de elementos 1d importados por caso/combinacao, elemento e intervalo.
- `origin_results_2d_df`: resultados de elementos 2d importados por caso/combinacao, elemento e no.
- `origin_results_nodes`: resultados de nos por caso/combinacao, contendo deslocamentos e reacoes.
- `overrides_df`: sobrescritas nao destrutivas aplicadas sobre entidades selecionadas.
- `task_results_1d_df`: resultados das tarefas em elementos 1d.
- `task_results_2d_df`: resultados das tarefas em elementos 2d.

### Regras de Normalizacao

- cada entidade deve possuir chave identificadora estavel;
- relacoes entre entidades devem ser explicitas e validaveis;
- duplicacao de atributo deve ser evitada quando existir referencia natural entre tabelas;
- importadores devem mapear nomenclaturas externas para essas tabelas internas.

## Regras de Dominio

- elementos de tarefas: somente 1D e 2D;
- resultados 1D guardam amostras do inicio ao fim do elemento;
- resultados 2D guardam valores nos nos dos elementos;
- resultados 2D solicitados por elemento sao calculados;
- overrides nao alteram o estado de importacao original.

## Contratos Relevantes

- `ElementType`: enum para classificacao interna.
- `ResultLocation`: nodal ou elemento.
- `TaskEligibility`: criterio de habilitacao para check/design.

## Mapeamentos de Origem

Cada importador deve mapear nomenclaturas de origem para a convencao interna do dominio:

- SAP2000 -> tipos internos e propriedades internas;
- MIDAS Civil -> tipos internos e propriedades internas;
- SCIA Engineer -> tipos internos e propriedades internas.

## Fora de Escopo do Dominio

- renderizacao 3D;
- widgets e eventos Qt;
- parser CSV concreto;
- descoberta dinamica de plugins.

## Ver Tambem

- [08 - Results](08-results.md)
- [09 - Overrides](09-overrides.md)
