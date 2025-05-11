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
        objeto_lector_estudiantes = Metodos_Estudiantes()
        objeto_lector_estudiantes.lector_csv_estudiantes() # Ejecución de método lector para usar las listas
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
        
        objeto_lector_estudiantes.Estudiantes_ingenieria_csv.close()
        objeto_lector_estudiantes.Estudiantes_diseno_csv.close()
        
    def menu_estudiantes(self):
        objeto_prestamo_equipos = Metodos_Prestamos()
        
    def menu_administrador(self):
        objeto_registro_estudiantes = Metodos_Estudiantes()
        objeto_registro_estudiantes.registrar_estudiantes_validacion_carrera()
        objeto_registro_equipos = Metodos_Equipos()
        objeto_prestamo_equipos = Metodos_Prestamos()
   
class Metodos_Estudiantes:
    def lector_csv_estudiantes(self):
        self.Estudiantes_ingenieria_csv = open("PracticaFinal/Estudiantes_Ingenieria.csv", "a+", newline="", encoding='utf-8')
        self.Estudiantes_ingenieria_csv.seek(0)
        self.Lector_Ingenieria = csv.reader(self.Estudiantes_ingenieria_csv)
        self.Escritor_Ingenieria = csv.writer(self.Estudiantes_ingenieria_csv)
        self.cedulas_estudiantes_ingenieria_lista = []
        self.estudiantes_ingenieria_lista = []

        for estudiante in self.Lector_Ingenieria:
            cedula = estudiante[0]
            self.cedulas_estudiantes_ingenieria_lista.append(cedula)

        for estudiante in self.Lector_Ingenieria:
            cedula, nombre, apellido, telefono, semestre, promedio, serial = estudiante
            self.estudiantes_ingenieria_lista.append(ESTUDIANTE_INGENIERIA(cedula, nombre, apellido, telefono, semestre, promedio, serial))
                
        self.Estudiantes_diseno_csv = open("PracticaFinal/Estudiantes_Diseno.csv", "a+", newline="", encoding='utf-8')
        self.Estudiantes_diseno_csv.seek(0)
        self.Lector_Diseno = csv.reader(self.Estudiantes_diseno_csv)
        self.Escritor_Diseno = csv.writer(self.Estudiantes_diseno_csv)
        self.cedulas_estudiantes_diseno_lista = []
        self.estudiantes_diseno_lista = []

        for estudiante in self.Lector_Diseno:
            cedula = estudiante[0]
            self.cedulas_estudiantes_diseno_lista.append(cedula)

        for registro in self.Lector_Diseno:
            cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, serial = registro
            self.estudiantes_diseno_lista.append(ESTUDIANTE_DISENO(cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, serial))            

    def registrar_estudiantes_validacion_carrera(self):
        self.lector_csv_estudiantes()
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
        self.frame_eleccion_carrera = CTK.CTkFrame(self.ventana_registro_estudiantes)
        self.frame_eleccion_carrera.pack()
        self.eleccion_carrera = self.desplegable_carrera.get()
        self.frame_validacion_carrera.destroy()
        
        self.etiqueta_cedula = CTK.CTkLabel(self.frame_eleccion_carrera, text="Cédula")
        self.etiqueta_cedula.grid(row=1,column=0,pady=5,padx=10)
        self.entrada_cedula = CTK.CTkEntry(self.frame_eleccion_carrera)
        self.entrada_cedula.grid(row=1,column=1,pady=5,padx=10)
        self.etiqueta_nombre = CTK.CTkLabel(self.frame_eleccion_carrera, text="Nombre")
        self.etiqueta_nombre.grid(row=2,column=0,pady=5,padx=10)
        self.entrada_nombre = CTK.CTkEntry(self.frame_eleccion_carrera)
        self.entrada_nombre.grid(row=2,column=1,pady=5,padx=10)
        self.etiqueta_apellido = CTK.CTkLabel(self.frame_eleccion_carrera, text="Apellido")
        self.etiqueta_apellido.grid(row=3,column=0,pady=5,padx=10)
        self.entrada_apellido = CTK.CTkEntry(self.frame_eleccion_carrera)
        self.entrada_apellido.grid(row=3,column=1,pady=5,padx=10)
        self.etiqueta_telefono = CTK.CTkLabel(self.frame_eleccion_carrera, text="Teléfono")
        self.etiqueta_telefono.grid(row=4,column=0,pady=5,padx=10)
        self.entrada_telefono = CTK.CTkEntry(self.frame_eleccion_carrera)
        self.entrada_telefono.grid(row=4,column=1,pady=5,padx=10)

        if self.eleccion_carrera == "Ingeniería":
            
            self.etiqueta_carrera = CTK.CTkLabel(self.frame_eleccion_carrera, text=self.eleccion_carrera)
            self.etiqueta_carrera.grid(row=0, column=0,pady=5,padx=10, columnspan=2)
            
            self.etiqueta_semestre = CTK.CTkLabel(self.frame_eleccion_carrera, text="Semestre")
            self.etiqueta_semestre.grid(row=5,column=0,pady=5,padx=10)
            self.desplegable_semestre = CTK.CTkComboBox(self.frame_eleccion_carrera, values=[str(i+1) for i in range(12)], state="readonly")
            self.desplegable_semestre.set("1")
            self.desplegable_semestre.grid(row=5,column=1,pady=5,padx=10)
            self.etiqueta_promedio = CTK.CTkLabel(self.frame_eleccion_carrera, text="Promedio")
            self.etiqueta_promedio.grid(row=6,column=0,pady=5,padx=10)
            self.entrada_promedio = CTK.CTkEntry(self.frame_eleccion_carrera)
            self.entrada_promedio.grid(row=6,column=1,pady=5,padx=10)

        elif self.eleccion_carrera == "Diseño":

            self.etiqueta_carrera = CTK.CTkLabel(self.frame_eleccion_carrera, text=self.eleccion_carrera)
            self.etiqueta_carrera.grid(row=0, column=0,pady=5,padx=10, columnspan=2)
            
            self.etiqueta_modalidad = CTK.CTkLabel(self.frame_eleccion_carrera, text="Modalidad")
            self.etiqueta_modalidad.grid(row=5,column=0,pady=5,padx=10)
            self.desplegable_modalidad = CTK.CTkComboBox(self.frame_eleccion_carrera, values=["Virtual","Presencial","Mixto"], state="readonly")
            self.desplegable_modalidad.set("Seleccione")
            self.desplegable_modalidad.grid(row=5,column=1,pady=5,padx=10)
            self.etiqueta_cantidad_materias = CTK.CTkLabel(self.frame_eleccion_carrera, text="Cantidad de materias")
            self.etiqueta_cantidad_materias.grid(row=6,column=0,pady=5,padx=10)
            self.desplegable_cantidad_materias = CTK.CTkComboBox(self.frame_eleccion_carrera, values=[str(i+1) for i in range(20)], state="readonly")
            self.desplegable_cantidad_materias.set(0)
            self.desplegable_cantidad_materias.grid(row=6,column=1,pady=5,padx=10)
        
        self.boton_validacion = CTK.CTkButton(self.frame_eleccion_carrera, text="Registrar", command=self.validacion_errores_registro)
        self.boton_validacion.grid(row=7,column=0, columnspan=2,pady=5,padx=10)

            
    def validacion_errores_registro(self):
        self.ventana_errores_registro = CTK.CTkToplevel()
        self.ventana_errores_registro.focus()
        self.ventana_errores_registro.grab_set()
        self.ventana_errores_registro.geometry("+300+100")
        self.frame_errores_registro = CTK.CTkScrollableFrame(self.ventana_errores_registro)
        self.lista_errores_registro = []
        
        if not self.entrada_cedula.get():
            self.lista_errores_registro.append("Ingresar cédula.")
        if not self.entrada_nombre.get():
            self.lista_errores_registro.append("Ingresar nombre.")
        if not self.entrada_apellido.get():
            self.lista_errores_registro.append("Ingresar apellido.")
        if not self.entrada_telefono.get():
            self.lista_errores_registro.append("Ingresar teléfono.")
        
        if self.eleccion_carrera == "Ingeniería":
            
            if not self.entrada_promedio.get():
                self.lista_errores_registro.append("Ingresar promedio.")
            elif self.entrada_promedio.get():
                try:
                    float(self.entrada_promedio.get())
                except ValueError:
                    self.lista_errores_registro.append("Promedio: Valor ingresado no válido.")

        elif self.eleccion_carrera == "Diseño":
            
            if self.desplegable_modalidad.get() == "Seleccione":
                self.lista_errores_registro.append("Seleccione una modalidad de estudio.")
            if self.desplegable_cantidad_materias.get() == 0:
                self.lista_errores_registro.append("Seleccione la cantidad de materias.")

        if len(self.lista_errores_registro) > 0:

            self.ventana_errores_registro.title("Error de registro")
            self.mensaje_error = CTK.CTkLabel(self.ventana_errores_registro, text="Se presentan las siguientes inconsistencias en el registro: ")
            self.mensaje_error.pack(pady=5,padx=10)
            self.frame_errores_registro.pack(pady=5,padx=10)
            for numero, elemento in enumerate(self.lista_errores_registro):
                CTK.CTkLabel(self.frame_errores_registro, text=f"{numero+1}. {elemento}", justify="left", anchor="w").pack(padx=5,anchor="w")
            return

        else:
            if self.eleccion_carrera == "Ingeniería":
                self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas
                            
                for registro_actual in self.cedulas_estudiantes_ingenieria_lista:
                    if registro_actual == var_cedula:
                        print("La persona ingresada ya se encuentra registrada.")
                        break
                    else:
                        registro = ESTUDIANTE_INGENIERIA(var_cedula,var_nombre,var_apellido,var_telefono,var_semestre,var_promedio)
                        self.Escritor_Ingenieria.writerow(registro.convertir_lista())
                        print("Registro exitoso.")
                        break
                
                if len(self.cedulas_estudiantes_ingenieria_lista) == 0:
                    registro = ESTUDIANTE_INGENIERIA(var_cedula,var_nombre,var_apellido,var_telefono,var_semestre,var_promedio)
                    self.Escritor_Ingenieria.writerow(registro.convertir_lista())
                    print("Registro exitoso.")
                
                self.Estudiantes_ingenieria_csv.close()
                        
            elif self.eleccion_carrera == "Diseño":
                self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas
                var_cedula = input("Ingresa el/la cedula: ") 
                var_nombre = input("Ingresa el/la nombre: ") 
                var_apellido = input("Ingresa el/la apellido: ") 
                var_telefono = input("Ingresa el/la telefono: ") 
                var_modalidad = input("Ingresa el/la modalidad: ") 
                var_cantidad_asignaturas = int(input("Ingresa el/la cantidad de asignaturas: "))

                for registro_actual in self.cedulas_estudiantes_diseno_lista:
                    if registro_actual == var_cedula:
                        print("La persona ingresada ya se encuentra registrada.")
                        break
                    else:
                        registro = ESTUDIANTE_DISENO(var_cedula,var_nombre,var_apellido,var_telefono,var_modalidad,var_cantidad_asignaturas)
                        self.Escritor_Diseno.writerow(registro.convertir_lista())
                        print("Registro exitoso.")
                        break
                    
                if len(self.cedulas_estudiantes_diseno_lista) == 0:
                    registro = ESTUDIANTE_DISENO(var_cedula,var_nombre,var_apellido,var_telefono,var_modalidad,var_cantidad_asignaturas)
                    self.Escritor_Diseno.writerow(registro.convertir_lista())
                    print("Registro exitoso.")

                self.Estudiantes_diseno_csv.close()
        
    def modificar_estudiantes(self):
        pass
    def inactivar_estudiantes(self):
        pass
    def mostrar_estudiantes(self):
        self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas
#        with open("PracticaFinal/Estudiantes_Ingenieria.csv", "a+", newline="", encoding='utf-8') as self.Estudiantes_ingenieria_csv:
#            self.Estudiantes_ingenieria_csv.seek(0)
#            self.lector_ingenieria = csv.reader(self.Estudiantes_ingenieria_csv)
        for registro in self.Lector_Ingenieria:
            cedula, nombre, apellido, telefono, semestre, promedio, serial = registro
            print(cedula, nombre, apellido, telefono, semestre, promedio, serial)

#        with open("PracticaFinal/Estudiantes_Diseno.csv", "a+", newline="", encoding='utf-8') as self.Estudiantes_diseno_csv:
#            self.Estudiantes_diseno_csv.seek(0)
#            self.lector_diseno = csv.reader(self.Estudiantes_diseno_csv)
        for registro in self.Lector_Diseno:
            cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, serial = registro
            print(cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, serial)

        self.Estudiantes_ingenieria_csv.close()
        self.Estudiantes_diseno_csv.close()

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
