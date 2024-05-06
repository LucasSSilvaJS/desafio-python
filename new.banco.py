import os
from datetime import datetime

logs = []

def log(logs):
    def decorator(funcao):
        def activity(*k, **kw):

            funcao_return = funcao(*k, **kw)
            operacao = ""
            nome_funcao = funcao.__name__ 

            if nome_funcao == 'sacar':
                operacao = 'saque'
            elif nome_funcao == 'depositar':
                operacao = 'deposito'
            elif nome_funcao == 'imprimir_extrato':
                operacao = 'extrato'
            
            date_ = f'Operação: {operacao.title()}\nData: {datetime.now().strftime("%d/%m/%Y, %H:%M")}'
            print(date_)
            logs.append(date_)

            return funcao_return
        return activity
    return decorator

def percorrer_extrato(login_conta):
    extrato_da_conta = login_conta.extrato
    registros_individuais = extrato_da_conta.split('\n')
    for registro_individual in registros_individuais:
     yield registro_individual

def filtrar_por(lista_de_operacoes, tipo_de_operacao):
        lista_de_operacoes = [registro for registro in lista_de_operacoes if tipo_de_operacao in registro]
        return lista_de_operacoes

class Usuario:

    def __init__(self, nome, data_nascimento, cpf, endereco) -> None:
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class Conta:

    def __init__(self, numero_da_conta, usuario) -> None:
        self.agencia = '0001'
        self.numero_da_conta = numero_da_conta
        self.usuario = usuario
        self.saldo = 0.00
        self.quantidade_de_saque_diario = 0
        self.extrato = ''

class Login:
    
    def __init__(self) -> None:
        self.login_conta = None

    def logado(self):
        return True if self.login_conta else False
    
    def fazer_login(self, conta):
        if not self.logado():
            self.login_conta = conta
    
    def deslogar(self):
        self.login_conta = None

class Saque:
    def __init__(self, valor) -> None:
        self.valor = valor
        self.valor_limite_de_saque = 500
        self.limite_de_quantidade_de_saque = 3

    @log(logs)
    def sacar(self, login_conta):
        if self.valor > 0:
            if login_conta.saldo >= self.valor:
                if self.valor <= self.valor_limite_de_saque and login_conta.quantidade_de_saque_diario < self.limite_de_quantidade_de_saque:
                    login_conta.saldo -= self.valor
                    login_conta.quantidade_de_saque_diario += 1
                    print(f'Você realizou um saque de R$ {self.valor:.2f}')
                    print()
                    login_conta.extrato += f'Saque realizado no valor de R$ {self.valor:.2f}\n'
                else:
                    if login_conta.quantidade_de_saque_diario >= self.limite_de_quantidade_de_saque:
                        print('Quantidade de saque diário passou do limite')
                        print()
                    if self.valor > self.valor_limite_de_saque:
                        print('O saque ultrapassou o limite máximo de R$ 500')
                        print()
            else:
                print('Não será possível sacar o dinheiro por falta de saldo')
                print()
        else:
            print('Operação falhou! O valor informado é inválido.')
            print()

class Deposito:
    def __init__(self, valor) -> None:
        self.valor = valor
    @log(logs)
    def depositar(self, login_conta):
        if self.valor > 0:
            login_conta.saldo += self.valor
            print(f'Você realizou um depósito de R$ {self.valor:.2f}')
            print()
            login_conta.extrato += f'Depósito realizado no valor de R$ {self.valor:.2f}\n'
        else:
            print('Operação falhou! O valor informado é inválido.')
            print()

class Extrato:
    def imprimir_extrato(self, login_conta):
        if login_conta.extrato:
            login_conta.extrato += f'Saldo total: R$ {login_conta.saldo:.2f}\n'
            print(login_conta.extrato)
            login_conta.extrato = login_conta.extrato.replace(f'Saldo total: R$ {login_conta.saldo:.2f}\n', '')
            enter_para_continuar()
        else:
            print('Você não possui movimentações em sua conta')
            enter_para_continuar()
    
    def filtrar_extrato(self, login_conta, filtro=None):
        filtro = input('Digite [d] para consultar os depósitos realizados\nou [s] para consultar os saques: ')
        
        if filtro.lower() == 'd':
            filtro = 'Depósito'
        elif filtro.lower() == 's':
            filtro = 'Saque'
        
        apresentacao_do_extrato = ''
        lista_de_operacoes = percorrer_extrato(login_conta)

        if filtro == 'Saque' or filtro == 'Depósito':
            apresentacao_do_extrato += apresentacao_do_extrato + '\n'.join(filtrar_por(lista_de_operacoes, filtro))
        else:
            apresentacao_do_extrato += apresentacao_do_extrato + '\n'.join(lista_de_operacoes)

        limpar_console()
        print(apresentacao_do_extrato)
        enter_para_continuar()

class Banco:
    def __init__(self) -> None:
        self.usuarios = []
        self.contas = []
        self.numero_da_conta = 0

    def adicionar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def gerar_numero_da_conta(self):
        self.numero_da_conta += 1
        return self.numero_da_conta

def limpar_console():
    os.system('cls')

def enter_para_continuar():
    print()
    input('Digite enter para continuar: ')
    limpar_console()

def mensagem_menu():
    menu = '''
        Seja bem-vindo ao nosso banco!        

        [l] Login
        [o] Deslogar
        [u] Cadastrar usuário
        [c] Criar conta
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [f] Filtrar Extrato
        [q] Sair
        
        Selecione uma opção: '''
    return menu

def main():
    banco = Banco()
    login = Login()
    extrato = Extrato()

    menu = mensagem_menu()
    while True:
        opcao = input(menu).lower()
        if opcao == 'd':
            limpar_console()
            if not login.logado():
                print('É preciso estar logado para efetuar essa operação')
                enter_para_continuar()
                continue
            valor = float(input('Digite um valor para depósito: '))
            deposito = Deposito(valor)
            deposito.depositar(login.login_conta)
            enter_para_continuar()
        elif opcao == 'l':
            limpar_console()
            print('Tela de login\n')
            agencia = input('Digite o número de sua agência: ')
            numero_da_conta = int(input('Digite o número de sua conta: '))
            if not(agencia and numero_da_conta):
                print('É preciso informar sua agência e conta para realizar o login')
                enter_para_continuar()
                continue
            conta_encontrada = None
            for conta in banco.contas:
                if conta.agencia == agencia and conta.numero_da_conta == numero_da_conta:
                    conta_encontrada = conta
                    break
            if conta_encontrada:
                print('Login efetuado')
                login.fazer_login(conta_encontrada)
                enter_para_continuar()
            else:
                print('Conta não encontrada')
                enter_para_continuar()
        elif opcao == 'o':
            limpar_console()
            login.deslogar()
            print('Conta desconectada')
            enter_para_continuar()
        elif opcao == 'u':
            limpar_console()
            print('Cadastro de usuário\n')
            nome = input('Digite seu nome completo: ')
            data_de_nascimento = input('Digite sua data de nascimento (dd-mm-aaaa): ')
            cpf = input('Digite seu CPF: ')
            endereco = input('Digite seu endereço completo: ')
            if not(nome and data_de_nascimento and cpf and endereco):
                print('É preciso informar todos os dados')
                enter_para_continuar()
                continue
            usuario = Usuario(nome, data_de_nascimento, cpf, endereco)
            banco.adicionar_usuario(usuario)
            print('Usuário cadastrado com sucesso!')
            enter_para_continuar()
        elif opcao == 'c':
            limpar_console()
            print('Cadastro de conta\n')
            cpf = input('Digite seu CPF: ')
            if not cpf:
                print('É preciso informar o CPF')
                enter_para_continuar()
                continue
            usuario_encontrado = None
            for usuario in banco.usuarios:
                if usuario.cpf == cpf:
                    usuario_encontrado = usuario
                    break
            if usuario_encontrado:
                numero_da_conta = banco.gerar_numero_da_conta()
                conta = Conta(numero_da_conta, usuario_encontrado)
                banco.adicionar_conta(conta)
                print(f'Agência: {conta.agencia}')
                print(f'Número da conta: {conta.numero_da_conta}')
                print('Conta cadastrada com sucesso!\n')
                enter_para_continuar()
            else:
                print('Erro! É necessário possuir um cadastro de usuário')
                enter_para_continuar()
        elif opcao == 's':
            limpar_console()
            if not login.logado():
                print('É preciso estar logado para efetuar essa operação')
                enter_para_continuar()
                continue
            valor = float(input('Digite um valor para saque: '))
            saque = Saque(valor)
            saque.sacar(login.login_conta)
            enter_para_continuar()
        elif opcao == 'e':
            limpar_console()
            if not login.logado():
                print('É preciso estar logado para efetuar essa operação')
                enter_para_continuar()
                continue
            extrato.imprimir_extrato(login.login_conta)
        elif opcao == 'f':
            limpar_console()
            if not login.logado():
                print('É preciso estar logado para efetuar essa operação')
                enter_para_continuar()
                continue
            extrato.filtrar_extrato(login.login_conta)
        elif opcao == 'q':
            limpar_console()
            print('Obrigado pela preferência! Volte sempre :)')
            print()
            enter_para_continuar()
            break
        else:
            limpar_console()
            print('Operação inválida! Por favor, selecione novamente a operação desejada.')
            print()
            enter_para_continuar()

if __name__ == "__main__":
    main()