import csv
import customtkinter as CTK
import Objetos

class Metodos_Prestamos:
    
    def __init__(self, informacion_estudiante, carrera_estudiante):
        self.informacion_estudiante = informacion_estudiante
        self.eleccion_carrera = carrera_estudiante

    def lector_csv_estudiantes(self, leer_archivo=True, modificar=False):
        if leer_archivo:
            self.cedulas_estudiantes_ingenieria_lista = []
            self.estudiantes_ingenieria_lista = []
            self.computadores_prestados_ingenieria = []
            with open("Estudiantes_Ingenieria.csv", "r", newline="", encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                for e in lector:
                    cedula, nombre, apellido, telefono, semestre, promedio, estado, serial = e
                    self.cedulas_estudiantes_ingenieria_lista.append(cedula)
                    self.computadores_prestados_ingenieria.append(serial)
                    self.estudiantes_ingenieria_lista.append(Objetos.ESTUDIANTE_INGENIERIA(cedula, nombre, apellido, telefono, semestre, promedio, estado, serial))

            self.cedulas_estudiantes_diseno_lista = []
            self.estudiantes_diseno_lista = []
            self.tabletas_prestados_diseno = []
            with open("Estudiantes_Diseno.csv", "r", newline="", encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                for e in lector:
                    cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, estado, serial = e
                    self.cedulas_estudiantes_diseno_lista.append(cedula)
                    self.tabletas_prestados_diseno.append(serial)
                    self.estudiantes_diseno_lista.append(Objetos.ESTUDIANTE_DISENO(cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, estado, serial))

            self.computadores_ingenieria = []
            self.computadores_ingenieria_disponibles = []
            with open("Computadores_Portatiles.csv", "r", newline="", encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                for e in lector:
                    serial, marca, tamano, precio, sistema_operativo, procesador, estado = e
                    self.computadores_ingenieria.append(Objetos.COMPUTADOR_PORTATIL(serial, marca, tamano, precio, sistema_operativo, procesador, estado))
                for e in self.computadores_ingenieria:
                    if e.serial not in self.computadores_prestados_ingenieria:
                        self.computadores_ingenieria_disponibles.append(e.serial)

            self.tabletas_diseno = []
            self.tabletas_diseno_disponibles = []
            with open("Tabletas_Graficas.csv", "r", newline="", encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                for e in lector:
                    serial, marca, tamano, precio, almacenamiento, peso, estado = e
                    self.tabletas_diseno.append(Objetos.TABLETA_GRAFICA(serial, marca, tamano, precio, almacenamiento, peso, estado))
                for e in self.tabletas_diseno:
                    if e.serial not in self.tabletas_prestados_diseno:
                        self.tabletas_diseno_disponibles.append(e.serial)

        if modificar:
            with open("Estudiantes_Ingenieria.csv", "w", newline="", encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                for e in self.estudiantes_ingenieria_lista:
                    escritor.writerow(e.convertir_lista_ingenieria())
            with open("Estudiantes_Diseno.csv", "w", newline="", encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                for e in self.estudiantes_diseno_lista:
                    escritor.writerow(e.convertir_lista_diseno())

    def paneles_prestamo(self, frame, carrera):
        self.frame_eleccion_carrera = CTK.CTkFrame(frame, fg_color="transparent")
        self.frame_eleccion_carrera.pack()

        # Campos comunes
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
        
        # Campo específico según carrera
        if carrera == "Ingeniería":
            CTK.CTkLabel(self.frame_eleccion_carrera, text="Computador").grid(row=5, column=0, padx=10, pady=5)
            self.desplegable_computador = CTK.CTkComboBox(self.frame_eleccion_carrera, values=self.computadores_ingenieria_disponibles, state="readonly")
            self.desplegable_computador.set("Seleccione")
            self.desplegable_computador.grid(row=5, column=1, padx=10, pady=5)
        else:
            CTK.CTkLabel(self.frame_eleccion_carrera, text="Tableta").grid(row=5, column=0, padx=10, pady=5)
            self.desplegable_tableta = CTK.CTkComboBox(self.frame_eleccion_carrera, values=self.tabletas_diseno_disponibles, state="readonly")
            self.desplegable_tableta.set("Seleccione")
            self.desplegable_tableta.grid(row=5, column=1, padx=10, pady=5)

    def precargar_datos_estudiante(self, persona, carrera, editable=True):
        self.entrada_cedula.insert(0, persona.cedula)
        self.entrada_nombre.insert(0, persona.nombre)
        self.entrada_apellido.insert(0, persona.apellido)

        if carrera == "Ingeniería":
            self.desplegable_computador.set(persona.serial)
        else:
            self.desplegable_tableta.set(persona.serial)

        if not editable:
            for entry in [self.entrada_cedula, self.entrada_nombre, self.entrada_apellido]:
                entry.configure(state="readonly")


    def validar_datos_registro(self, carrera):
        errores = []
        if carrera == "Ingeniería" and self.desplegable_computador.get() == "Seleccione":
            errores.append("Selecciona un computador.")
        elif carrera == "Diseño" and self.desplegable_tableta.get() == "Seleccione":
            errores.append("Selecciona una tableta.")
        return errores

    def mostrar_errores_registro(self, errores):
        if errores:
            ventana = CTK.CTkToplevel()
            ventana.title("Error de registro")
            ventana.geometry("270x150+850+300")
            ventana.resizable(False, False)
            ventana.grab_set()
            CTK.CTkLabel(ventana, text="Inconsistencias detectadas:").pack(pady=5)
            frame = CTK.CTkScrollableFrame(ventana, width=250)
            frame.pack(padx=10, pady=5)
            for i, error in enumerate(errores):
                CTK.CTkLabel(frame, text=f"{i+1}. {error}", anchor="w").pack(anchor="w", padx=5)

    def guardar_serial(self, cedula, nuevo_serial, devolucion=False):

        for persona in self.estudiantes_ingenieria_lista + self.estudiantes_diseno_lista:
            if persona.cedula == cedula or persona.serial == cedula:
                if devolucion:
                    persona.serial = ""
                else:
                    persona.serial = nuevo_serial
                break
        self.lector_csv_estudiantes(leer_archivo=False, modificar=True)

    def registrar_prestamo_validacion_carrera(self, ventana):
        self.lector_csv_estudiantes()
        self.etiqueta_error_prestamo = CTK.CTkLabel(ventana, height=15)
        estudiante_actual = None

        if self.eleccion_carrera == "Ingeniería":
            lista = self.estudiantes_ingenieria_lista 
        else:
            lista = self.estudiantes_diseno_lista
            
        for persona in lista:
            if persona.cedula == self.informacion_estudiante.cedula:
                estudiante_actual = persona
                break

        if not estudiante_actual:
            self.etiqueta_error_prestamo.configure(text="Estudiante no encontrado.")
            self.etiqueta_error_prestamo.grid(row=1, column=0)
            return

        if estudiante_actual.serial == "":
            self.paneles_prestamo(ventana, self.eleccion_carrera)
            self.precargar_datos_estudiante(estudiante_actual, self.eleccion_carrera)
            CTK.CTkLabel(self.frame_eleccion_carrera, text="Registrar préstamo").grid(row=0, column=0, columnspan=2)
            self.boton_validacion = CTK.CTkButton(self.frame_eleccion_carrera, text="Registrar", command=self.realizar_registro, width=170)
            self.boton_validacion.grid(row=7, column=0, columnspan=2, pady=5)
            self.etiqueta_excepciones = CTK.CTkLabel(self.frame_eleccion_carrera, height=15)
        else:
            self.etiqueta_error_prestamo.configure(text="Ya tiene un equipo prestado. Devuelva primero el actual.")
            self.etiqueta_error_prestamo.grid(row=1, column=0, pady=5)

    def realizar_registro(self):
        errores = self.validar_datos_registro(self.eleccion_carrera)
        if errores:
            self.mostrar_errores_registro(errores)
        else:
            if self.eleccion_carrera == "Ingeniería":
                serial = self.desplegable_computador.get()
            else:
                serial = self.desplegable_tableta.get()

            self.guardar_serial(self.informacion_estudiante.cedula, serial)
            self.etiqueta_excepciones.configure(text="Registro completado exitosamente.")
            self.etiqueta_excepciones.grid(row=8, column=0, columnspan=2, pady=5)
            
    def busqueda_estudiantes_admin(self,ventana_busqueda_estudiantes_admin):
        def buscar_estudiante_admin():
            self.lector_csv_estudiantes()
            try:
                for elemento in self.ventana_carga_busqueda_estudiantes_admin.winfo_children():
                    elemento.destroy()
            except:
                pass
            cedula_buscar_admin = self.entrada_id_busqueda.get()
            self.buscar_registro_modificar(self.ventana_carga_busqueda_estudiantes_admin, cedula_buscar_admin)
        
        self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas de cédulas u objetos
        self.frame_validacion_carrera = CTK.CTkFrame(ventana_busqueda_estudiantes_admin,fg_color="transparent",height=48)
        self.frame_validacion_carrera.pack()
        self.ventana_carga_busqueda_estudiantes_admin = CTK.CTkFrame(ventana_busqueda_estudiantes_admin)
        self.ventana_carga_busqueda_estudiantes_admin.pack()

        self.etiqueta_id_busqueda = CTK.CTkLabel(self.frame_validacion_carrera, text="Id/Serial")
        self.etiqueta_id_busqueda.grid(row=0, column=0, padx=5, pady=10)

        self.entrada_id_busqueda = CTK.CTkEntry(self.frame_validacion_carrera)
        self.entrada_id_busqueda.grid(row=0, column=1, padx=5, pady=10)

        self.boton_carrera_busqueda = CTK.CTkButton(self.frame_validacion_carrera, text="🔍", font=(None,20), width=28, command=buscar_estudiante_admin)
        self.boton_carrera_busqueda.grid(row=0, column=4, padx=5, pady=10)

        self.etiqueta_excepciones = CTK.CTkLabel(self.frame_validacion_carrera,height=15)

    def buscar_registro_modificar(self, ventana, cedula_buscar):
        self.lector_csv_estudiantes()

        frame = CTK.CTkFrame(ventana,fg_color="transparent")
        frame.pack()
        etiqueta_estados = CTK.CTkLabel(frame,text="")
#        self.paneles_prestamo(frame, self.eleccion_carrera)
        persona_actual = None

        lista_personas_ingenieria, lista_cedulas_ingenieria, seriales_ingenieria = self.estudiantes_ingenieria_lista, self.cedulas_estudiantes_ingenieria_lista, self.computadores_prestados_ingenieria
        lista_personas_diseno, lista_cedulas_diseno, seriales_diseno = self.estudiantes_diseno_lista, self.cedulas_estudiantes_diseno_lista, self.tabletas_prestados_diseno

        lista_personas = []

        if cedula_buscar in lista_cedulas_ingenieria + seriales_ingenieria:
            self.eleccion_carrera = "Ingeniería"
            lista_personas = lista_personas_ingenieria
        elif cedula_buscar in lista_cedulas_diseno + seriales_diseno:
            self.eleccion_carrera = "Diseño"
            lista_personas = lista_personas_diseno

        for persona in lista_personas:
            if persona.cedula == cedula_buscar or persona.serial == cedula_buscar:
                if persona.estado == "INACTIVO":
                    etiqueta_estados.configure(text="Usuario inactivo.")
                    return
                persona_actual = persona
                break
            
        def guardar_nuevo_serial():
            if self.eleccion_carrera == "Ingeniería":
                serial = self.desplegable_computador.get()
            else:
                serial = self.desplegable_tableta.get()

            self.guardar_serial(cedula_buscar,serial)
            etiqueta_estados.configure(text="Modificación completada exitosamente.")
            
        def devolucion():
            if self.eleccion_carrera == "Ingeniería":
                serial = self.desplegable_computador.get()
                self.desplegable_computador.set("")
            else:
                serial = self.desplegable_tableta.get()
                self.desplegable_tableta.set("")

            self.guardar_serial(cedula_buscar,serial, True)
            etiqueta_estados.configure(text="Devolución completada exitosamente.")

        if persona_actual:
            self.paneles_prestamo(frame, self.eleccion_carrera)
            self.precargar_datos_estudiante(persona_actual, self.eleccion_carrera, False)
            CTK.CTkButton(frame, text="Guardar cambios", command=guardar_nuevo_serial).pack(pady=10)
            CTK.CTkButton(frame, text="Realizar devolución", command=devolucion).pack()
            etiqueta_estados.pack()
        else:
            CTK.CTkLabel(frame, text="Documento/serial no encontrado.").pack()

    def mostrar_prestamos(self, ventana_mostrar_prestamos):
        self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas de cédulas u objetos
        pantalla_validacion_carrera = CTK.CTkFrame(ventana_mostrar_prestamos)
        pantalla_validacion_carrera.pack(pady=10)
        pantalla_mostrar_registros = CTK.CTkFrame(ventana_mostrar_prestamos)
        
        def mostrar_prestamos_segun_equipo(equipo):
            pantalla_validacion_carrera.destroy()
            pantalla_mostrar_registros.pack(pady=10)
            
            if equipo == "Computadores":
                lista = self.estudiantes_ingenieria_lista
            if equipo == "Tabletas":
                lista = self.estudiantes_diseno_lista
            
            for numero_registro, registro in enumerate(lista):
                
                if registro.estado in ["ACTIVO", "Estado"] and not registro.serial == "":
                    try:
                        registro_lista = registro.convertir_lista_ingenieria()
                    except:
                        try:
                            registro_lista = registro.convertir_lista_diseno()
                        except:
                            etiqueta_error_conversion = CTK.CTkLabel(pantalla_validacion_carrera, text="Error al convertir a listas.", height=15)
                            etiqueta_error_conversion.grid(row=2, column=0, columnspan=3, padx=3)
                                                
                    if numero_registro == 0:
                        for numero, dato in enumerate(registro_lista):
                            if numero in [0,1,2,7]:
                                CTK.CTkLabel(pantalla_mostrar_registros, text=dato, fg_color="#2A2A2A", height= 33, width=120, wraplength=115).grid(row=numero_registro+1, column=numero, pady=3)
                    else:
                        for numero, dato in enumerate(registro_lista):
                            if numero in [0,1,2,7]:
                                etiqueta_entrada_registro = CTK.CTkEntry(pantalla_mostrar_registros, fg_color="#4b4b4b", justify="center", height= 33, width=120, corner_radius=0, border_width=0)
                                etiqueta_entrada_registro.insert(0,dato)
                                etiqueta_entrada_registro.configure(state="readonly")
                                etiqueta_entrada_registro.grid(row=numero_registro+1, column=numero)
        
        def mostar_prestamos_boton():
            mostrar_prestamos_segun_equipo(desplegable_equipo.get())
            
        etiqueta_equipo = CTK.CTkLabel(pantalla_validacion_carrera, text="Seleccionar equipo")
        etiqueta_equipo.grid(row=0, column=0, padx=10)
        desplegable_equipo = CTK.CTkComboBox(pantalla_validacion_carrera, values=["Computadores","Tabletas"], state="readonly")
        desplegable_equipo.set("Computadores")
        desplegable_equipo.grid(row=0, column=1, padx=10)
        boton_buscar_equipo = CTK.CTkButton(pantalla_validacion_carrera, text="🔍", font=(None,20), width=28, command=mostar_prestamos_boton)
        boton_buscar_equipo.grid(row=0, column=2, padx=10) 
