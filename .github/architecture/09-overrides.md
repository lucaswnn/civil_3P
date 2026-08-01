# 09 - Overrides

## Objetivo

Registrar sobrescritas de propriedades sem modificar os dados importados originais.

## Exemplos De Propriedades Cobertas

- material;
- espessura;
- secao de barra;
- coeficientes de projeto;
- outras propriedades de calculo configuraveis.

## Principio Nao Destrutivo

- modelo importado permanece imutavel;
- overrides sao armazenados separadamente;
- tarefas aplicam overrides em tempo de execucao.

## Modelo de Dados

Cada override deve conter:

- alvo (elemento/grupo);
- propriedade alterada;
- valor antigo (opcional para rastreio);
- valor novo;
- origem/autor/data.

## Fluxo

1. Usuario seleciona elementos.
2. Define sobrescrita na GUI.
3. `OverrideService` valida e persiste.
4. TaskExecution combina dados base + overrides.

## Ver Tambem

- [03 - Domain Model](03-domain-model.md)
- [04 - Application Layer](04-application-layer.md)
- [14 - Design Plugins](14-design-plugins.md)
