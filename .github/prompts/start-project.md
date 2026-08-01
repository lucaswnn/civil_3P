Quero fazer um programa que serve para visualizar resultados, dimensionamento ou verificação de elementos finitos. O programa capta dados tabulares de algum programa de elementos finitos como sap2000 ou midas civil ou scia engineer (dados do modelo e resultados) e o usuário escolhe o que quer fazer. O programa mostra o modelo 3d e o usuário pode mover, rotacionar, selecionar elementos e fazer algumas operações de visualização, dimensionamento ou verificação. O programa usa uma interface gráfica. Ele é feito em python com as bibliotecas mais indicadas para visualização científica em 3d. O programa usa a estrutura de projeto .toml e deve gerar um executável. O dimensionamento e verificação seguem o princípio do aberto e fechado, em que o usuário pode criar nobos arquivos python para dimensionamentos e verificações específicas. O usuário também pode associar e sobrescrever algumas propriedades de elementos finitos selecionados. O usuário carrega um arquivo python personalizado e a i terface é capaz de detectar esse arquivo para escolher a tarefa a ser feita. A tarefa a ser feita depende dos elementos finitos selecionados. As tarefas só podem ser feitas em elementos 1d e 2d. Cada tarefa serve apenas para um tipo de elemento. A tarefa é feita em elementos selecionados. Todos os dados são importados e convertidos para a convenção interna do projeto, como espessura das placas ou material. Para elementos de placa, deve existir a opção de resultado por elemento e resultado por nó. As tarefas de visualização não podem ter arquivos python personalizados, mas devem seguir o princípio do aberto fechado para o desenvolvedor criar novas funcionalidades. O modo de importação dos dados dos softwares também deve seguir o princípio aberto fechado;

Qual formato de de dados importará: csv;

Os plugins .py ficarão em uma pasta interna. O usuário deve criar seu plugin e importar pelo programa, que copiará esse .py para a pasta interna;


A plataforma alvo é windows;

O toolkit de interface gráfica é PySide6;

A biblioteca 3D usada será uma combinação de pyvista e VTK;

A api do plugin será por meio de uma classe abstrata, devendo o usuário implementar essa classe abstrata;

Resultados importados: no caso de elementos 1d, são passados por pontos intervalados, do início ao fim. No caso de elementos 2d, são passados por seus pontos;

Propriedades sobrescritas: material, espessura, seção de barra, coeficientes de projeto, outras propriedades, sendo que essas propriedades nao alteram o modelo importado, sao salvos como overrides;

Escopo do projeto: visualização 3d, seleção de elementos, colormap de resultados, tabela de resultados, plugins de verificação, plugins de dimensionamento;

arquitetura desejada: hexagonal, mas com um toque de mvc para a parte gráfica;

O programa deve ter uma padronização dos elementos finitos para tornar extensível;

Subsistemas recomendados: "core" (modelo que implementa em geral elementos finitos, propriedades de material, casos de carga, combinaçoes, resultados e overrides, assim como outras features centrais de modelo), "importers" (sistema que importa os dados dos softwares e transforma os dados para o "core"), "visualization" (módulo responsável pela renderização 3d do modelo, seleção de elementos e resultados), "tasks" (módulo responsável por dimensionamentos, verificações, consultas, ferramentas etc, tudo baseado em plugins), "GUI" (PySide6, menus ,dock widgets, paineis, tabela de resultados etc);

Seu papel é documentar todo o projeto nos arquivos criados na pasta github. O arquivo copilot-instructions.md deve documentar em linhas gerais o projeto e indexar os subarquivos da pasta architecture. Os subarquivos da pasta architecture devem esclarecer os seguintes pontos:
- Filosofia e objetivos do projeto.
- Arquitetura geral (Hexagonal + MVC na GUI).
- Organização completa do repositório.
- Modelo de domínio (Core).
- Convenções para entidades de elementos finitos.
- Modelo interno unificado.
- Sistema de importadores (Adapter + Factory).
- Sistema de renderização (PyVista/VTK).
- Sistema de seleção e interação.
- Sistema de resultados (nodal, por elementos, com média, sem média).
- Sistema de overrides.
- Sistema de plugins (classes base abstratas, descoberta e carregamento).
- API para plugins de dimensionamento.
- API para plugins de verificação.
- Sistema de visualizações internas.
- Serviços da aplicação.
- GUI em PySide6.
- Padrões de projeto obrigatórios.
- Convenções de código.
- Tratamento de erros e logging.
- Estratégia de testes.
- Desempenho e escalabilidade.
- Geração do executável para Windows.
- Regras específicas que o GitHub Copilot deve seguir e evitar.
o projeto deve adotar Python 3.13+, tipagem estática completa, dataclasses, pytest;

O arquivo copilot-instructions.md também deve possuir regras para o Copilot:
- Nunca:
 -- quebrar Open/Closed.
 -- acoplar importadores ao domínio.
 -- acessar PyVista dentro do domínio.
 -- colocar regras de negócio na GUI.
 -- acessar widgets Qt fora da camada GUI.

- Sempre:
 -- usar interfaces.
 -- usar composição.
 -- usar injeção de dependências.
 -- manter alta coesão;