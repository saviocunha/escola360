# Escola360 — Dashboard de Acompanhamento Escolar

O Escola360 é uma aplicação de gestão escolar que modela o ecossistema de uma instituição de ensino. Desenvolvido com foco em boas práticas de programação, extensibilidade e manutenibilidade, o sistema oferece uma base sólida para o gerenciamento acadêmico.

> **Aviso:** O sistema ainda está em fase de desenvolvimento.

---

## Sobre o projeto

Visto que, na maior parte das escolas públicas de educação básica, principalmente no interior, o acompanhamento da vida escolar do aluno ainda depende de registros em papel e planilhas isoladas. Ademais, as notas ficam com o professor, a frequência fica na secretaria e os avisos chegam à família por bilhete no caderno. 

Percebemos o quanto a comunicação é fragmentada,  o responsável só descobre que o filho está com notas baixas ou faltando na reunião de fim de bimestre, quando já é tarde para intervir. Do outro lado, o gestor não tem indicadores consolidados para agir sobre evasão e baixo rendimento, e o professor perde horas em tarefas administrativas repetitivas.

Dessa forma, resolvemos centralizar as informações acadêmicas dos alunos e criar um canal de comunicação direto entre a escola, os professores, os alunos e os responsáveis. O sistema reúne em um único lugar: notas, frequência, calendário e avisos, com uma visão diferente para cada perfil, de modo que a informação certa chegue à pessoa certa em tempo real.


- Acesse o site: https://saviocunha.github.io/escola360/

---

## Características Principais

- Gestão de múltiplos tipos de usuários (professores, alunos, responsáveis, gestores)
- Controle completo de notas e frequência
- Sistema de disciplinas curriculares
- Geração de relatórios
- Arquitetura modular e extensível

---
## Possíveis Usos do Escola360

Embora seja um projeto de fins didáticos, o Escola360 já representa um núcleo que pode ser expandido em várias direções:

**1. Backend de um sistema escolar web ou mobile:**
Servir como camada de domínio em uma API (Flask, FastAPI ou Django), expondo endpoints para cadastro de usuários e disciplinas, lançamento de notas, registro de frequência e geração de relatórios.

**2. Ferramenta de acompanhamento pedagógico:**
Permitir que professores e gestores registrem avaliações e presenças em tempo real, gerem relatórios por aluno, turma ou disciplina, e exportem dados em CSV/JSON.

**3. Portal de pais e alunos:**
Alimentar um portal onde responsáveis e alunos acessam informações em tempo real — notificações de ocorrências, agendamento de reuniões e acompanhamento de atividades escolares.

**4. Integração com ERPs escolares:**
Atuar como módulo de "vida acadêmica" (notas, frequências, boletins) e fonte de dados para dashboards de desempenho e evasão escolar.

---

## Visão Geral do Projeto (Backend)

O projeto está organizado em módulos, cada um representando uma parte do domínio:

| Arquivo          | Descrição                                                                                   |
|------------------|---------------------------------------------------------------------------------------------|
| `usuarios.py`    | Classes base (`Usuario`, `Autenticavel`, `GeradorRelatorio`) e papéis de gestão, ensino e acompanhamento (`Professor`, `Gestor`, `Responsavel`). |
| `aluno.py`       | Implementação da classe `Aluno` e seus métodos de consulta de dados acadêmicos.             |
| `disciplinas.py` | Implementação da classe `Disciplina` e seu registro de notas e frequências.                 |
| `avaliacao.py`   | Classes que representam registros acadêmicos (`Nota` e `Frequencia`).                       |
| `relatorios.py`  | Classe simples para o objeto `Relatorio`, usado pelo `Gestor`.                              |
| `main.py`        | Script de demonstração para testar as funcionalidades e relações entre as classes.          |

---

## Como Executar

Certifique-se de ter o **Python 3.10+** instalado e que todos os arquivos estejam na mesma pasta. No terminal, navegue até a pasta do projeto e execute:

```bash
python main.py
```

Você deverá ver uma saída semelhante a:

```
--- 1. CRIAÇÃO DE ENTIDADES ---
Professor criado: João Silva (ID: 10)
----------------------------------------
--- 2. TESTES DE AUTENTICAÇÃO ---
Login de João Silva: SUCESSO.
Login de João Silva: FALHA (esperado).
----------------------------------------
--- 3. LANÇAMENTO DE NOTAS E VALIDAÇÃO ---
Nota 9.0 em Matemática lançada com sucesso.
Nota 7.5 em Português lançada com sucesso.
Teste de Erro de Nota: SUCESSO. Erro capturado: valor da nota deve estar entre 0 e 10
----------------------------------------
--- 4. TESTES DE FREQUÊNCIA E CÁLCULOS ---
Total de Aulas de Matemática: 5
Presenças: 3 | Faltas: 2
Porcentagem de Frequência: 60.00%
----------------------------------------
--- 5. TESTES DE RELACIONAMENTO ---
Notas registradas para Ana Pereira:
  > Matemática: 9.0 (Prova Mensal)
  > Português: 7.5 (Trabalho)
Notas registradas em Matemática:
  > Aluno: Ana Pereira, Nota: 9.0
```

> Os textos exatos podem variar conforme adaptações no arquivo `main.py`.

---

## Conceitos de Design e Boas Práticas

Este projeto foi desenvolvido como um modelo de domínio didático, aplicando boas práticas de Programação Orientada a Objetos (POO):

**Herança e polimorfismo**
`Usuario` é a classe base abstrata, enquanto `Gestor`, `Professor`, `Responsavel` e `Aluno` especializam seu comportamento. Interfaces como `Autenticavel` e `GeradorRelatorio` definem contratos claros.

**Encapsulamento**
Atributos privados (`__nome`, `__notas`, `__frequencias` etc.) são expostos via properties, retornando apenas o necessário. As coleções são retornadas como cópias para evitar modificação externa direta.

**Validação de regras de negócio**
Notas limitadas entre 0 e 10, status de frequência restrito a `"P"` ou `"F"`, e-mail com formato mínimo, ID positivo e CPF não vazio.

**Consistência do modelo**
Ao lançar uma nota ou registrar uma frequência, o código atualiza simultaneamente as listas do `Professor`, do `Aluno` e da `Disciplina`, garantindo que todos os lados do relacionamento se mantenham sincronizados.

---

## Banco de Dados

O projeto físico do banco de dados foi desenvolvido com **PostgreSQL**, escolhido por seu suporte robusto, integridade referencial, constraints avançadas e conformidade com os padrões SQL.

**Dominar essa etapa é fundamental, principalmente para quem está aprendento a programar**. Um projeto físico bem feito é essencial para qualquer aplicação séria. Entender a lógica por trás da criação das tabelas, dos relacionamentos, das chaves, ajuda o estudante a desenvolver sistemas mais robustos, organizados e profissionais. Além disso, quando o banco de dados é mal implementado o código do programa (front-end e back-end) fica mais complexo, lento e cheio de "gambiarras" para compensar as falhas na estrutura de dados.
O diagrama abaixo é uma representação simplificada no banco de dados criado para o Escola360. O código SQL e o diagrama lógico estão nos arquivos do projeto.

```mermaid
---
title: Banco de Dados - Escola360
---
graph TD
    USUARIOS[Usuarios] --> ALUNOS[Alunos]
    USUARIOS --> PROFESSORES[Professores]
    USUARIOS --> GESTORES[Gestores]
    USUARIOS --> RESPONSAVEIS[Responsaveis]

    ALUNOS --- TURMAS[Turmas]
    ALUNOS --- RA{Responsavel_Aluno}
    RESPONSAVEIS --- RA

    PROFESSORES --- LOT{Prof_Turma_Lotacao}
    TURMAS --- LOT
    DISCIPLINAS[Disciplinas] --- LOT

    ALUNOS --- NOTAS[Notas]
    ALUNOS --- FREQUENCIAS[Frequencias]

    PROFESSORES --- NOTAS
    PROFESSORES --- FREQUENCIAS

    DISCIPLINAS --- NOTAS
    DISCIPLINAS --- FREQUENCIAS

    USUARIOS --- AVISOS[Avisos]
```

---

## Prototipação da Interface (Wireframe)

Antes do desenvolvimento completo do frontend de qualquer projeto, é uma prática recomendada realizar a prototipação da interface utilizando wireframes. Um wireframe é uma representação visual simplificada da interface de um sistema, utilizada para planejar a organização dos elementos da tela, a navegação entre páginas e a experiência do usuário (UX), sem focar inicialmente em cores, tipografia ou design visual final. No projeto **Escola360**, o processo de criação do wireframe seguiu uma abordagem baseada em **Design Centrado no Usuário (DCU)**, priorizando as necessidades reais dos diferentes perfis que utilizam a plataforma.

### Perfis de Usuário

| Perfil        | Necessidade principal                                                                 |
|---------------|--------------------------------------------------------------------------------------|
| Gestor        | Visão macroscópica da instituição, com acesso a indicadores gerais e ferramentas administrativas. |
| Professor     | Operações acadêmicas rápidas: lançamento de notas, calendário, avisos e registro de frequência.          |
| Aluno         | Consulta de informações acadêmicas: boletim, calendário e avisos.                    |
| Responsável   | Acompanhamento do desempenho do aluno: boletim, frequência e comunicados da escola.  |

#### A identificação desses perfis é essencial para orientar as decisões de design da interface.

### Funcionalidades Principais

- Login e autenticação de usuários
- Gerenciamento de turmas, disciplinas e usuários
- Dashboard com indicadores acadêmicos
- Lançamento de notas e registro de frequência
- Consulta de boletim escolar
- Comunicação escolar (avisos)
- Geração de relatórios

### Estrutura de Navegação (Sitemap)

#### Antes de iniciar o desenho das telas, é importante definir **como o usuário navegará pelo sistema**. Essa estrutura é representada por um **Sitemap**, que demonstra a hierarquia de páginas e a relação entre elas. Essa etapa é essencial para garantir:

- organização da informação
- clareza de navegação
- escalabilidade do sistema

```
Login
 ├── Dashboard Gestor
 │    ├── Gerenciar Usuários
 │    ├── Gerenciar Turmas
 │    ├── Gerenciar Disciplinas
 │    └── Relatórios
 │
 ├── Dashboard Professor
 │    ├── Minhas Turmas
 │    ├── Lançar Notas
 │    ├── Lançar Frequência
 │    └── Comunicação Escolar
 │
 ├── Dashboard Aluno
 │    ├── Boletim Escolar
 │    ├── Calendário de Aulas
 │    └── Mural de Avisos
 │
 └── Dashboard Responsável
      ├── Boletim e Frequência
      ├── Calendário de Aulas
      └── Mural de Avisos
```

## Estruturação de Interface

Nesta etapa, o foco está na **organização dos elementos na tela**, sem preocupação inicial com cores, tipografia ou design visual final. 
O wireframe utiliza **caixas, linhas e blocos estruturais** para representar os componentes da interface.

Em geral, um wireframe deve apresentar:

- Estrutura geral da página
- Menus de navegação
- Botões principais
- Campos de formulário
- Listas e tabelas
- Indicadores e dashboards

#### O wireframe do Escola360 adotou as seguintes diretrizes estruturais:

- Dashboards com indicadores rápidos
- Menu lateral fixo para navegação entre módulos
- Tabelas estruturadas para lançamento de notas e registro de presença
- Mural de avisos para comunicação entre escola, alunos e responsáveis

Essas decisões ajudam a tornar o sistema **mais organizado, intuitivo e eficiente para os usuários**.

### Design Centrado no Usuário (DCU)

O DCU é uma metodologia que coloca o usuário final no centro das decisões de design, considerando suas necessidades, limitações e comportamentos reais. 
No Escola360, esses princípios contribuíram para a redução de erros humanos, melhoria da usabilidade, redução da carga cognitiva e maior eficiência operacional com o objetivo de entregar não apenas código funcional, mas um sistema capaz de resolver problemas reais do ambiente educacional, proporcionando uma experiência digital mais eficiente e acessível. 

## Importância da Experiência do Usuário (UX)

A Experiência do Usuário é o conjunto de percepções, emoções e reações que uma pessoa tem ao interagir com um produto digital. Devemos sempre nos perguntar "como uma pessoa se sente ao usar esse sistema?".

Um sistema pode ter todas as informações que o usuário precisa e ainda assim falhar completamente. Isso acontece quando a interface é confusa, os botões estão no lugar errado, as cores dificultam a leitura ou o fluxo de navegação exige que o usuário adivinhe o próximo passo. E isso leva a desistência do usuário para usá-lo.

Um bom design de interface mostra que a pessoa está no controle, quando o usuário abre o aplicativo e imediatamente entende onde está, o que pode fazer e como chegar onde quer.

No contexto do Escola360, esse risco é especialmente crítico. O nosso usuário principal, que é o pai ou responsável, muitas vezes não tem familiaridade com tecnologia, acessa o aplicativo pelo celular em momentos rápidos do dia e precisa encontrar a informação que busca em segundos. Se a interface não for intuitiva, ele simplesmente para de usar e o problema que a plataforma veio resolver continua existindo.
 
No desenvolvimento do nosso projeto, a preocupação com o UX guiou decisões práticas desde o início: a escolha das cores com base na psicologia visual, a organização das informações mais importantes na tela inicial, a simplicidade dos ícones e a clareza das notificações. Cada uma dessas decisões tem um impacto direto em se um pai em Itapipoca vai abrir o aplicativo amanhã de manhã ou não.
 
E ainda mais importante, o UX tem que ser pensado no quesito de inclusão. Um design bem planejado torna a tecnologia acessível para quem mais precisa dela e é esse compromisso que orienta o desenvolvimento do Escola360.


### Protótipo de Alta Fidelidade (Figma)
 
Após a etapa de wireframe, o projeto Escola360 evoluiu para um protótipo de alta fidelidade, desenvolvido no Figma. Diferente do wireframe, que tem foco estrutural, o protótipo de alta fidelidade representa a interface de forma mais próxima ao produto final, incluindo identidade visual, paleta de cores, tipografia, componentes interativos, organização visual dos elementos, experiência de navegação, responsividade e usabilidade.
 
- [Protótipo no Figma](https://www.figma.com/site/Emqrc76z13FP6LB8lXMvCq/Escola360?node-id=0-1&t=YLUsID5bcvFmgdKQ-1)

---
 
## Arquitetura de Software
 
A arquitetura de software pode ser compreendida como a espinha dorsal que estrutura um sistema. Ela define não apenas seus componentes, mas também as relações entre eles e os princípios que governam sua evolução. Assim como um edifício precisa de um projeto estrutural, um sistema de software necessita de um planejamento arquitetônico para garantir seu funcionamento adequado e eficiente.
 
### Por que a Arquitetura é Importante?
 
A arquitetura permite a **modularização do sistema**, dividindo-o em partes colaborativas, o que possibilita o desenvolvimento paralelo entre equipes e reduz a sobrecarga cognitiva dos desenvolvedores. Ela também atua como um **artefato de comunicação** entre arquitetos, desenvolvedores, gerentes e clientes, alinhando expectativas e orientando decisões técnicas e de negócio.
 
Além disso, as decisões arquiteturais determinam, ainda antes da implementação, as tecnologias que poderão ser utilizadas, como ocorrerá o fluxo de dados entre os componentes e quais trade-offs serão aceitos, como o equilíbrio entre desempenho, escalabilidade e complexidade.
 

### Influência nos Atributos de Qualidade
 
Um dos aspectos mais relevantes da arquitetura é sua influência direta sobre os atributos de qualidade, que definem **como** o sistema se comporta:
 
| Atributo          | Impacto da Arquitetura                                                                                     |
|-------------------|------------------------------------------------------------------------------------------------------------|
| Escalabilidade    | A forma como o sistema é particionado determina sua capacidade de crescimento.                             |
| Segurança         | O isolamento de dados sensíveis e a definição de fronteiras de confiança reduzem a superfície de ataque.   |
| Desempenho        | O arranjo dos componentes e os fluxos de comunicação impactam diretamente a velocidade do sistema.         |
| Manutenibilidade  | Em um sistema bem projetado, alterações em uma regra de negócio não exigem modificações extensas em outros módulos. |
| Evolução          | Uma boa arquitetura protege as regras de negócio das mudanças tecnológicas, evitando reescritas completas. |
 
Concluindo, a qualidade de um projeto de software está diretamente relacionada à qualidade de sua arquitetura. É ela que determina se o software terá uma vida útil longa e sustentável ou então, se tornará um sistema legado de difícil manutenção. 

 - [Clique aqui para visualisar o projeto arquitetural do Escola360.](https://github.com/saviocunha/escola360/blob/main/Projeto_Arquitetural_Escola360.md)

---

## Visao Geral da Interface

O Escola360 é organizado em quatro perfis de acesso, cada um com sua própria
visão do sistema, sobre uma base comum de gestão de usuários, turmas,
disciplinas, notas e frequência.

### Funcionalidades implementadas

- Landing page de apresentacão com chamada para o sistema.
- Páginas institucionais: Sobre nós, Funcionalidades e Suporte.
- Tela de login com campos de e-mail e senha, opcão "Lembrar-me" e link de
  recuperação de senha
- Estrutura base do dashboard, preparada para receber os módulos por perfil
- Layout responsivo para celular, com menu hamburguer implementado apenas em CSS
- Identidade visual aplicada: paleta de cores, tipografia, logo e favicon.

### Funcionalidades previstas

- Autenticação real e controle de acesso por perfil
- Dashboards de gestor, professor, aluno e responsável
- Lançamento de notas e registro de frequência pela interface
- Boletim escolar e mural de avisos
- Geração de relatórios
- Integração entre a interface web e o banco de dados
 
 ---

 ## Interface Web Implementada (prints)

- Página Inicial
- Login
- Funcionalidades
- Sobre Nós

## Tecnologias Utilizadas

### Frontend (entrega desta Sprint)

| Tecnologia | Uso no projeto | Por que foi escolhida |
|---|---|---|
| **HTML5** | Estrutura das seis paginas do site | Marcação semântica (`header`, `nav`, `main`, `section`, `article`, `footer`), que melhora acessibilidade e SEO |
| **CSS3** | Toda a estilização, em um único `style.css` | Flexbox e media queries dão conta da responsividade sem dependências externas |
| **JavaScript** | Diretório reservado para as próximas etapas | O menu hamburguer foi resolvido apenas com CSS, então nenhum script foi necessário no MVP |
| **Google Fonts (DM Sans)** | Tipografia da interface | Fonte sem serifa de alta legibilidade em telas pequenas, ponto critico para o acesso via celular |

### Backend e dados

| Tecnologia | Uso no projeto | Por que foi escolhida |
|---|---|---|
| **Python 3.10+** | Modelagem do domínio em POO | Sintaxe legível e suporte nativo a herança, properties e encapsulamento |
| **PostgreSQL** | Projeto físico do banco de dados | Integridade referencial, constraints avançadas e conformidade com o padrão SQL |

### Ferramentas de desenvolvimento

| Ferramenta | Uso no projeto |
|---|---|
| **Git e GitHub** | Versionamento, hospedagem do código e colaboração entre os integrantes |
| **GitHub Pages** | Publicação do site, permitindo validar o resultado em celulares reais |
| **Visual Studio Code** | Editor padrão da equipe, com a extensão Live Server |
| **Figma** | Protótipo de alta fidelidade |
| **Canva** | Wireframe e sitemap |

## Processo de Desenvolvimento

### Divisão das tarefas

| Integrante | Frente de trabalho |
|---|---|
| Francisco Savio | Home Page, arquitetura de pastas, relatórios |
| Beatriz Benigno | Página de Funcionalidades , identidade visual, menu hambúrguer responsivo, relatórios |
| Diogo Sousa | Tela de login completa (campos, botão, "Lembrar-me", recuperação de senha) correções de responsividade, relatórios |
| Junior Ferreira | Página "Sobre nós", relatórios |

### Uso do GitHub e estratégia de versionamento

O código ficou centralizado em um repositório único, com todo o trabalho
integrado na branch `main`. Cada integrante trabalhava na sua frente e
sincronizava com `git pull` antes de enviar as alterações; as divergências
foram resolvidas por merge, sem perda de trabalho.

### Dificuldades encontradas e soluções adotadas

**Organização inicial dos arquivos.** Os primeiros arquivos foram criados
soltos na raiz do repositório. Conforme o numero de paginas cresceu, ficou
claro que a navegação não escalaria, e a equipe reorganizou tudo nos
diretórios `css/`, `img/`, `js/` e `paginas/`, corrigindo todas as referencias.

**Caminhos absolutos quebravam o site fora da raiz.** As paginas usavam
caminhos absolutos, o que funcionava na maquina de quem escreveu mas quebrava
imagens e estilos ao abrir o site de uma subpasta ou publica-lo no GitHub
Pages. A solução foi converter todas as referencias para caminhos relativos.

**Menu de navegação no celular.** O cabeçalho não cabia em telas pequenas e a
equipe ainda não havia estudado JavaScript. A solução foi implementar o menu
hamburguer apenas com CSS, usando um `checkbox` oculto controlado por um
`label` para guardar o estado de aberto e fechado, o que manteve o site sem
dependência de script.

**Volume do CSS.** Com um único arquivo de estilos passando de 600 linhas,
achar e alterar uma regra virou um gargalo. Foram adicionados comentários
delimitando cada bloco e criado um glossário das propriedades usadas, que
serviu também como material de estudo para a equipe.



## Desenvolvedores

| Nome                              | E-mail                               |
|-----------------------------------|--------------------------------------|
| Aldemir Ferreira da Silva Junior  | junior.ferreira@aluno.ufca.edu.br    |
| Beatriz Benigno de Vasconcelos    | benigno.beatriz@aluno.ufca.edu.br    |
| Francisco Diogo de Sousa Silva    | sousa.diogo@aluno.ufca.edu.br        |
| Francisco Sávio Sousa da Cunha    | savio.cunha@aluno.ufca.edu.br        |
| João Paulo Lima David             | lima.david@aluno.ufca.edu.br         |

---

## Requisitos

- Python 3.10+
- Nenhuma dependência externa

---

## Licença

Uso livre para fins acadêmicos e didáticos.
