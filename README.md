# Trabalho de Banco de Dados - 2ª Nota

Este repositório contém o trabalho prático da disciplina de Banco de Dados. O objetivo é demonstrar a integração de uma aplicação **Python** com um banco de dados relacional **PostgreSQL (Supabase)**, realizando operações completas de CRUD, controle de acesso por perfis de usuário e consultas complexas com JOINs.

---

##  Sobre o Projeto

O tema escolhido para este trabalho foi um **Sistema de Gestão de Clínica Odontológica**, operado via **terminal (console)**. O sistema permite gerenciar pacientes, dentistas, consultas e perfis de acesso, com autenticação por login e restrição de funcionalidades conforme o cargo do usuário (`admin` ou `recepcionista`). Todas as operações são integradas diretamente ao banco de dados PostgreSQL hospedado no Supabase.

---

##  Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Banco de Dados:** PostgreSQL (via Supabase)
- **Driver de Conexão:** `psycopg2`
- **Autenticação:** Sistema próprio via tabela `perfis` + token administrativo
- **Interface:** Console (Terminal)

---

##  Estrutura do Repositório

A organização dos arquivos segue as exigências da disciplina:

- `/diagrama`: Modelo Entidade-Relacionamento (DER) — `Diagrama_ER.pdf`
- `/ddl`: Scripts de criação das tabelas (`CREATE TABLE`, `CONSTRAINTS`, `TRIGGERS`, `RLS`)
- `/dml`: Scripts de manipulação de dados (`INSERT`, `UPDATE`, `DELETE`)
- `/dql`: Scripts de consulta (`SELECT`, `INNER JOIN`, `LEFT JOIN`)
- `/projeto`: Código-fonte da aplicação Python (`main.py`)

---

##  Modelo de Dados

O banco é composto pelas seguintes tabelas:

- **`pacientes`** — Armazena nome, CPF, data de nascimento, telefone e e-mail
- **`dentistas`** — Armazena nome, CRO e especialidade
- **`consultas`** — Registra o agendamento entre paciente e dentista, com data/hora, status (`Agendada`, `Confirmada`, `Finalizada`, `Cancelada`) e valor do procedimento
- **`perfis`** — Controla os usuários e cargos do sistema (`admin`, `dentista`, `recepcionista`, `paciente`), com políticas de Row Level Security (RLS)

---

##  Controle de Acesso

O sistema possui autenticação por login com dois níveis de permissão:

| Cargo | Permissões |
|---|---|
| **Admin** | Acesso total — cadastra, edita, exclui pacientes, dentistas, consultas e perfis. Requer token de segurança no login. |
| **Recepcionista** | Pode cadastrar pacientes, agendar consultas, consultar e alterar status. Não acessa funções administrativas. |

---

## Demonstração (Prints do Sistema)

### 1. Tela de Login com Autenticação por Cargo
![Tela de Login](tela_login.png)

### 2. Menu Principal com as 13 Operações Disponíveis
![Menu Principal](menu_principal.png)

### 3. Relatório Completo de Atendimentos (INNER JOIN)
![Relatório JOIN](relatorio_join.png)

---

##  Como Executar o Projeto

### Configuração do Banco de Dados

1. Acesse o projeto no [Supabase](https://supabase.com) ou configure um servidor PostgreSQL local.
2. Execute o script de criação das tabelas:
   ```
   /ddl/script_criacao.sql
   ```
3. (Opcional) Popule o banco com dados iniciais:
   ```
   /dml/script_insercao.sql
   ```

### Executando em Python

4. Clone o repositório:
   ```bash
   git clone https://github.com/JeytheJo/SistemaCRUD_Barbearia.git
   cd SistemaCRUD_Barbearia
   ```

5. Instale as dependências:
   ```bash
   pip install psycopg2-binary
   ```

6. Execute o sistema:
   ```bash
   python main.py
   ```

7. Na tela de login, informe seu `usuario_login` cadastrado na tabela `perfis`. Administradores precisam informar o token de segurança adicional.

---

##  Regras de Negócio e Consultas Complexas

O sistema implementa as seguintes consultas complexas:

- **INNER JOIN:** Relatório geral de atendimentos — lista todas as consultas com o nome real do paciente e do dentista vinculados, ordenadas por ID decrescente.

```sql
SELECT c.id_consulta, p.nome AS paciente, d.nome AS dentista, c.status, c.data_hora
FROM consultas c
INNER JOIN pacientes p ON c.id_paciente_fk = p.id_paciente
INNER JOIN dentistas d ON c.id_dentista_fk = d.id_dentista
ORDER BY c.id_consulta DESC;
```

- **LEFT JOIN:** Lista todos os pacientes cadastrados e exibe a data da consulta quando houver — pacientes sem consulta aparecem com data `NULL`.

```sql
SELECT p.nome AS "Nome Paciente", p.cpf AS "CPF", c.data_hora AS "Data da Consulta"
FROM pacientes p
LEFT JOIN consultas c ON p.id_paciente = c.id_paciente_fk
ORDER BY p.nome;
```

---

##  Funcionalidades do Sistema

| Opção | Função | Cargo Necessário |
|---|---|---|
| 01 | Cadastrar novo paciente | Admin / Recepcionista |
| 02 | Cadastrar novo dentista | Admin |
| 03 | Criar novo acesso (login) | Admin |
| 04 | Consultar/filtrar pacientes | Admin / Recepcionista |
| 05 | Agendar nova consulta | Admin / Recepcionista |
| 06 | Relatório completo (JOINs) | Admin / Recepcionista |
| 07 | Excluir cadastro de paciente | Admin |
| 08 | Excluir cadastro de dentista | Admin |
| 09 | Listar usuários do sistema | Admin / Recepcionista |
| 10 | Remover acesso do sistema | Admin |
| 11 | Listar dentistas cadastrados | Admin / Recepcionista |
| 12 | Editar cadastro de paciente | Admin / Recepcionista |
| 13 | Alterar status de consulta | Admin / Recepcionista |

---

##  Autor

- **Vladimir Gustavo**
- **Professor:** Anderson Costa — [andersoncosta@unifsa.com.br](mailto:andersoncosta@unifsa.com.br)
- **Centro Universitário Santo Agostinho (UNIFSA)**
