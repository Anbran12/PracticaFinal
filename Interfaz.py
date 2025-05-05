import Metodos as Mt

obj = Mt.Metodos_Estudiantes()
obj.registrar_estudiantes()
obj.mostrar_estudiantes()

#while True:
#    try:
#        print("Menú:",
#        	"\n1. ",
#	        "\n2. ",
#	        "\n3. ", 
#	        "\n4. ")
#        
#        opcion = int(input("\nIngrese el punto a ejecutar (1 - 10): "))
#        if opcion in [1,2,3,4]:   
#            if opcion == 1:
#                #PUNTO 1
#                punto1 = p1.Punto1()
#                print(punto1.Epunto1())
#
#            if opcion == 2:
#                #PUNTO 2
#                punto2 = p2.Punto2()
#                print(punto2.Epunto2())
#
#            if opcion == 3:
#                #PUNTO 3
#                punto3 = p3.Punto3()
#                print(punto3.Epunto3())
#
#            if opcion == 4:
#                #PUNTO 4
#                punto4 = p4.Punto4()
#                print(punto4.Epunto4())
#        
#        elif opcion in [5,6,7,8,9,10]:
#            print("\nEn mantenimiento")
#
#        else:
#            print("\nOpción no valida")
#    except ValueError:
#        print("\nIngresa un valor tipo numerico.")