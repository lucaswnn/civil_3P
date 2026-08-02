# 17 - Coding Style

## Base Tecnica

- Python 3.13+.
- Tipagem estatica completa em APIs publicas e internas criticas.
- Uso preferencial de `dataclasses` para DTOs e entidades apropriadas.

## Convencoes Gerais

- nomes claros, sem abreviacoes ambiguas;
- funcoes curtas e coesas;
- dependencias injetadas por construtor/fabrica;
- codigo e comentarios escritos em ingles;
- interfaces/protocols para contratos entre camadas.

## Padroes Obrigatorios

- Adapter + Factory para importacao;
- Strategy para variacoes por tipo de elemento/tarefa;
- composicao sobre heranca;
- MVC para Application.

## Regras de Fronteira

- dominio sem Qt/PyVista;
- GUI sem regra de negocio;
- importadores sem acoplamento indevido com dominio;
- plugins sem acesso direto a widgets Qt.

## Erros e Logging

Padroes gerais neste arquivo. Regras detalhadas em:

- [18 - Error Handling](18-error-handling.md)

## Documentacao de Codigo

- docstrings objetivas em APIs publicas;
- exemplos curtos para contratos de plugin;
- comentarios apenas onde o fluxo nao for obvio.

## Ver Tambem

- [01 - Guiding Principles](01-guiding-principles.md)
- [11 - Plugin System](11-plugin-system.md)
- [18 - Error Handling](18-error-handling.md)
