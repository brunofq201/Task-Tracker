"""
Um programa que rode em CLI onde o usuário pode cadastrar e gerenciar tarefas.

 - Adicionar tarefa
 - Listar tarefas
 - Concluir tarefa
 - Remover tarefa
 - Sair
"""

import json
from time import sleep
from datetime import datetime

def iniciar_arquivo(nome):
    try:
        with open(f"{nome}.json", "r") as arquivo:
            json.load(arquivo)
    except FileNotFoundError:
        with open(f"{nome}.json", "x") as arquivo:
            json.dump({"tarefas":[]}, arquivo, indent=4)
    except json.JSONDecodeError:
        with open(f"{nome}.json", "w") as arquivo:
            json.dump({"tarefas":[]}, arquivo, indent=4)

def atribuir_id():
    ids = []
    with open("TaskTracker.json", "r") as arquivo:
        tasks = json.load(arquivo)
        for tarefa in tasks["tarefas"]:
            ids.append(tarefa["ID"])
    with open("Concluidas.json", "r") as arquivo:
        tasks = json.load(arquivo)
        for tarefa in tasks["tarefas"]:
            ids.append(tarefa["ID"])
    with open("Lixeira.json", "r") as arquivo:
        tasks = json.load(arquivo)
        for tarefa in tasks["tarefas"]:
            ids.append(tarefa["ID"])
    if len(ids) > 0:
        id_tarefa = max(ids)+1
        return(id_tarefa)
    else:
        return 1

#---------------------------------------------------------

def listar_tarefas(nome):
    with open(f"{nome}.json", "r") as arquivo:
        lista = json.load(arquivo)
        print(f"\n{json.dumps(lista, indent=4)}")
        if len(lista["tarefas"]) == 0:
            print("\nNenhuma tarefa ainda\n")

def adicionar_tarefa(id_tarefa, nome, descricao):
    with open("TaskTracker.json", "r") as arquivo:
        add = json.load(arquivo)
        with open("TaskTracker.json", "w") as arquivo:
            add["tarefas"].append({"ID":id_tarefa,
                                "nome":nome,
                                "descricao":descricao,
                                "criada_em":datetime.now().strftime("%d/%m/%Y %H:%M")})
                                #"editado_em":datetime.now().strftime("%d/%m/%Y %H:%M")})
            json.dump(add, arquivo, indent=4)
        print("\nTarefa criada com sucesso\n")

def editar_tarefa():
    listar_tarefas("TaskTracker")
    id_tarefa = int(input("\nDigite a ID da tarefa que deseja editar\n-> "))
    with open("TaskTracker.json", "r") as arquivo:
        tasks = json.load(arquivo)
        achei = False
        for tarefa in tasks["tarefas"]:
            if tarefa["ID"] == id_tarefa:
                achei = True
                break
        if achei:
            confirm = str(input(f"\nVc tem ctz q deseja editar a tarefa n {id_tarefa}? (S/n)\n-> "))
            if confirm.upper() == "S": 
                novo_nome = str(input(f"Digite o novo nome\n - Anterior: {tarefa['nome']}\n-> "))
                nova_desc = str(input(f"Digite a nova descrição\n - Anterior: {tarefa['descricao']}\n-> "))
                if novo_nome != "":
                    tarefa["nome"] = novo_nome
                if nova_desc != "":
                    tarefa["descricao"] = nova_desc
                if novo_nome != "" or nova_desc != "":
                    tarefa["editado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                with open("TaskTracker.json", "w") as arquivo:
                    json.dump(tasks, arquivo, indent=4)
                print("\nTarefa alterada com sucesso.\n")
        else:
            print(f"\nNão foi possivel encontrar a tarefa de ID {id_tarefa}\n")
                
def remover_tarefa(id_tarefa):
    with open("TaskTracker.json", "r") as arquivo:
        tasks = json.load(arquivo)
        achei = False
        for tarefa in tasks["tarefas"]:
            if tarefa["ID"] == id_tarefa:
                achei = True
                break
        if achei:
            confirm = str(input(f"\nVc tem ctz q deseja remover a tarefa n {id_tarefa}? (S/n)\n-> "))
            if confirm.upper() == "S":
                with open("Lixeira.json", "r") as lixeira:
                    lixo = json.load(lixeira)
                    lixo["tarefas"].append(tarefa)
                    with open("Lixeira.json", "w") as lixeira:
                        json.dump(lixo, lixeira, indent=4)
                tasks["tarefas"].remove(tarefa)
                with open("TaskTracker.json", "w") as arquivo:
                    json.dump(tasks, arquivo, indent=4)
                print("\nTarefa removida com sucesso.\n")
        else:
            print(f"\nNão foi possivel encontrar a tarefa de ID {id_tarefa}\n")

def restaurar_tarefa(nome, id_tarefa):
    with open(f"{nome}.json", "r") as lixeira:
        lixo = json.load(lixeira)
        achei = False
        for tarefa in lixo["tarefas"]:
            if tarefa["ID"] == id_tarefa:
                achei = True
                break
        if achei:
            confirm = str(input(f"\nVc tem ctz q deseja restaurar a tarefa n {id_tarefa}? (S/n)\n-> "))
            if confirm.upper() == "S":
                lixo["tarefas"].remove(tarefa)
                with open("TaskTracker.json", "r") as arquivo:
                    tasks = json.load(arquivo)
                    tasks["tarefas"].append(tarefa)
                    tarefa["restaurado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                with open("TaskTracker.json", "w") as arquivo:
                    json.dump(tasks, arquivo, indent=4)
                with open(f"{nome}.json", "w") as lixeira:
                    json.dump(lixo, lixeira, indent=4)
                print("\nTarefa restaurada com sucesso.\n")
        else:
            print(f"\nNão foi possivel encontrar a tarefa de ID {id_tarefa}\n")

def concluir_tarefa():
    listar_tarefas("TaskTracker")
    id_tarefa = int(input("\nDigite a ID da tarefa que deseja concluir\n-> "))
    with open("TaskTracker.json", "r") as arquivo:
            tasks = json.load(arquivo)
            achei = False
            for tarefa in tasks["tarefas"]:
                if tarefa["ID"] == id_tarefa:
                    achei = True
                    break
            if achei:
                confirm = str(input(f"\nVc tem ctz q deseja concluir a tarefa n {id_tarefa}? (S/n)\n-> "))
                if confirm.upper() == "S":
                    with open("Concluidas.json", "r") as concluidas:
                        feitas = json.load(concluidas)
                        tarefa["concluida_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                        feitas["tarefas"].append(tarefa)
                        with open("Concluidas.json", "w") as concluidas:
                            json.dump(feitas, concluidas, indent=4)
                    tasks["tarefas"].remove(tarefa)
                    with open("TaskTracker.json", "w") as arquivo:
                        json.dump(tasks, arquivo, indent=4)
                    print("\nTarefa concluida com sucesso.\n")
            else:
                print(f"\nNão foi possivel encontrar a tarefa de ID {id_tarefa}\n")

def deletar_tarefas(nome):
    with open(f"{nome}.json", "r") as arquivo:
        tasks = json.load(arquivo)
        if len(tasks["tarefas"])>0:
            delete = str(input("\nDeseja deletar? (S/n)\n-> "))
            if delete.upper() == "S":
                print("\nVc tem certeza que deseja deletar todas as tarefas salvas?\n...")
                sleep(3)
                delete2 = str(input("-> "))
                if delete2.upper() == "S":
                    with open(f"{nome}.json", "w") as arquivo:
                        json.dump({"tarefas":[]}, arquivo, indent=4)
                    print("\nTodas as tarefas deletadas com sucesso.\n")
        else:
            listar_tarefas(nome)
            print("\nNão existem tarefas para serem deletadas\n")

def ajuda():
    print("\nhelp [ajuda com comandos]\n" \
    "ls [listar as tarefas]\n"
    " > ls -ccd [listar as tarefas concluidas]\n"
    " > ls -trsh [listar a lixeira]\n" \
    "add [adicionar tarefa]\n" \
    "edt [editar uma tarefa]\n" \
    "rm [remover uma tarefa]\n" \
    "sv [restaurar uma tarefa removida]\n"
    " > sv -ccd [Restaurar uma tareda concluida]\n" \
    "ccd [concluir uma tarefa]\n" \
    "del [deletar tarefas]\n"
    " > del -ccd [deletar tarefas concluidas]\n"
    " > del -trsh [limpar a lixeira]\n" \
    "exit [fechar programa]\n")

#---------------------------------------------------------

iniciar_arquivo("TaskTracker")
iniciar_arquivo("Concluidas")
iniciar_arquivo("Lixeira")

while True:
    escolha = input("\nSelecione o que fazer (digite 'help' para ajuda)\n-> ")
    if escolha == "help":
        ajuda()
    elif escolha == "ls":
        listar_tarefas("TaskTracker")
    elif escolha == "ls -ccd":
        listar_tarefas("Concluidas")
    elif escolha == "ls -trsh":
        listar_tarefas("Lixeira")
    elif escolha == "add":
        nome = str(input("\nDigite o nome da tarefa\n-> "))
        descricao = str(input("\nDigite a descrição da tarefa\n-> "))
        adicionar_tarefa(atribuir_id(), nome, descricao)
    elif escolha == "edt":
        editar_tarefa()
    elif escolha == "rm":
        listar_tarefas("TaskTracker")
        id_tarefa = int(input("Digite a ID da tarefa que deseja remover\n-> "))
        remover_tarefa(id_tarefa)
    elif escolha == "sv":
        listar_tarefas("Lixeira")
        id_tarefa = int(input("Digite a ID da tarefa que deseja restaurar\n-> "))
        restaurar_tarefa("Lixeira",id_tarefa)
    elif escolha == "sv -ccd":
        listar_tarefas("Concluidas")
        id_tarefa = int(input("Digite a ID da tarefa que deseja restaurar\n-> "))
        restaurar_tarefa("Concluidas", id_tarefa)
    elif escolha == "ccd":
        concluir_tarefa()
    elif escolha == "del":
        deletar_tarefas("TaskTracker")
    elif escolha == "del -ccd":
        deletar_tarefas("Concluidas")
    elif escolha == "del -trsh":
        deletar_tarefas("Lixeira")
    elif escolha == "exit":
        break
    else:
        print("\nComando nao identificado, digite 'help' para ajuda\n")
        continue

    # fazer um cache pras concluidas !!!