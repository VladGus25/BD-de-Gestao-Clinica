-- ============================================================
-- DML - SCRIPT DE MANIPULAÇÃO DE DADOS
-- Sistema de Gestão de Clínica Odontológica
-- Disciplina: Banco de Dados | UNIFSA
-- Professor: Anderson Costa
-- Autor: Vladimir Gustavo
-- ============================================================

-- ============================================================
-- INSERT - Inserção de dados iniciais
-- ============================================================

-- Inserindo Dentistas
INSERT INTO dentistas (nome, cro, especialidade) VALUES
    ('Dean Gus',   '4452-88',  'Cirurgião'),
    ('Gustavo Jin', '2545-96', 'Botox'),
    ('Kilon F',    '52563-78', 'SLA');

-- Inserindo Pacientes
INSERT INTO pacientes (nome, cpf, email) VALUES
    ('Léo Flix',       '11111111111', 'leoflix@email.com'),
    ('Dinilsoon Hues', '22222222222', 'dinilsoon@email.com'),
    ('Fernando Dilo',  '33333333333', 'fernando@email.com');

-- Inserindo Perfis de Acesso
INSERT INTO perfis (usuario_login, cargo) VALUES
    ('Vladimir',  'admin'),
    ('Nayelle',   'recepcionista');

-- ============================================================
-- INSERT - Agendando Consultas
-- ============================================================

INSERT INTO consultas (id_paciente_fk, id_dentista_fk, data_hora, status) VALUES
    (1, 3, '2026-04-25 18:19:00+00', 'Cancelada'),
    (2, 2, '2026-04-25 17:48:00+00', 'Confirmada'),
    (3, 2, '2026-04-25 17:44:00+00', 'Agendada');

-- ============================================================
-- UPDATE - Atualização de dados
-- ============================================================

-- Atualizar status de uma consulta
UPDATE consultas
    SET status = 'Finalizada'
    WHERE id_consulta = 1;

-- Atualizar dados de um paciente
UPDATE pacientes
    SET email = 'novoemail@email.com'
    WHERE id_paciente = 1;

-- Promover usuário para admin
UPDATE perfis
    SET cargo = 'admin'
    WHERE usuario_login = 'Vladimir';

-- ============================================================
-- DELETE - Remoção de dados
-- ============================================================

-- Remover um paciente pelo ID
DELETE FROM pacientes
    WHERE id_paciente = 3;

-- Remover acesso de um usuário do sistema
DELETE FROM perfis
    WHERE usuario_login = 'usuario_exemplo';

-- Cancelar (deletar) uma consulta pelo ID
DELETE FROM consultas
    WHERE id_consulta = 2;
