-- ============================================================
-- DQL - SCRIPT DE CONSULTAS
-- Sistema de Gestão de Clínica Odontológica
-- Disciplina: Banco de Dados | UNIFSA
-- Professor: Anderson Costa
-- Autor: Vladimir Gustavo
-- ============================================================

-- ============================================================
-- CONSULTA 1 - INNER JOIN
-- Relatório geral de atendimentos
-- Retorna todas as consultas com nome do paciente e dentista
-- ============================================================

SELECT
    c.id_consulta           AS "ID",
    p.nome                  AS "Nome Paciente",
    d.nome                  AS "Nome Dentista",
    d.especialidade         AS "Especialidade",
    c.data_hora             AS "Data e Hora",
    c.status                AS "Status",
    c.valor_procedimento    AS "Valor (R$)"
FROM consultas c
INNER JOIN pacientes p ON c.id_paciente_fk = p.id_paciente
INNER JOIN dentistas d ON c.id_dentista_fk = d.id_dentista
ORDER BY c.data_hora ASC;

-- ============================================================
-- CONSULTA 2 - LEFT JOIN
-- Lista todos os pacientes com suas consultas (se houver)
-- Pacientes sem consulta aparecem com data NULL
-- ============================================================

SELECT
    p.nome          AS "Nome Paciente",
    p.cpf           AS "CPF",
    p.email         AS "E-mail",
    c.data_hora     AS "Data da Consulta",
    c.status        AS "Status da Consulta"
FROM pacientes p
LEFT JOIN consultas c ON p.id_paciente = c.id_paciente_fk
ORDER BY p.nome ASC;

-- ============================================================
-- CONSULTA 3 - Filtro por status
-- Lista todas as consultas agendadas ou confirmadas
-- ============================================================

SELECT
    c.id_consulta   AS "ID",
    p.nome          AS "Paciente",
    d.nome          AS "Dentista",
    c.data_hora     AS "Data e Hora",
    c.status        AS "Status"
FROM consultas c
INNER JOIN pacientes p ON c.id_paciente_fk = p.id_paciente
INNER JOIN dentistas d ON c.id_dentista_fk = d.id_dentista
WHERE c.status IN ('Agendada', 'Confirmada')
ORDER BY c.data_hora ASC;

-- ============================================================
-- CONSULTA 4 - Contagem de consultas por dentista
-- ============================================================

SELECT
    d.nome              AS "Dentista",
    d.especialidade     AS "Especialidade",
    COUNT(c.id_consulta) AS "Total de Consultas"
FROM dentistas d
LEFT JOIN consultas c ON d.id_dentista = c.id_dentista_fk
GROUP BY d.id_dentista, d.nome, d.especialidade
ORDER BY "Total de Consultas" DESC;
