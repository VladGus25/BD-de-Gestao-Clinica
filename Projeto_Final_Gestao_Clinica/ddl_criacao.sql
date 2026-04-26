-- ============================================================
-- DDL - SCRIPT DE CRIAÇÃO DAS TABELAS
-- Sistema de Gestão de Clínica Odontológica
-- Disciplina: Banco de Dados | UNIFSA
-- Professor: Anderson Costa
-- Autor: Vladimir Gustavo
-- ============================================================

-- Tabela de Pacientes
CREATE TABLE pacientes (
    id_paciente     SERIAL PRIMARY KEY,
    nome            VARCHAR(100) NOT NULL,
    cpf             CHAR(11) UNIQUE NOT NULL,
    data_nascimento DATE,
    telefone        VARCHAR(15),
    email           VARCHAR(100),
    id_usuario      UUID REFERENCES auth.users(id)
);

-- Tabela de Dentistas
CREATE TABLE dentistas (
    id_dentista  SERIAL PRIMARY KEY,
    nome         VARCHAR(100) NOT NULL,
    cro          VARCHAR(20) UNIQUE NOT NULL,
    especialidade VARCHAR(50),
    id_usuario   UUID REFERENCES auth.users(id)
);

-- Tabela de Consultas
CREATE TABLE consultas (
    id_consulta         SERIAL PRIMARY KEY,
    id_paciente_fk      INT REFERENCES pacientes(id_paciente) ON DELETE CASCADE,
    id_dentista_fk      INT REFERENCES dentistas(id_dentista) ON DELETE RESTRICT,
    data_hora           TIMESTAMPTZ NOT NULL,
    status              VARCHAR(20) DEFAULT 'Agendada'
                            CHECK (status IN ('Agendada', 'Confirmada', 'Finalizada', 'Cancelada')),
    valor_procedimento  DECIMAL(10,2),
    observacoes         TEXT
);

-- Tabela de Perfis (Cargos de Acesso)
CREATE TABLE perfis (
    id            UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY DEFAULT gen_random_uuid(),
    cargo         TEXT CHECK (cargo IN ('admin', 'dentista', 'recepcionista', 'paciente')) DEFAULT 'paciente',
    usuario_login VARCHAR(255) UNIQUE,
    senha         VARCHAR(255)
);

-- ============================================================
-- CONSTRAINTS ADICIONAIS
-- ============================================================

ALTER TABLE consultas
    ADD CONSTRAINT fk_paciente
    FOREIGN KEY (id_paciente_fk) REFERENCES pacientes(id_paciente);

ALTER TABLE consultas
    ADD CONSTRAINT fk_dentista
    FOREIGN KEY (id_dentista_fk) REFERENCES dentistas(id_dentista);

-- ============================================================
-- TRIGGERS
-- ============================================================

-- Função: cria perfil automaticamente ao cadastrar novo usuário
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.perfis(id, cargo)
    VALUES (new.id, 'paciente');
    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger: executa a função ao inserir novo usuário
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- ============================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================

-- Habilitar RLS nas tabelas
ALTER TABLE pacientes  ENABLE ROW LEVEL SECURITY;
ALTER TABLE dentistas  ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultas  ENABLE ROW LEVEL SECURITY;
ALTER TABLE perfis     ENABLE ROW LEVEL SECURITY;

-- PERFIS: qualquer usuário autenticado pode ler
CREATE POLICY "Leitura de perfis para todos logados"
    ON perfis FOR SELECT TO authenticated
    USING (true);

-- PERFIS: apenas admin pode criar novos perfis
CREATE POLICY "Admins criam perfis"
    ON perfis FOR INSERT TO authenticated
    WITH CHECK (
        EXISTS (SELECT 1 FROM perfis WHERE id = auth.uid() AND cargo = 'admin')
    );

-- PACIENTES: o próprio paciente ou funcionários podem visualizar
CREATE POLICY "Ver pacientes"
    ON pacientes FOR SELECT TO authenticated
    USING (
        id_usuario = auth.uid()
        OR EXISTS (
            SELECT 1 FROM perfis
            WHERE id = auth.uid() AND cargo IN ('admin', 'dentista', 'recepcionista')
        )
    );

-- PACIENTES: apenas admin pode deletar
CREATE POLICY "Apenas admin deleta pacientes"
    ON pacientes FOR DELETE TO authenticated
    USING (
        EXISTS (SELECT 1 FROM perfis WHERE id = auth.uid() AND cargo = 'admin')
    );

-- DENTISTAS: qualquer autenticado pode visualizar
CREATE POLICY "Leitura pública de dentistas"
    ON dentistas FOR SELECT TO authenticated
    USING (true);

-- DENTISTAS: apenas admin pode criar, editar e excluir
CREATE POLICY "Apenas admin edita dentistas"
    ON dentistas FOR ALL TO authenticated
    USING (
        EXISTS (SELECT 1 FROM perfis WHERE id = auth.uid() AND cargo = 'admin')
    );

-- DENTISTAS: apenas admin pode deletar
CREATE POLICY "Apenas admin deleta dentistas"
    ON dentistas FOR DELETE TO authenticated
    USING (
        EXISTS (SELECT 1 FROM perfis WHERE id = auth.uid() AND cargo = 'admin')
    );

-- CONSULTAS: o paciente da consulta ou funcionários podem visualizar
CREATE POLICY "Ver consultas"
    ON consultas FOR SELECT TO authenticated
    USING (
        id_paciente_fk IN (
            SELECT id_paciente FROM pacientes WHERE id_usuario = auth.uid()
        )
        OR EXISTS (
            SELECT 1 FROM perfis
            WHERE id = auth.uid() AND cargo IN ('admin', 'dentista', 'recepcionista')
        )
    );

-- CONSULTAS: apenas admin ou recepcionista podem agendar
CREATE POLICY "Agendar consultas"
    ON consultas FOR INSERT TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM perfis
            WHERE id = auth.uid() AND cargo IN ('admin', 'recepcionista')
        )
    );

-- CONSULTAS: apenas admin pode deletar
CREATE POLICY "Deletar consultas"
    ON consultas FOR DELETE TO authenticated
    USING (
        EXISTS (SELECT 1 FROM perfis WHERE id = auth.uid() AND cargo = 'admin')
    );
