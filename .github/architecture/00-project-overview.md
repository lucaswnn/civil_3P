# 00 - Project Overview

## Objetivo

civil_3P e uma plataforma desktop para analise de modelos de elementos finitos, com foco em:

- visualizacao 3D do modelo;
- exploracao de resultados;
- verificacao e dimensionamento por plugins.

## Problema Resolvido

Softwares FEM exportam dados heterogeneos. O civil_3P cria uma convencao interna unica para permitir:

- interoperabilidade entre fontes de dados;
- pipelines de visualizacao e consulta consistentes;
- extensibilidade por plugins sem quebrar o nucleo.

## Escopo Funcional

- Importar dados em CSV (origens SAP2000, MIDAS Civil, SCIA Engineer).
- Converter para modelo interno padronizado.
- Exibir malha e atributos em 3D com interacao.
- Selecionar elementos e aplicar tarefas.
- Executar plugins de check/design em 1D e 2D.
- Persistir overrides locais de propriedades.

## Subsistemas

- `core`: entidades de dominio, resultados, materiais, overrides e contratos base.
- `importers`: adaptadores de entrada e conversao para o modelo interno.
- `visualization`: renderizacao 3D e interacao.
- `tasks`: framework e execucao de tarefas (check/design/visualizacoes internas).
- `gui`: interface PySide6 com padrao MVC.

## Metas Nao Funcionais

- Tipagem estatica completa.
- Coesao alta, baixo acoplamento e Open/Closed.
- Suporte a grandes modelos com estrategia de desempenho progressiva.
- Empacotamento para Windows como executavel.

## Ver Tambem

- [01 - Guiding Principles](01-guiding-principles.md)
- [02 - Project Structure](02-project-structure.md)
- [03 - Domain Model](03-domain-model.md)
