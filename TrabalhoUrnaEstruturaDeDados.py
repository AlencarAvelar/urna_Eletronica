eleitores_aptos = 0
total_votos_nominais = 0
total_votos_brancos = 0
total_votos_nulos = 0

def localizar_arquivo():
    filename = input("Informe a localização dos dados que deseja: ")

    try:
        linhas = []

        arq = open(filename, "r")

        for linha in arq:
            linhas.append(linha.strip())

        arq.close()

        return linhas

    except:
        print("Erro ao processar o arquivo!")
        print("\n")
        return None

def gerar_lista_candidatos(listaCandidatos):
    info_candidatos = list()

    for candidato in listaCandidatos:

        linha = []

        dados = candidato.split(",")

        for x in range(len(dados)):
            linha.append(dados[x].strip())

        info_candidatos.append(linha)

    return info_candidatos

def gerar_lista_eleitores(listaEleitores):
    info_eleitores = list()

    for eleitor in listaEleitores:

        linha = []

        dados = eleitor.split(",")

        for x in range(len(dados)):
            linha.append(dados[x].strip())

        info_eleitores.append(linha)

    return info_eleitores

def votacaoCandidato(listaCandidatos, cargo, sigla, estadoUrna):
    global total_votos_nominais, total_votos_brancos, total_votos_nulos
    while True:
        voto = input("Informe o voto para %s: " % (cargo))
        confirmacao = None

        if voto == 'B':
            print("Voto em Branco")
            confirmacao = input("Confirma (S ou N)? ")

            if confirmacao == 'S':
                total_votos_brancos += 1
                voto = 'B'
                print("\n")
                break
            elif confirmacao == 'N':
                None
                print("\n")
            else:
                None
                print("\n")
        else:
            for x in range(len(listaCandidatos)):
                if voto == listaCandidatos[x][1] and listaCandidatos[x][4] == sigla and (
                        estadoUrna == listaCandidatos[x][3] or sigla == 'P'):
                    print("Candidato %s | %s" % (listaCandidatos[x][0], listaCandidatos[x][2]))

                    confirmacao = input("Confirma (S ou N)? ")

                    if confirmacao == 'S':
                        total_votos_nominais += 1
                        print("\n")
                        break
                    elif confirmacao == 'N':
                        print("\n")
                        break
                    else:
                        print("\n")
                        break

            if confirmacao is None:
                print("Candidato não encontrado! Voto Nulo.")
                total_votos_nulos += 1
                confirmacao = input("Confirma (S ou N)? ")

                if confirmacao == 'S':
                    voto = 'N'
                    print("\n")
                    break
                elif confirmacao == 'N':
                    print("\n")
                    None
                else:
                    print("Opção inválida, tente novamente.")
                    print("\n")

        if confirmacao == 'S':
            break

    print("\n")

    return voto

#Funcao que cuida completamente de toda a votacao e a grava no arquivo
def votacao(listaEleitores, listaCandidatos):
    global eleitores_aptos
    #Checa o estado da urna e o titulo de eleitor para ver se sao validos
    estadosValidos = ["AC", "AL", "AP", "AM", "BA", "CE", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO", "DF"]
    estadoUrna = None
    while estadoUrna not in estadosValidos:
        estadoUrna = input("UF onde está localizada a urna: ")

    #Checa se o titulo de eleitor e valido e do estado da urna
    while True:
        tituloEleitor = str(input("Informe o Título de Eleitor: "))
        titulo_encontrado = False

        for i in range(len(listaEleitores)):
            if tituloEleitor == listaEleitores[i][2] and estadoUrna == listaEleitores[i][4]:
                print("Eleitor: %s" %(listaEleitores[i][0]))
                print("Estado: %s" %(listaEleitores[i][4]))
                titulo_encontrado = True
                break
                
        if titulo_encontrado == False:   
            print("Título não encontrado!")
        else:
            break

    print("\n")


    #Realiza a votacao de cada candidato
    votoDeputadoFederal = votacaoCandidato(listaCandidatos, "Deputado Federal", 'F',estadoUrna)
    votoDeputadoEstadual = votacaoCandidato(listaCandidatos, "Deputado Estadual", 'E',estadoUrna)
    votoSenador = votacaoCandidato(listaCandidatos, "Senador", 'S',estadoUrna)
    votoGovernador = votacaoCandidato(listaCandidatos, "Governador", 'G',estadoUrna)
    votoPresidente = votacaoCandidato(listaCandidatos, "Presidente", 'P',estadoUrna)

    print("Voto registrado com sucesso!")
    print("\n")
        
    #Salva no arquivo os votos
    arq = open("votos.txt", "a")

    arq.write('{"UF": "%s", "F": %s, "E": %s, "S": %s, "G": %s, "P": %s}' %(estadoUrna, votoDeputadoFederal, votoDeputadoEstadual, votoSenador, votoGovernador, votoPresidente))
    arq.write("\n")

    arq.close

    while True:
        novoVoto = input("Registrar novo voto (S ou N)? ")

        if novoVoto == 'S':
            print("\n")
            votacao(listaEleitores, listaCandidatos)
        elif novoVoto == 'N':
            print("\n")
            break
        else:
            print("Resposta inválida, tente novamente")
            print("\n")
            None

        if novoVoto == 'N':
            break



#Realiza a apuracao dos votos
def apuracao_votos(listaCandidatos):
    # Inicializa a contagem de votos para cada candidato
    for x in range(len(listaCandidatos)):
        listaCandidatos[x].append(0)

    # Abre o arquivo de votos e lê cada linha
    with open("votos.txt", "r") as arq:
        listaVotos = [linha.strip() for linha in arq]

    # Conta os votos para cada candidato
    for voto in listaVotos:
        voto = voto.replace("{", "").replace("}", "").replace('"', "").split(", ")
        voto_dict = {item.split(": ")[0]: item.split(": ")[1] for item in voto}
        for candidato in listaCandidatos:
            if voto_dict[candidato[4]] == candidato[1]:
                candidato[-1] += 1

    # Calcula a porcentagem de votos para cada candidato
    total_votos = len(listaVotos)
    for candidato in listaCandidatos:
        porcentagem = (candidato[-1] / total_votos) * 100
        print(f"Candidato {candidato[0]} recebeu {candidato[-1]} votos, que representam {porcentagem:.2f}% do total.")



    arq.close()

    #Conta os votos para cada candidato e coloca como valor no final da listaCandidatos
    for x in range(len(listaVotos)):
        for y in range(len(listaCandidatos)):
                for z in range(11):
                    if listaVotos[x][z] == listaCandidatos[y][4]: #Valor na linha de votos for igual letrea do cargo de candidato
                        if (listaVotos[x][1] == listaCandidatos[y][3]  or listaCandidatos[y][4] == 'P') and listaVotos[x][z+1] == listaCandidatos[y][1]:#Mesmo estado ou presidente e numero do voto igual numero do candidato
                            listaCandidatos[y][-1] += 1
    

    print()

def gerar_boletim_urna(listaCandidatos, listaEleitores):
    global eleitores_aptos, total_votos_nominais, total_votos_brancos, total_votos_nulos
    total_eleitores = len(listaEleitores)
    total_votos_nominais = 0
    total_votos_brancos = 0
    total_votos_nulos = 0

        
    
    
    
    
    # Conta os votos para cada candidato
    for candidato in listaCandidatos:
        if isinstance(candidato[-1], int):
            total_votos_nominais += candidato[-1]
        elif candidato[-1] == 'B':
            total_votos_brancos += 1
        elif candidato[-1] == 'N':
            total_votos_nulos += 1

    # Gera o boletim de urna
    with open("boletim_urna.txt", "w") as bu:
        bu.write(f"Apuração dos votos:\n")
        bu.write(f"Eleitores Aptos: {total_eleitores}\n")
        bu.write(f"Total de Votos Nominais: {total_votos_nominais}\n")
        bu.write(f"Brancos: {total_votos_brancos}\n")
        bu.write(f"Nulos: {total_votos_nulos}\n\n")

        

        for candidato in listaCandidatos:
            porcentagem = (candidato[-1] / total_votos_nominais) * 100 if isinstance(candidato[-1], int) else 0
            resultado = f"Candidato: {candidato[0]} | Cargo: {candidato[4]} | Estado: {candidato[3]} | Votos: {candidato[-1]} ({porcentagem:.2f}%)\n"
            bu.write(resultado)
            print(resultado)  # Imprime o resultado na tela

    print("Boletim de Urna gerado com sucesso!")

def menu():
   global eleitores_aptos, total_votos_nominais, total_votos_brancos, total_votos_nulos
   candidatosBruto = None
   eleitoresBruto = None
   while True:
       print("Menu:")
       print("1 - Ler arquivo de candidatos")
       print("2 - Ler arquivo de eleitores")
       print("3 - Iniciar votação")
       print("4 - Apurar votos")
       print("5 - Mostrar resultados")
       print("6 - Fechar programa")
       opcao = str(input("Selecione a opção que deseja: "))

       if opcao == "1":
           candidatosBruto = localizar_arquivo()
           if candidatosBruto != None:
                listaCandidatos = gerar_lista_candidatos(candidatosBruto)
                print("Candidatos carregados com sucesso!")
                print("\n")
       elif opcao == "2":
           eleitoresBruto = localizar_arquivo()
           if eleitoresBruto != None:
                listaEleitores = gerar_lista_eleitores(eleitoresBruto)
                print("Eleitores carregados com sucesso!")
                print("\n")
       elif opcao == "3":
           if candidatosBruto is None or eleitoresBruto is None:
               print("Por favor, leia os arquivos de candidatos e eleitores primeiro.")
               print("\n")
           else:
               print("Iniciar votação")
               print("\n")
               votacao(listaEleitores, listaCandidatos)
       elif opcao == "4":
           if candidatosBruto is None or eleitoresBruto is None:
               print("Por favor, leia os arquivos de candidatos e eleitores primeiro.")
               print("\n")
           else:
               print("Apurar votos")
               print("\n")
               apuracao_votos(listaCandidatos)
       elif opcao == "5":
            if candidatosBruto is None or eleitoresBruto is None:
                print("Por favor, leia os arquivos de candidatos e eleitores primeiro.")
                print("\n")
            else:
                print("Mostrar resultados")
                print("\n")
                gerar_boletim_urna(listaCandidatos, listaEleitores)
       elif opcao == "6":
           print("Fechando programa")
           print("\n")
           #FALTA LIMPAR O ARQUIVO
           break
       else:
           print("Opção inválida. Tente novamente.")
           print("\n")




menu()

