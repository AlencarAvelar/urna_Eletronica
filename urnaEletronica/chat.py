def localizar_arquivo():
   filename = input("Informe a localização dos dados que deseja: ")
   with open(filename, "r") as arq: 
       return arq.read()

def menu():
   candidatos = None
   eleitores = None
   while True:
       print("Menu:")
       print("1 - Ler arquivo de candidatos")
       print("2 - Ler arquivo de eleitores")
       print("3 - Iniciar votação")
       print("4 - Apurar votos")
       print("5 - Mostrar resultados")
       print("6 - Fechar programa")
       opcao = int(input("Selecione a opção que deseja: "))

       if opcao == 1:
           candidatos = localizar_arquivo()
           print(candidatos)
       elif opcao == 2:
           eleitores = localizar_arquivo()
           print(eleitores)
       elif opcao == 3:
           if candidatos is None or eleitores is None:
               print("Por favor, leia os arquivos de candidatos e eleitores primeiro.")
           else:
               print("Iniciar votação")
               #  Colocar codigo
       elif opcao == 4:
           if candidatos is None or eleitores is None:
               print("Por favor, leia os arquivos de candidatos e eleitores primeiro.")
           else:
               print("Apurar votos")
               # Colocar codigo
       elif opcao == 5:
           if candidatos is None or eleitores is None:
               print("Por favor, leia os arquivos de candidatos e eleitores primeiro.")
           else:
               print("Mostrar resultados")
               # Colocar codigo
       elif opcao == 6:
           print("Fechando programa")
           break
       else:
           print("Opção inválida. Tente novamente.")

menu()