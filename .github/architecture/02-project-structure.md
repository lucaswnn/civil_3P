# 02 - Project Structure

## Objetivo

Definir a organizacao do repositorio para manter fronteiras claras entre dominio, adaptadores e interface.

## Estrutura Recomendada

```text
src/
	civil_3P/
		core/
		application/
		importers/
		visualization/
		tasks/
		gui/
		infrastructure/
tests/
	unit/
	integration/
	e2e/
plugins_internal/
docs/
.github/
```

## Responsabilidades por Pasta

- `core`: entidades, value objects, contratos de resultado e convencoes FEM.
- `application`: casos de uso, servicos e coordenacao.
- `importers`: adaptadores CSV por software de origem e fabrica de importadores.
- `visualization`: backend de render, colormap e picking.
- `tasks`: sistema de plugins e visualizacoes internas.
- `gui`: janelas, paineis, comandos UI e adaptadores MVC.
- `infrastructure`: logging, persistencia local, configuracao e paths.

## pyproject.toml

O projeto deve centralizar configuracoes de:

- build system;
- dependencias runtime/dev;
- ferramentas de qualidade (ruff/mypy/pytest);
- metadados de empacotamento.

## Plataforma Alvo

- Windows como plataforma primaria.
- Compatibilidade deve ser validada com Python 3.13+.

## Convencoes de Dependencia

- `core` sem dependencia de frameworks de UI/render.
- `application` conhece portas e DTOs, nao widgets.
- `gui` e `visualization` conectadas por adaptadores de apresentacao.

## Build e Distribuicao

Detalhes de empacotamento, assets e release estao em:

- [19 - Build and Deployment](19-build-deployment.md)

## Ver Tambem

- [01 - Guiding Principles](01-guiding-principles.md)
- [10 - Importers](10-importers.md)
- [05 - GUI](05-gui.md)
