# 19 - Build and Deployment

## Objetivo

Padronizar empacotamento e distribuicao do civil_3P como executavel Windows.

## Base de Build

- configuracoes centralizadas em `pyproject.toml`;
- dependencias runtime/dev separadas;
- validacao de tipagem, lint e testes antes de empacotar.

## Empacotamento Windows

Ferramenta recomendada: PyInstaller (ou equivalente) com:

- binario principal do app;
- assets de GUI;
- plugins internos necessarios;
- configuracoes padrao.

## Itens de Runtime

- garantir distribuicao de dependencias PySide6/PyVista/VTK;
- validar path de plugins de usuario: `%APPDATA%/civil_3P/plugins`;
- criar diretorio de dados de app quando ausente.

## Checklist de Release

1. Executar testes automatizados.
2. Validar tipagem estatica.
3. Gerar executavel.
4. Testar instalacao limpa em Windows.
5. Validar importacao CSV e renderizacao 3D.
6. Validar carregamento de plugin check/design.
7. Validar logs e recuperacao de erros comuns.

## Estrategia de Versao

- versao semantica para aplicacao;
- compatibilidade de API de plugin registrada por versao;
- notas de release com mudancas de contrato.

## Ver Tambem

- [02 - Project Structure](02-project-structure.md)
- [16 - Testing](16-testing.md)
- [18 - Error Handling](18-error-handling.md)
