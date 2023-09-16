def print_regras(base_conhecimento):
    for i, regra in enumerate(base_conhecimento):
        print(f"Regra {i + 1}: SE", end=" ")
        for condicao in regra["condicao"]:
            print(f"{condicao[0]} = {condicao[1]}", end=" ")
            if condicao != regra["condicao"][-1]:
                print("E", end=" ")
        print(f"ENTÃO {regra['valor'][0]} = {regra['valor'][1]}")

def encad_tras(objetivo, fatos, base_conhecimento):
    n = 0
    for f in fatos:
        for i in base_conhecimento:
            if i["valor"][1] == f[1] and i["valor"][0] == f[0]:
                for j in i["condicao"]:
                    if j not in fatos:
                        valido = 1
                        for z in fatos:
                            if j[0] == z[0]:
                                valido = 0
                        if (valido):
                            fatos.append(j)
                            n += 1
 
    return n, fatos

def encad_frente(classificatorio, base_conhecimento, atributos, valores):
    fatos = list()
    apli_regras = list()
    temp_atributos = atributos.copy()
    temp_valores = valores.copy()
    temp_base_conhecimento = base_conhecimento.copy()
    flag = 0
    while temp_atributos:
        i = temp_atributos[0]
        
        if i == classificatorio:
            temp_atributos.pop(0)
            temp_valores.pop(0) #!!!!!!
            continue

        valores_possiveis = temp_valores[0]

        if len(valores_possiveis) == 1:
            resposta = input(f"\nO tipo do/a {i} é {valores_possiveis[0]}? [S/N] ").upper()
            if resposta == "S":
                fatos.append([i, valores_possiveis[0]])
            elif resposta != "N":
                print("Digite uma resposta válida!")

        else:
            print(f"Qual o tipo do/a {i}? ")
            for f, j in enumerate(valores_possiveis):
                print(f"[ {f} ] - {j}")
            print("[ -1 ] - Não sei")
            resposta = int(input("Resposta: "))
            if resposta != -1:
                fatos.append([i, valores_possiveis[resposta]])

        temp_atributos.pop(0)
        temp_valores.pop(0)

        for k, i in enumerate(temp_base_conhecimento):
            aux = 0
            tam = len(i["condicao"])
            for j in fatos:
                if j[0] == i["valor"][0] and j[1] != i["valor"][1]:
                    # print(f"Excluir regra valor {i['valor'][0]} = {i['valor'][1]}")
                    # print(i)
                    temp_base_conhecimento.pop(k)
                    break
                       
                    
                for x in i["condicao"]:
                    if j[0] == x[0] and j[1] == x[1]:
                        tam -= 1
                    elif j[0] == x[0] and j[1] != x[1]:
                        # print(f"exclui regra condição {x[0]} = {x[1]}")
                        # print(i)
                        temp_base_conhecimento.pop(k)
                        if j[0] in temp_atributos:
                            ind = temp_atributos.index(j[0])
                            temp_atributos.pop(ind)
                            temp_valores.pop(ind)
                        aux = 1
                        break
                if aux == 1:
                    break
    
            if tam == 0:
                if i not in apli_regras:
                    apli_regras.append(i)
                if i["valor"][0] == classificatorio:
                    resposta = input(f"\nA partir dos fatos fornecidos {classificatorio} é o/a {i['valor'][1]}? [S/N] ").upper()
                    if resposta == "S":
                        flag = 1
                        # print(f"\nA partir dos fatos fornecidos {classificatorio} = {classe}")
                        print("\nÓtimo adivinhei!!!")
                        print("\nAs regras aplicadas foram: ")
                        print_regras(apli_regras)
                        break
                    elif resposta == "N":
                        print(f"\nA partir dos fatos fornecidos não foi possível definir o {classificatorio}")
                        flag=1
                        break
                    else:
                        print("Digite uma resposta válida!")
                        continue
    
                elif i["valor"] not in fatos:
                    fatos.append(i["valor"])
                    ind = temp_atributos.index(i['valor'][0])
                    temp_atributos.pop(ind)
                    temp_valores.pop(ind)
        if flag == 1:
            break

def encad_frente_2(fatos, apli_regras, classificatorio, base_conhecimento):
    classe = None  # Inicialize a variável classe
    for k, i in enumerate(base_conhecimento): #Analisando regra por regra
        tam = len(i["condicao"])
        for j in fatos:
            for x in i["condicao"]:
                if j[0] == x[0] and j[1] == x[1]:
                    tam -= 1
 
        if tam == 0:
            apli_regras.append(k + 1)
            if i["valor"][0] == classificatorio:
                classe = i["valor"][1]  # Atualize a classe se a regra corresponder ao atributo
 
            elif i["valor"] not in fatos:
                fatos.append(i["valor"])
    if classe == None:
        print(f"\nA partir dos fatos fornecidos não foi possivel definir o {classificatorio}")
    else:
        print(f"\nA partir dos fatos fornecidos {classificatorio} = {classe}")
    print("\nAs regras aplicadas foram: ")
    for i in apli_regras:
        print(f"Regra {i}")


base_conhecimento = []

qt_regras = int(input("Quantas regras serão digitadas? "))

atributos = []
valores = []

for i in range(qt_regras):
    regra = input(f"Regra {i + 1}: ").replace("=", "").replace(",", "").replace(".", "").split()

    dic_regra = {
        "condicao": [],
        "valor": []
    }

    for j in range(len(regra)):
        if regra[j] == "SE" or regra[j] == "E":
            atributo, valor = regra[j + 1], regra[j + 2]
            dic_regra["condicao"].append([atributo, valor])

            if atributo in atributos:
                k = atributos.index(atributo)
                if valor not in valores[k]:
                    valores[k].append(valor)
            else:
                atributos.append(atributo)
                valores.append([valor])
    if "ENTÃO" in regra:
        atributo, valor = regra[regra.index("ENTÃO") + 1], regra[regra.index("ENTÃO") + 2]
        dic_regra["valor"] = [atributo, valor]
        if atributo in atributos:
            k = atributos.index(atributo)
            if valor not in valores[k]:
                valores[k].append(valor)
        else:
            atributos.append(atributo)
            valores.append([valor])

    base_conhecimento.append(dic_regra)
classificatorio = input("Qual o Atributo classificatório? ")

print("\nRegras na Base de Conhecimento:")
print_regras(base_conhecimento)
# print("\nAtributos encontrados:")
# print(atributos)
# print("\nValores possíveis para cada atributo:")
# for i, atributo in enumerate(atributos):
#     print(f"{atributo}: {valores[i]}")

while True:
    x = int(input("\n[ 1 ]  Encadeamento para Frente\n[ 2 ]  Encadeamento para Trás\n[ 0 ]  Sair\n"))
    if x == 0:
        break
    elif x == 1:
        print("ENCADEAMENTO PARA FRENTE: \n")
        encad_frente(classificatorio, base_conhecimento, atributos, valores)
 
    elif x == 2:
        print("ENCADEAMENTO PARA TRÁS: \n")
        objetivo = input(f"Qual o seu objetivo para classe {classificatorio}? ")
        fatos = list()
        fato_objetivo = list()
        fato_objetivo.append(classificatorio)
        fato_objetivo.append(objetivo)
        fatos.append(fato_objetivo)
        n = 0
        n, fatos = encad_tras(objetivo, fatos, base_conhecimento)
        while n != 0:
            for i in fatos:
                n, fatos = encad_tras(i, fatos, base_conhecimento)
        print(f"\nPara {classificatorio} = {objetivo} serão necessários os Fatos: ")
        for fato in fatos:
            print(f"{fato[0]} = {fato[1]}")
