import sys
import os
import psycopg2
import getpass
from psycopg2 import extras
from datetime import datetime

caminho_lib = os.path.expanduser("~/.local/lib/python3.12/site-packages")
if caminho_lib not in sys.path:
    sys.path.append(caminho_lib)

TOKEN_ADMIN = "7799" 

def conectar():
    try:
        return psycopg2.connect(
            host="aws-1-sa-east-1.pooler.supabase.com",
            port="6543",
            database="postgres",
            user="postgres.ychsyvoeiajhckhhhimz",
            password="RDni8xesT5QJnuU4",
            connect_timeout=10
        )
    except Exception as e:
        print("\n" + "!"*60)
        print(f" [ERRO CRÍTICO DE CONEXÃO]: ".center(60))
        print(f" {e} ".center(60))
        print("!"*60)
        return None

def consulta_filtrada():
    print("\n" + " CONSULTA DE PACIENTES ".center(60, "-"))
    filtro = input("Digite o nome para buscar (ou pressione Enter para todos): ").strip()
    
    print("\nEscolha como os resultados devem ser exibidos:")
    print(" [A] - Ordem Alfabética (A-Z)")
    print(" [D] - Ordem Alfabética (Z-A)")
    print(" [R] - Registros Recentes (ID Decrescente)")
    
    escolha = input("Opção de ordenação: ").strip().upper()
    
    if escolha == "A":
        ordem_sql = "LOWER(nome) ASC"
    elif escolha == "D":
        ordem_sql = "LOWER(nome) DESC"
    else:
        ordem_sql = "id_paciente DESC"
    
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=extras.DictCursor)
            # AJUSTE: Adicionado "AND nome != ''" para não listar registros vazios
            query = f"SELECT id_paciente, nome, cpf FROM pacientes WHERE nome ILIKE %s AND nome != '' AND nome IS NOT NULL ORDER BY {ordem_sql}"
            cursor.execute(query, (f'%{filtro}%',))
            registros = cursor.fetchall()
            
            if registros:
                print("\n" + " LISTAGEM DE PACIENTES ENCONTRADOS ".center(60, "="))
                print(f"{'ID'.ljust(6)} | {'NOME DO PACIENTE'.ljust(30)} | {'CPF'}")
                print("-" * 60)
                for p in registros:
                    nome_exibir = p[1] if p[1] else "SEM NOME"
                    print(f"{str(p[0]).ljust(6)} | {nome_exibir.ljust(30)} | {p[2]}")
            else:
                print("\n[AVISO]: Nenhum paciente corresponde aos critérios de busca.")
        except Exception as e:
            print(f"\n[ERRO AO EXECUTAR CONSULTA]: {e}")
        finally:
            conn.close()

def listar_dentistas():
    print("\n" + " EQUIPE DE DENTISTAS CADASTRADOS ".center(60, "-"))
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=extras.DictCursor)
            cursor.execute("SELECT id_dentista, nome, cro, especialidade FROM dentistas ORDER BY nome ASC")
            registros = cursor.fetchall()
            
            if registros:
                print(f"{'ID'.ljust(6)} | {'NOME DO DENTISTA'.ljust(25)} | {'CRO'.ljust(12)} | {'ESPECIALIDADE'}")
                print("-" * 75)
                for d in registros:
                    print(f"{str(d[0]).ljust(6)} | {d[1].ljust(25)} | {d[2].ljust(12)} | {d[3]}")
            else:
                print("\n[AVISO]: Não existem dentistas cadastrados no banco de dados.")
        except Exception as e:
            print(f"\n[ERRO AO LISTAR EQUIPE]: {e}")
        finally:
            conn.close()

def atualizar_paciente():
    print("\n" + " FORMULÁRIO DE EDIÇÃO DE PACIENTE ".center(60, "-"))
    id_alvo = input("Informe o ID do Paciente que deseja editar: ").strip()
    
    print("DICA: Deixe o campo em branco caso não queira alterar o valor atual.")
    novo_nome = input("Informe o NOVO NOME: ").strip()
    novo_email = input("Informe o NOVO E-MAIL: ").strip()
    
    if not novo_nome and not novo_email:
        print("\n[SISTEMA]: Nenhuma alteração foi realizada (campos vazios).")
        return

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            if novo_nome:
                cursor.execute("UPDATE pacientes SET nome = %s WHERE id_paciente = %s", (novo_nome, id_alvo))
            if novo_email:
                cursor.execute("UPDATE pacientes SET email = %s WHERE id_paciente = %s", (novo_email, id_alvo))
            
            conn.commit()
            
            if cursor.rowcount > 0:
                print("\n" + "="*50)
                print(" [SUCESSO]: Dados atualizados no banco de dados! ".center(50))
                print("="*50)
            else:
                print("\n[ERRO]: O ID informado não foi localizado no sistema.")
        except Exception as e:
            print(f"\n[ERRO NA OPERAÇÃO DE UPDATE]: {e}")
        finally:
            conn.close()

def alterar_status_consulta():
    print("\n" + " GERENCIAMENTO DE STATUS DE CONSULTA ".center(60, "-"))
    id_con = input("Digite o ID da Consulta para atualizar: ").strip()
    
    print("\nSelecione o novo status para o registro:")
    print(" [1] Agendada     [2] Confirmada")
    print(" [3] Finalizada   [4] Cancelada")
    
    op_status = input("Sua escolha: ").strip()
    
    mapa = {"1": "Agendada", "2": "Confirmada", "3": "Finalizada", "4": "Cancelada"}
    novo_status = mapa.get(op_status)

    if not novo_status:
        print("\n[ERRO]: A opção selecionada é inválida.")
        return

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE consultas SET status = %s WHERE id_consulta = %s", (novo_status, id_con))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"\n[OK]: Consulta {id_con} atualizada com sucesso para '{novo_status}'.")
            else:
                print("\n[ERRO]: Nenhuma consulta foi encontrada com o ID informado.")
        except Exception as e:
            print(f"\n[ERRO AO ATUALIZAR STATUS]: {e}")
        finally:
            conn.close()

def realizar_login():
    print("\n" + "=".center(60, "="))
    print("  SISTEMA DE GESTÃO ODONTOLÓGICA - ACESSO RESTRITO  ".center(60))
    print("=".center(60, "="))
    
    tentativa_login = input("Identificação de Usuário (Login): ").strip()
    
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=extras.DictCursor)
            cursor.execute("SELECT cargo, usuario_login FROM perfis WHERE usuario_login ILIKE %s", (tentativa_login,))
            usuario_db = cursor.fetchone()
            
            if usuario_db:
                cargo = usuario_db['cargo'].lower()
                nome_formatado = usuario_db['usuario_login'].upper()
                
                if cargo == 'admin':
                    print(f"\nBem-vindo, Administrador {nome_formatado}. Confirmação necessária.")
                    token_input = getpass.getpass("Token de Segurança Administrativo: ")
                    if token_input == TOKEN_ADMIN:
                        return nome_formatado, cargo, "ADMINISTRAÇÃO"
                    else:
                        print("\n[NEGADO]: Token incorreto. Acesso administrativo bloqueado.")
                        return None, None, None
                
                print(f"\nBem-vindo(a), {nome_formatado}. Acesso liberado.")
                return nome_formatado, cargo, "RECEPÇÃO"
            else:
                print("\n[ERRO]: Usuário inexistente ou login incorreto.")
        finally:
            conn.close()
    return None, None, None

def listar_usuarios_sistema():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            print("\n" + " CONTROLE DE USUÁRIOS DO SISTEMA ".center(60, "-"))
            cursor.execute("SELECT usuario_login, cargo FROM perfis ORDER BY cargo ASC")
            print(f"{'USUÁRIO'.ljust(20)} | {'NÍVEL DE PERMISSÃO'}")
            print("-" * 50)
            for perfil in cursor.fetchall():
                print(f"{perfil[0].ljust(20)} | {perfil[1]}")
        finally:
            conn.close()

def menu():
    user, cargo, label = realizar_login()
    if not user:
        return
    
    while True:
        print("\n" + "║" + "="*58 + "║")
        print(f"║ USUÁRIO: {user.ljust(20)} | STATUS: {label.ljust(23)} ║")
        print("║" + "="*58 + "║")
        print(" 01. Cadastrar Novo Paciente      | 02. Cadastrar Novo Dentista")
        print(" 03. Criar Novo Acesso (Login)    | 04. Consultar/Filtrar Pacientes")
        print(" 05. Agendar Nova Consulta        | 06. Relatório Completo (JOINs)")
        print(" 07. Excluir Cadastro de Paciente | 08. Excluir Cadastro de Dentista")
        print(" 09. Listar Equipe de Acesso      | 10. Remover Acesso do Sistema")
        print(" 11. Listar Dentistas Cadastrados | 12. Editar Cadastro de Paciente")
        print(" 13. Alterar Status de Consulta   | 00. Sair do Sistema")
        print("-" * 60)
        
        opcao = input("Selecione a operação desejada: ").strip()

        opcoes_admin = ['02','2','03','3','07','7','08','8','10']
        if opcao in opcoes_admin and cargo != 'admin':
            print("\n" + "!"*50)
            print(" [ACESSO NEGADO]: Função restrita ao ADMIN. ".center(50))
            print("!"*50)
            continue
        
        if opcao in ['1', '01']:
            print("\n" + " NOVO PACIENTE ".center(40, "-"))
            nome = input("Nome: ").strip()
            cpf = input("CPF: ").strip()
            email = input("E-mail: ").strip()

            # AJUSTE: Impede cadastro se o nome estiver vazio
            if not nome:
                print("\n[ERRO]: Não é possível cadastrar um paciente sem nome.")
                continue

            conn = conectar()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO pacientes(nome, cpf, email) VALUES(%s, %s, %s)", (nome, cpf, email))
                    conn.commit()
                    print("\n[SUCESSO]: Paciente incluído com êxito.")
                finally:
                    conn.close()

        elif opcao in ['2', '02']:
            print("\n" + " NOVO DENTISTA ".center(40, "-"))
            nome, cro, especialidade = input("Nome: "), input("CRO: "), input("Especialidade: ")
            conn = conectar()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO dentistas(nome, cro, especialidade) VALUES(%s, %s, %s)", (nome, cro, especialidade))
                    conn.commit()
                    print("\n[SUCESSO]: Dentista incluído com êxito.")
                finally:
                    conn.close()

        elif opcao in ['3', '03']:
            print("\n" + " NOVO PERFIL DE ACESSO ".center(40, "-"))
            novo_u = input("Defina o Nome de Usuário: ").strip()
            print("Cargos suportados pelo banco: 'admin' ou 'recepção'")
            novo_c = input("Defina o Cargo: ").strip().lower()
            
            conn = conectar()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO perfis (usuario_login, cargo) VALUES (%s, %s)", (novo_u, novo_c))
                    conn.commit()
                    print(f"\n[SUCESSO]: O acesso para '{novo_u}' foi configurado.")
                except Exception as ex:
                    conn.rollback()
                    print("\n" + "X"*50)
                    print(" [ERRO NO BANCO DE DADOS] ".center(50))
                    print(f" Motivo: {ex} ".center(50))
                    print(" Dica: O cargo deve ser exatamente 'admin' ou 'recepção'. ".center(50))
                    print("X"*50)
                finally:
                    conn.close()

        elif opcao in ['4', '04']:
            consulta_filtrada()

        elif opcao in ['5', '05']:
            print("\n" + " NOVO AGENDAMENTO ".center(40, "-"))
            id_p = input("Informe o ID do Paciente: ")
            id_d = input("Informe o ID do Dentista: ")
            
            conn = conectar()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_paciente FROM pacientes WHERE id_paciente = %s", (id_p,))
                    if not cursor.fetchone():
                        print("\n[ERRO]: Paciente não encontrado no banco."); continue
                    
                    cursor.execute("SELECT id_dentista FROM dentistas WHERE id_dentista = %s", (id_d,))
                    if not cursor.fetchone():
                        print("\n[ERRO]: Dentista não encontrado no banco."); continue

                    print("\nStatus Inicial: [1] Agendada | [2] Confirmada")
                    status_inicial = {"1": "Agendada", "2": "Confirmada"}.get(input("Escolha: "), "Agendada")
                    
                    cursor.execute("""
                        INSERT INTO consultas (id_paciente_fk, id_dentista_fk, status, data_hora) 
                        VALUES (%s, %s, %s, %s)
                    """, (id_p, id_d, status_inicial, datetime.now()))
                    conn.commit()
                    print("\n[SUCESSO]: Consulta registrada no cronograma.")
                finally:
                    conn.close()

        elif opcao in ['6', '06']:
            conn = conectar()
            if conn:
                try:
                    cursor = conn.cursor(cursor_factory=extras.DictCursor)
                    cursor.execute("""
                        SELECT c.id_consulta, p.nome as paciente, d.nome as dentista, c.status, c.data_hora 
                        FROM consultas c 
                        JOIN pacientes p ON c.id_paciente_fk = p.id_paciente 
                        JOIN dentistas d ON c.id_dentista_fk = d.id_dentista
                        ORDER BY c.id_consulta DESC
                    """)
                    dados = cursor.fetchall()
                    print("\n" + " RELATÓRIO GERAL DE ATENDIMENTOS ".center(70, "="))
                    for linha in dados:
                        data_f = linha['data_hora'].strftime('%d/%m/%Y %H:%M') if linha['data_hora'] else "N/A"
                        print(f"ID: {str(linha[0]).zfill(3)} | Paciente: {linha[1].ljust(15)} | Dent: {linha[2].ljust(15)}")
                        print(f"Status: {linha[3].ljust(12)} | Horário: {data_f}")
                        print("-" * 70)
                finally:
                    conn.close()

        elif opcao in ['7', '07', '8', '08']:
            tabela = "pacientes" if opcao in ['7', '07'] else "dentistas"
            campo_id = "id_paciente" if opcao in ['7', '07'] else "id_dentista"
            alvo_del = input(f"Informe o ID do registro para remover de {tabela}: ")
            
            conn = conectar()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM {tabela} WHERE {campo_id} = %s", (alvo_del,))
                    conn.commit()
                    if cursor.rowcount > 0:
                        print(f"\n[OK]: Registro removido com sucesso de {tabela}.")
                    else:
                        print("\n[AVISO]: O ID informado não existe.")
                except:
                    print("\n[IMPEDIMENTO]: Não é possível excluir; este registro possui consultas vinculadas.")
                finally:
                    conn.close()

        elif opcao in ['9', '09']:
            listar_usuarios_sistema()

        elif opcao == '10':
            alvo_remov = input("Informe o Login para revogar acesso: ").strip()
            if alvo_remov.upper() != user:
                conn = conectar()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM perfis WHERE usuario_login ILIKE %s", (alvo_remov,))
                    conn.commit()
                    print(f"\n[OK]: Acesso de '{alvo_remov}' removido.") if cursor.rowcount > 0 else print("\n[!] Não encontrado.")
                    conn.close()
            else:
                print("\n[ERRO]: Protocolo de segurança impede que você remova seu próprio acesso.")

        elif opcao == '11':
            listar_dentistas()

        elif opcao == '12':
            atualizar_paciente()

        elif opcao == '13':
            alterar_status_consulta()

        elif opcao in ['0', '00']:
            print("\n[ENCERRANDO]: Sistema finalizado. Até breve!")
            break
        else:
            print("\n[OPÇÃO INVÁLIDA]: Por favor, tente novamente.")

if __name__ == "__main__":
    menu()