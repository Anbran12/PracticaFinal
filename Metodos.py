import csv
import customtkinter as CTK

class ESTUDIANTES:
    def __init__(self, cedula, nombre, apellido, telefono):
        self.cedula = cedula 
        self.nombre = nombre 
        self.apellido = apellido 
        self.telefono = telefono

class ESTUDIANTE_INGENIERIA(ESTUDIANTES):
    def __init__(self, cedula, nombre, apellido, telefono, semestre, promedio, serial=""):
        super().__init__(cedula, nombre, apellido, telefono)
        self.semestre = semestre 
        self.promedio = promedio 
        self.serial = serial

    def convertir_lista(self):
        return [self.cedula,self.nombre,self.apellido,self.telefono,self.semestre,self.promedio,self.serial]
        
class ESTUDIANTE_DISENO(ESTUDIANTES):
    def __init__(self, cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, serial=""):
        super().__init__(cedula, nombre, apellido, telefono)
        self.modalidad = modalidad 
        self.cantidad_asignaturas = cantidad_asignaturas 
        self.serial = serial

    def convertir_lista(self):
        return [self.cedula,self.nombre,self.apellido,self.telefono,self.modalidad,self.cantidad_asignaturas,self.serial]

class DISPOSITIVOS:
    def __init__(self, serial, marca, tamano, precio):
        self.serial = serial 
        self.marca = marca 
        self.tamano = tamano 
        self.precio = precio 
    
class TABLETA_GRAFICA(DISPOSITIVOS):
    def __init__(self, serial, marca, tamano, precio, almacenamiento, peso):
        super().__init__(serial, marca, tamano, precio)
        self.almacenamiento = almacenamiento 
        self.peso = peso

    def convertir_lista(self):
        return [self.serial,self.marca,self.tamano,self.precio,self.almacenamiento,self.peso]
        
class COMPUTADOR_PORTATIL(DISPOSITIVOS):
    def __init__(self, serial, marca, tamano, precio, sistema_operativo, procesador):
        super().__init__(serial, marca, tamano, precio)
        self.sistema_operativo = sistema_operativo 
        self.procesador = procesador

    def convertir_lista(self):
        return [self.serial,self.marca,self.tamano,self.precio,self.sistema_operativo,self.procesador]

class PANTALLA_PRINCIPAL:
    def __init__(self):
        self.pagina_inicial = CTK.CTk()
        self.pagina_inicial.geometry("+300+100")
        self.pantalla_login()
    
    def pantalla_login(self):
        def login_validacion():
            cedula_busqueda = self.entrada_busqueda.get()
            try:
                cedula_busqueda = int(cedula_busqueda)
            except ValueError:
                self.etiqueta_busqueda_error.configure(text="Valor ingresado no valido")
                self.etiqueta_busqueda_error.pack()
                return
            if cedula_busqueda == 1234:
                self.pagina_inicial.title("EQUIPOS ELECTRÓNICOS SAN JUAN DE DIOS")
                self.frame_pantalla_busqueda.destroy()
                self.menu_administrador()
            else:
                self.etiqueta_busqueda_error.configure(text="Usuario no existe")
                self.etiqueta_busqueda_error.pack()

        self.frame_pantalla_busqueda = CTK.CTkFrame(self.pagina_inicial)
        self.frame_pantalla_busqueda.pack()
        
        self.pagina_inicial.title("Login")
        self.etiqueta_busqueda = CTK.CTkLabel(self.frame_pantalla_busqueda, text="Ingresa tu documento de identidad")
        self.etiqueta_busqueda.pack(pady=10, padx=10)

        self.entrada_busqueda = CTK.CTkEntry(self.frame_pantalla_busqueda)
        self.entrada_busqueda.pack()

        self.etiqueta_busqueda_error = CTK.CTkLabel(self.frame_pantalla_busqueda, text="")

        self.boton_busqueda = CTK.CTkButton(self.frame_pantalla_busqueda, text="Buscar", command=login_validacion)
        self.boton_busqueda.pack(pady=10, padx=10)
        
    def menu_estudiantes(self):
        objeto_prestamo_equipos = Metodos_Prestamos()
        
    def menu_administrador(self):
        objeto_registro_estudiantes = Metodos_Estudiantes()
        objeto_registro_estudiantes.registrar_estudiantes_validacion_carrera()
        objeto_registro_equipos = Metodos_Equipos()
        objeto_prestamo_equipos = Metodos_Prestamos()
   
class Metodos_Estudiantes:
    def registrar_estudiantes_validacion_carrera(self):
        self.ventana_registro_estudiantes = CTK.CTkToplevel()
        self.ventana_registro_estudiantes.geometry("+300+100")
        self.ventana_registro_estudiantes.focus()
        self.ventana_registro_estudiantes.grab_set()
        self.frame_validacion_carrera = CTK.CTkFrame(self.ventana_registro_estudiantes)
        self.frame_validacion_carrera.pack()
        self.etiqueta_carrera = CTK.CTkLabel(self.frame_validacion_carrera, text="¿Qué carrera esta estudiando?")
        self.etiqueta_carrera.grid()
        self.desplegable_carrera = CTK.CTkComboBox(self.frame_validacion_carrera, values=["Ingeniería","Diseño"], state="readonly")
        self.desplegable_carrera.set("Ingeniería")
        self.desplegable_carrera.grid()
        self.boton_carrera = CTK.CTkButton(self.frame_validacion_carrera, text="Continuar", command=self.registro_segun_eleccion_carrera)
        self.boton_carrera.grid()

    def registro_segun_eleccion_carrera(self):
        eleccion_carrera = self.desplegable_carrera.get()
        if eleccion_carrera == "Ingeniería":  
            var_cedula = input("Ingresa el/la cedula: ") 
            var_nombre = input("Ingresa el/la nombre: ") 
            var_apellido = input("Ingresa el/la apellido: ") 
            var_telefono = input("Ingresa el/la telefono: ") 
            var_semestre = int(input("Ingresa el/la semestre: ")) 
            var_promedio = float(input("Ingresa el/la promedio: "))
                        
            with open("PracticaFinal/Estudiantes_Ingenieria.csv", "a+", newline="", encoding='utf-8') as Est_Ing_CSV:
                Est_Ing_CSV.seek(0)
                Lector_Ing = csv.reader(Est_Ing_CSV)
                Escritor_Ing = csv.writer(Est_Ing_CSV)
                
                for c in Lector_Ing:
                    registro_actual = c[0]
                    if registro_actual == var_cedula:
                        print("La persona ingresada ya se encuentra registrada.")
                        break
                    else:
                        registro = ESTUDIANTE_INGENIERIA(var_cedula,var_nombre,var_apellido,var_telefono,var_semestre,var_promedio)
                        Escritor_Ing.writerow(registro.convertir_lista())
                        print("Registro exitoso.")
                        break
                
                if next(Lector_Ing, None) is None:
                    registro = ESTUDIANTE_INGENIERIA(var_cedula,var_nombre,var_apellido,var_telefono,var_semestre,var_promedio)
                    Escritor_Ing.writerow(registro.convertir_lista())
                    print("Registro exitoso.")
            
            Est_Ing_CSV.close()
                    
        elif eleccion_carrera == "Diseño":
            var_cedula = input("Ingresa el/la cedula: ") 
            var_nombre = input("Ingresa el/la nombre: ") 
            var_apellido = input("Ingresa el/la apellido: ") 
            var_telefono = input("Ingresa el/la telefono: ") 
            var_modalidad = input("Ingresa el/la modalidad: ") 
            var_cantidad_asignaturas = int(input("Ingresa el/la cantidad de asignaturas: "))
                        
            with open("PracticaFinal/Estudiantes_Diseno.csv", "a+", newline="", encoding='utf-8') as Est_Dis_CSV:
                Est_Dis_CSV.seek(0)
                Lector_Dis = csv.reader(Est_Dis_CSV)
                Escritor_Dis = csv.writer(Est_Dis_CSV)
                
                for c in Lector_Dis:
                    registro_actual = c[0]
                    if registro_actual == var_cedula:
                        print("La persona ingresada ya se encuentra registrada.")
                        break
                    else:
                        registro = ESTUDIANTE_DISENO(var_cedula,var_nombre,var_apellido,var_telefono,var_modalidad,var_cantidad_asignaturas)
                        Escritor_Dis.writerow(registro.convertir_lista())
                        print("Registro exitoso.")
                        break
                    
                if next(Lector_Dis, None) is None:
                    registro = ESTUDIANTE_DISENO(var_cedula,var_nombre,var_apellido,var_telefono,var_modalidad,var_cantidad_asignaturas)
                    Escritor_Dis.writerow(registro.convertir_lista())
                    print("Registro exitoso.")

            Est_Dis_CSV.close()
        
    def modificar_estudiantes(self):
        with open("PracticaFinal/Estudiantes_Ingenieria.csv", "a+", newline="", encoding='utf-8') as Est_Ing_CSV:
            Est_Ing_CSV.seek(0)
            lector_ing = csv.reader(Est_Ing_CSV)
            lista_estudiates_ingenieria = []
            for estudiante in lector_ing:
                cedula, nombre, apellido, telefono, semestre, promedio, serial = estudiante
                lista_estudiates_ingenieria.append(ESTUDIANTE_INGENIERIA(cedula, nombre, apellido, telefono, semestre, promedio, serial))
        with open("PracticaFinal/Estudiantes_Diseno.csv", "a+", newline="", encoding='utf-8') as Est_Dis_CSV:
            Est_Dis_CSV.seek(0)
            lector_dis = csv.reader(Est_Dis_CSV)
            lista_estudiates_ingenieria = []
            for registro in lector_dis:
                cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, serial = registro
                lista_estudiates_ingenieria.append(ESTUDIANTE_DISENO(cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, serial))

        Est_Ing_CSV.close()
        Est_Dis_CSV.close()        

    def inactivar_estudiantes(self):
        pass
    def mostrar_estudiantes(self):
        with open("PracticaFinal/Estudiantes_Ingenieria.csv", "a+", newline="", encoding='utf-8') as Est_Ing_CSV:
            Est_Ing_CSV.seek(0)
            lector_ing = csv.reader(Est_Ing_CSV)
            for registro in lector_ing:
                cedula, nombre, apellido, telefono, semestre, promedio, serial = registro
                print(cedula, nombre, apellido, telefono, semestre, promedio, serial)

        with open("PracticaFinal/Estudiantes_Diseno.csv", "a+", newline="", encoding='utf-8') as Est_Dis_CSV:
            Est_Dis_CSV.seek(0)
            lector_dis = csv.reader(Est_Dis_CSV)
            for registro in lector_dis:
                cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, serial = registro
                print(cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, serial)

        Est_Ing_CSV.close()
        Est_Dis_CSV.close()

class Metodos_Equipos:
    def registrar_equipo(self):
        pass
    def modificar_equipo(self):
        pass
    def inactivar_equipo(self):
        pass
    def buscar_equipo(self):
        pass
class Metodos_Prestamos:
    def registrar_prestamo(self):
        pass
    def modificar_prestamo(self):
        pass
    def devolución_prestamo(self):
        pass
    def devolución_prestamo(self):
        pass
    def devolución_prestamo(self):
        pass
    def devolución_prestamo(self):
        pass
