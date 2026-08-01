# 13 - Check Plugins

## Objetivo

Definir API de plugins de verificacao para analise normativa/criterial em elementos selecionados.

## Elegibilidade

- somente elementos 1D e 2D;
- execucao condicionada ao contexto de selecao ativo;
- disponibilidade controlada por tipo de elemento suportado pelo plugin.

## Contrato da Classe Abstrata

Metodos minimos esperados:

- `metadata()`
- `supports(element_type)`
- `validate_input(context)`
- `run_check(context)`
- `build_report(result)`

## Contexto de Entrada

- elementos selecionados (selecao primaria);
- elementos adjacentes quando existirem (vizinhanca candidata);
- propriedades efetivas (base + overrides);
- resultados solicitados;
- configuracoes do usuario para a verificacao.

Observacao: o plugin consome o contexto entregue pela aplicacao. A regra de media com ou sem adjacentes e definida no modulo de resultados.

## Saida Esperada

- status (ok, warning, fail);
- itens de nao conformidade;
- valores calculados e limites;
- relatorio estruturado para GUI/exportacao.

## Restricoes

- sem acesso a widgets Qt;
- sem dependencia de PyVista/VTK;
- sem alteracao de dados originais importados.

## Ver Tambem

- [11 - Plugin System](11-plugin-system.md)
- [07 - Selection](07-selection.md)
- [08 - Results](08-results.md)
- [09 - Overrides](09-overrides.md)
