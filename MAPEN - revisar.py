# importando bibliotecas:

import json # para salvar dados em arquivos em formato de dicionario
import os # para limpar tela do console através de função
from datetime import datetime # para registrar data e hora de cada dado adicionado no sistema

# criando variáveis:

dados_cadastro = {} # dicionario para armazenar os dados e salvar no arquivo 'dados_cadastro.json'
historico_app = [] # lista que vai receber dicionarios de cada registro e salvar no arquivo 'dados_app.json'

# função que limpa o console de acordo com o sistema operacional
def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

print('Bem vindo ao MAPEN. Siga as instruções abaixo para navegar pelo sistema.')

while True:

    # trata o erro caso o usuario digite uma letra ou símbolo inválido no menu
    try:
        opcoes = int(input('''
  [ MAPEN - MENU PRINCIPAL ]
  -----------------------------------
  1. Criar conta
  2. Fazer login
  3. Inserir novos dados da empresa
  4. Consultar relatório e acumulado
  5. Deletar dados da empresa
  6. Sair do sistema
  -----------------------------------
  Escolha uma opção: '''))
    except ValueError:
        limpar_tela()
        print('⚠ Por favor, digite apenas números correspondentes às opções.\n')
        continue # volta para o início do loop principal

# criando o match case para navegar pelo sistema e cadastro de login:
    match opcoes:
        case 1:
            limpar_tela()
            print('--- CADASTRO DE EMPRESA ---')
            while True:
                input_usuario = str(input('Nome da empresa: '))
                input_senha = str(input('Senha: '))
                confirmar_senha = str(input('Repita a senha: '))

                if input_senha == confirmar_senha:
                    
                    # tenta carregar os usuários já existentes antes de salvar. Se não tiver dados, cria um dicionario vazio dados_cadastro
                    try:
                        with open('dados_cadastro.json', 'r', encoding='utf-8') as arquivo:
                            dados_cadastro = json.load(arquivo)
                    except (FileNotFoundError, json.decoder.JSONDecodeError):
                        dados_cadastro = {}

                    dados_cadastro[input_usuario] = input_senha

                    with open('dados_cadastro.json', 'w', encoding = 'utf-8') as arquivo:
                        json.dump(dados_cadastro, arquivo, ensure_ascii = False, indent = 4)
                    
                    limpar_tela()
                    print(f'✓ Empresa "{input_usuario}" cadastrada com sucesso!\n')
                    break

                else:
                    print('\n⚠ Senhas não coincidem. Tente novamente.\n')

  # criando sistema de login:
        case 2:
            limpar_tela()
            print('--- ACESSO AO SISTEMA ---')
            try:
                with open('dados_cadastro.json', 'r', encoding='utf-8') as arquivo:
                    cadastro = json.load(arquivo)
            except (FileNotFoundError, json.decoder.JSONDecodeError):        
                cadastro = {}
            # solicita input dos dados de login e senha
            while True:
                login = input('Login: ')
                senha = input('Senha: ')
              
                # procura a 'chave' login no cadastro e comparar com o 'valor' senha
                if login in cadastro and senha == cadastro[login]:
                    limpar_tela()
                    print(f'✓ Logado com sucesso como: {login}!\n')
                    break
                else:
                    print('\n⚠ Dados incorretos. Tente novamente.\n')

    # criando dicionario de dados da empresa:
        case 3:
            limpar_tela()
            print('--- INSERIR DADOS DA EMPRESA ---')
            
            # carrega o histórico existente em uma lista de dicionarios ou cria uma lista vazia se FileNotFoundError 
            try:
                with open('dados_app.json', 'r', encoding='utf-8') as arquivo:
                    historico_app = json.load(arquivo)
                    # garante que dados antigos em formato de dicionário simples não quebrem o sistema
                    if isinstance(historico_app, dict):
                        historico_app = []
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                historico_app = []

            ###### trata entradas inválidas nos campos numéricos
            try:
                # Criamos um dicionário temporário para o registro atual
                novo_registro = {}
                novo_registro['data_hora'] = datetime.now().strftime('%d/%m/%Y %H:%M')
                novo_registro['regiao'] = input('Insira a região: ')
                novo_registro['qtd_kw_enviado'] = float(input('Quantidade de kW enviados: '))
                novo_registro['qtd_kw_recebido'] = float(input('Quantidade de kW recebidos: '))
                
                novo_registro['energia_perdida'] = (novo_registro['qtd_kw_enviado'] - novo_registro['qtd_kw_recebido'])
                novo_registro['perda_R$'] = novo_registro['energia_perdida'] * 0.77
                
                # adiciona registro em historico_app e salva no JSON
                historico_app.append(novo_registro)
                
                with open('dados_app.json', 'w', encoding = 'utf-8') as arquivo:
                    json.dump(historico_app, arquivo, ensure_ascii = False, indent = 4)
                
                limpar_tela()
                print('✓ Novo registro adicionado ao histórico com sucesso!\n')
                
            except ValueError:
                limpar_tela()
                print('⚠ Erro: Certifique-se de digitar números válidos (use ponto para decimais).\n')

    # consultando os dados criados da empresa:
        case 4:
            limpar_tela()
            try:
                with open('dados_app.json', 'r', encoding='utf-8') as arquivo:
                    historico_app = json.load(arquivo)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                historico_app = []

            if not historico_app or len(historico_app) == 0:
                print('⚠ Nenhum dado da empresa foi cadastrado no sistema.\n')
                continue

            print('=====================================================')
            print('          RELATÓRIO DETALHADO POR PERÍODO            ')
            print('=====================================================')
            
            # variáveis acumuladoras do relatório 
            total_enviado = 0
            total_recebido = 0
            total_perdido = 0
            total_prejuizo = 0
            
            # exibindo o registro detalhado de cada lançamento (relatorio de consulta)
            for i, registro in enumerate(historico_app, 1):
                print(f" Lançamento #{i} - {registro.get('data_hora')}")
                print(f" • Região:           {registro.get('regiao')}")
                print(f" • kW Enviados:      {registro.get('qtd_kw_enviado')} kW")
                print(f" • kW Recebidos:     {registro.get('qtd_kw_recebido')} kW")
                print(f" • Energia Perdida:  {registro.get('energia_perdida')} kW")
                print(f" • Prejuízo:         R$ {registro.get('perda_R$'):.2f}")
                print('-----------------------------------------------------')
                
                # somando os valores ao acumulado do período
                total_enviado += registro.get('qtd_kw_enviado', 0)
                total_recebido += registro.get('qtd_kw_recebido', 0)
                total_perdido += registro.get('energia_perdida', 0)
                total_prejuizo += registro.get('perda_R$', 0)

            # exibindo o relatório consolidado e acumulado do período
            print('============= RESUMO ACUMULADO DO PERÍODO ===========')
            print(f" Total de kW Enviados no período:   {total_enviado:.2f} kW")
            print(f" Total de kW Recebidos no período:  {total_recebido:.2f} kW")
            print(f" Total de Energia Perdida acumulada: {total_perdido:.2f} kW")
            print(f" Prejuízo Financeiro Total:         R$ {total_prejuizo:.2f}")
            print('=====================================================\n')

    # deletando os dados criados da empresa:
        case 5:
            limpar_tela()
            try:
                with open('dados_app.json', 'r', encoding='utf-8') as arquivo:
                    historico_app = json.load(arquivo)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                historico_app = []

            if not historico_app:
                print('⚠ Não existem dados salvos para serem deletados.\n')
                continue

            while True:
                print('--- OPÇÕES DE EXCLUSÃO ---')
                print('1. Apagar o ÚLTIMO registro inserido')
                print('2. Apagar TODO o histórico (Limpeza Total)')
                print('3. Voltar ao menu principal')
                print('--------------------------')
                
                try:
                    opcao_del = int(input('Escolha uma opção de exclusão: '))
                except ValueError:
                    print('Por favor, escolha 1, 2 ou 3.\n')
                    continue

                match opcao_del:
                    case 1:
                        confirmar = input('Apagar apenas o último lançamento realizado? (S/N): ').lower()
                        if confirmar == 's':
                            # remove o último elemento da lista usando .pop() sem argumentos
                            historico_app.pop()
                            with open('dados_app.json', 'w', encoding='utf-8') as arquivo:
                                json.dump(historico_app, arquivo, ensure_ascii=False, indent=4)
                            
                            limpar_tela()
                            print('✓ O último registro foi removido com sucesso!\n')
                            break
                        else:
                            limpar_tela()
                            print('Operação cancelada.\n')
                            break

                    case 2:
                        confirmar = input('Tem certeza que deseja apagar TODO o histórico? (S/N): ').lower()
                        if confirmar == 's':
                            historico_app = []
                            with open('dados_app.json', 'w', encoding='utf-8') as arquivo:
                                json.dump(historico_app, arquivo)
                            
                            limpar_tela()
                            print('✓ Histórico completamente limpo!\n')
                            break
                        else:
                            limpar_tela()
                            print('Operação cancelada.\n')
                            break

                    case 3:
                        limpar_tela()
                        break
                    case _:
                        print('Opção inválida. Escolha 1, 2 ou 3.')

        case 6:
            limpar_tela()
            print('Saindo do sistema MAPEN. Até logo!')
            break

        case _:
            limpar_tela()
            print('⚠ Opção inválida. Escolha um número de 1 a 6.\n')
