"""Um programa de terminal onde o usuário pode cadastrar e gerenciar tarefas.

 - Adicionar tarefa
 - Listar tarefas
 - Concluir tarefa
 - Remover tarefa
 - Sair
"""

import json
from time import sleep

#cria o arquivo TaskTracker.json caso não exista
def start():
    try:
        with open("TaskTracker.json", "r") as arquivo:
            json.load(arquivo)
    except FileNotFoundError:
        with open("TaskTracker.json", "x") as arquivo:
            json.dump({"tarefas":[]}, arquivo, indent=4)
    except json.JSONDecodeError:
        with open("TaskTracker.json", "w") as arquivo:
            json.dump({"tarefas":[]}, arquivo, indent=4)
start()

def listar():
    with open("TaskTracker.json", "r") as arquivo:
        lista = json.load(arquivo)
        print(json.dumps(lista, indent=4))

def adicionar():
    with open("TaskTracker.json", "r") as arquivo:
        add = json.load(arquivo)
        nome = str(input("Digite o nome da tarefa\n-> "))
        descricao = str(input("Digite a descrição da tarefa\n-> "))
        with open("TaskTracker.json", "w") as arquivo:
            add["tarefas"].append({"ID":1,
                                "nome":nome,
                                "descricao":descricao})
            json.dump(add, arquivo, indent=4)

def remover():
    pass

def deletar():
    delete = str(input("Deseja deletar? (S/n)\n->"))
    if delete.upper() == "S":
        print("Vc tem certeza que deseja deletar todas as tarefas salvas?\n...")
        sleep(3)
        delete2 = str(input("->"))
        if delete2.upper() == "S":
            with open("TaskTracker.json", "w") as arquivo:
                json.dump({"tarefas":[]}, arquivo)

#-------------------

adicionar()
listar()

