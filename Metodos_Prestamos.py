import csv
import customtkinter as CTK
import Objetos
import Pagina_Inicial

class Metodos_Prestamos:

#    def registrar_prestamo(self):
#        pass
#    def modificar_prestamo(self):
#        pass
#    def devolución_prestamo(self):
#        pass
#    def devolución_prestamo(self):
#        pass
#    def devolución_prestamo(self):
#        pass
#    def devolución_prestamo(self):
#        pass
    
    # Lee ambos archivos .csv donde se almancenan los estudiantes.
    def lector_csv_estudiantes(self, leer_archivo=True, modificar=False):
        if leer_archivo:
            self.cedulas_estudiantes_ingenieria_lista = []
            self.estudiantes_ingenieria_lista = []
            self.computadores_prestados_ingenieria = []
            with open("PracticaFinal/Estudiantes_Ingenieria.csv", "r", newline="", encoding='utf-8') as Estudiantes_ingenieria_csv:
                Lector_Ingenieria = csv.reader(Estudiantes_ingenieria_csv)
                # Crea un lista con los valores extraidos, (lista de cédulas de ingenieria)
                for estudiante in Lector_Ingenieria:
                    cedula, nombre, apellido, telefono, semestre, promedio, estado, serial = estudiante
                    self.cedulas_estudiantes_ingenieria_lista.append(cedula)
                    self.computadores_prestados_ingenieria.append(serial)
                # Extrae toda la información del archivo, convierte los valores en objetos y crea un lista (lista de objetos de ingenieria)
                    self.estudiantes_ingenieria_lista.append(Objetos.ESTUDIANTE_INGENIERIA(cedula, nombre, apellido, telefono, semestre, promedio, estado, serial))

            self.cedulas_estudiantes_diseno_lista = []
            self.estudiantes_diseno_lista = []
            self.tabletas_prestados_diseno = []
            with open("PracticaFinal/Estudiantes_Diseno.csv", "r", newline="", encoding='utf-8') as Estudiantes_diseno_csv:
                Lector_Diseno = csv.reader(Estudiantes_diseno_csv)
                # Crea un lista con los valores extraidos, (lista de cédulas de diseño)
                for estudiante in Lector_Diseno:
                    cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, estado, serial = estudiante
                    self.cedulas_estudiantes_diseno_lista.append(cedula)
                    self.tabletas_prestados_diseno.append(serial)
                # Extrae toda la información del archivo, convierte los valores en objetos y crea un lista (lista de objetos de diseño)
                    self.estudiantes_diseno_lista.append(Objetos.ESTUDIANTE_DISENO(cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, estado, serial))
                
        if modificar:
            with open("PracticaFinal/Estudiantes_Ingenieria.csv", "w", newline="", encoding='utf-8') as Estudiantes_ingenieria_csv:
                Escritor_Ingenieria = csv.writer(Estudiantes_ingenieria_csv)
                for estudiante in self.estudiantes_ingenieria_lista:
                    Escritor_Ingenieria.writerow(estudiante.convertir_lista_ingenieria())

            with open("PracticaFinal/Estudiantes_Diseno.csv", "w", newline="", encoding='utf-8') as Estudiantes_diseno_csv:
                Escritor_Diseno = csv.writer(Estudiantes_diseno_csv)
                for estudiante in self.estudiantes_diseno_lista:
                    Escritor_Diseno.writerow(estudiante.convertir_lista_diseno())

    def registrar_prestamo_validacion_carrera(self,ventana_registro_prestamos, informacion_estudiante, carrera_estudiante):
        
        self.informacion_estudiante = informacion_estudiante
        self.eleccion_carrera = carrera_estudiante

        self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas de cédulas u objetos
        self.etiqueta_error_prestamo = CTK.CTkLabel(ventana_registro_prestamos,height=15)

        if carrera_estudiante == "Ingeniería":
            for persona in self.estudiantes_ingenieria_lista:
                if persona.cedula == informacion_estudiante.cedula:
                    estudiante_actual = persona
                    break

        elif carrera_estudiante == "Diseño":
            for persona in self.estudiantes_diseno_lista:
                if persona.cedula == informacion_estudiante.cedula:
                    estudiante_actual = persona
                    break

        if estudiante_actual.serial == "":
            self.paneles_prestamo(ventana_registro_prestamos, carrera_elegida=carrera_estudiante)
            self.entrada_cedula.insert(0,estudiante_actual.cedula)
            self.entrada_cedula.configure(state="readonly")
            self.entrada_nombre.insert(0,estudiante_actual.nombre)
            self.entrada_nombre.configure(state="readonly")
            self.entrada_apellido.insert(0,estudiante_actual.apellido)
            self.entrada_apellido.configure(state="readonly")
            
            # Boton validación de datos ingresados y posterior registro si es el caso.
            self.etiqueta_prestamo = CTK.CTkLabel(self.frame_eleccion_carrera, text="Registrar prestamo")
            self.etiqueta_prestamo.grid(row=0,column=0, columnspan=2,pady=5,padx=10)
            self.boton_validacion = CTK.CTkButton(self.frame_eleccion_carrera, text="Registrar", command=self.realizar_registro, width=170)
            self.boton_validacion.grid(row=7,column=0, columnspan=2,pady=5,padx=10)
            self.etiqueta_excepciones = CTK.CTkLabel(self.frame_eleccion_carrera,height=15)

        else:
            self.etiqueta_error_prestamo.configure(text="Actualmente ya cuenta con un equipo bajo prestamo, por favor realizar primero la devolución.", padx=10, pady=15)
            self.etiqueta_error_prestamo.grid(row=1,column=0,pady=5,padx=10)

    def paneles_prestamo(self, frame_para_paneles, carrera_elegida):
                
        self.frame_eleccion_carrera = CTK.CTkFrame(frame_para_paneles,fg_color="transparent")
        self.frame_eleccion_carrera.pack()

        # Se muestra las entradas comunes para todos los estudiantes.
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
        
        # Se muestra las entradas específicas para todos los estudiantes según su carrera.
        if carrera_elegida == "Ingeniería":
                        
            self.etiqueta_computador = CTK.CTkLabel(self.frame_eleccion_carrera, text="Computador")
            self.etiqueta_computador.grid(row=5,column=0,pady=5,padx=10)
            self.desplegable_computador = CTK.CTkComboBox(self.frame_eleccion_carrera, values=["Sin equipos aún"], state="readonly")
            self.desplegable_computador.set("Seleccione")
            self.desplegable_computador.grid(row=5,column=1,pady=5,padx=10)

        elif carrera_elegida == "Diseño":

            self.etiqueta_tableta = CTK.CTkLabel(self.frame_eleccion_carrera, text="Tableta")
            self.etiqueta_tableta.grid(row=5,column=0,pady=5,padx=10)
            self.desplegable_tableta = CTK.CTkComboBox(self.frame_eleccion_carrera, values=["Sin equipos aún"], state="readonly")
            self.desplegable_tableta.set("Seleccione")
            self.desplegable_tableta.grid(row=5,column=1,pady=5,padx=10)
        
    # Función para validar datos ingresados y si es el caso el registro
    def realizar_registro(self):
        errores = self.validar_datos_registro(self.eleccion_carrera)

        if errores:
            self.mostrar_errores_registro(errores)
        else:
            self.guardar_registro(informacion_estudiante_guardar=self.informacion_estudiante)

    # Validar datos ingresados en los entry y combobox
    def validar_datos_registro(self, eleccion_carrera):
        lista_errores_registro = []
                
        # Validación de datos según carrera.
        if eleccion_carrera == "Ingeniería":
            
            if self.desplegable_computador.get() == "Seleccione":
                lista_errores_registro.append("Selecciona un equipo")

        elif eleccion_carrera == "Diseño":
            
            if self.desplegable_tableta.get() == "Seleccione":
                lista_errores_registro.append("Selecciona un equipo")

        return lista_errores_registro

    # Si hay errores, se mustra ventana (Toplevel) con mensajes
    def mostrar_errores_registro(self, lista_errores):
        lista_errores_registro = lista_errores

        if len(lista_errores_registro) > 0:
            self.ventana_errores_registro = CTK.CTkToplevel()
            self.ventana_errores_registro.focus()
            self.ventana_errores_registro.grab_set()
            self.ventana_errores_registro.geometry("270x150+850+300")
            self.ventana_errores_registro.resizable(False,False)
            self.frame_errores_registro = CTK.CTkScrollableFrame(self.ventana_errores_registro,width=250)
            self.mensaje_error = CTK.CTkLabel(self.ventana_errores_registro, text="", wraplength=245)
            self.mensaje_error.pack(padx=10)

            self.ventana_errores_registro.title("Error de registro")
            self.mensaje_error.configure(text="Inconsistencias detectadas:")
            self.frame_errores_registro.pack(pady=5,padx=10)
            for numero, elemento in enumerate(lista_errores_registro):
                CTK.CTkLabel(self.frame_errores_registro, text=f"{numero+1}. {elemento}", justify="left", anchor="w",wraplength=225).pack(padx=5,anchor="w")

    # Guardar datos en archivos .csv
    def guardar_registro(self, informacion_estudiante_guardar):
        self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas de cédulas u objetos

        cedula = informacion_estudiante_guardar.cedula
                
        if self.eleccion_carrera == "Ingeniería":
            for persona in self.estudiantes_ingenieria_lista:
                if persona.cedula == cedula:
                    persona.serial = self.desplegable_computador.get()
                    self.lector_csv_estudiantes(leer_archivo=False,modificar=True)
                    break
                    
        elif self.eleccion_carrera == "Diseño":
            for persona in self.estudiantes_diseno_lista:
                if persona.cedula == cedula:
                    persona.serial = self.desplegable_tableta.get()
                    self.lector_csv_estudiantes(leer_archivo=False,modificar=True)
                    break

        self.etiqueta_excepciones.configure(text="El registro se ha completado exitosamente.", padx=10, pady=15)
        self.etiqueta_excepciones.grid(row=8,column=0, columnspan=2,pady=5,padx=10)
        
#    def busqueda_estudiantes(self,ventana_modificacion_estudiantes):
#        self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas de cédulas u objetos
#        self.ventana_modificacion_estudiantes = CTK.CTkFrame(ventana_modificacion_estudiantes)
#        self.ventana_modificacion_estudiantes.pack()
#        self.frame_validacion_carrera = CTK.CTkFrame(self.ventana_modificacion_estudiantes,fg_color="transparent")
#        self.frame_validacion_carrera.pack()
#
#        self.etiqueta_id_busqueda = CTK.CTkLabel(self.frame_validacion_carrera, text="Id")
#        self.etiqueta_id_busqueda.grid(row=0, column=0, padx=5, pady=10)
#        self.entrada_id_busqueda = CTK.CTkEntry(self.frame_validacion_carrera)
#        self.entrada_id_busqueda.grid(row=0, column=1, padx=5, pady=10)
#
#        self.etiqueta_carrera_busqueda = CTK.CTkLabel(self.frame_validacion_carrera, text="Carrera")
#        self.etiqueta_carrera_busqueda.grid(row=0, column=2, padx=5, pady=10)
#        self.desplegable_carrera_busqueda = CTK.CTkComboBox(self.frame_validacion_carrera, values=["Ingeniería","Diseño"], state="readonly")
#        self.desplegable_carrera_busqueda.set("Ingeniería")
#        self.desplegable_carrera_busqueda.grid(row=0, column=3, padx=5, pady=10)
#        self.boton_carrera_busqueda = CTK.CTkButton(self.frame_validacion_carrera, text="Buscar", command=self.buscar_registro_modificar)
#        self.boton_carrera_busqueda.grid(row=0, column=4, padx=5, pady=10)
#        self.etiqueta_excepciones = CTK.CTkLabel(self.frame_validacion_carrera,height=15)
#        
#    def buscar_registro_modificar(self):
#        self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas de cédulas u objetos
#
#        try:
#            self.frame_mostrar_registro_busqueda.destroy()
#            self.boton_guardar.destroy()
#        except:
#            pass
#        self.frame_mostrar_registro_busqueda = CTK.CTkFrame(self.ventana_modificacion_estudiantes,fg_color="transparent")        
#
#        self.entrada_id_busqueda.configure(border_color="gray")
#        self.etiqueta_excepciones.configure(text="", padx=0, pady=0)        
#        try:
#            int(self.entrada_id_busqueda.get())
#        except ValueError:
#            self.entrada_id_busqueda.configure(border_color="#FF5844")
#            self.etiqueta_excepciones.configure(text=f"Valor no valido", padx=10, pady=3)
#            self.etiqueta_excepciones.grid(row=1, column=0, columnspan=5, padx=5)
#            return
#            
#        def actualizar_datos_estudiante(actualizar=True, activar=False):
#            if actualizar:
#                persona_actual.cedula = self.entrada_cedula.get()
#                persona_actual.nombre = self.entrada_nombre.get()
#                persona_actual.apellido = self.entrada_apellido.get()
#                persona_actual.telefono = self.entrada_telefono.get()
#                persona_actual.estado = self.desplegable_estado.get()
#                        
#                if self.eleccion_carrera == "Ingeniería":
#                    persona_actual.semestre = self.desplegable_semestre.get()
#                    persona_actual.promedio = self.entrada_promedio.get()
#                                            
#                elif self.eleccion_carrera == "Diseño":
#                    persona_actual.modalidad = self.desplegable_modalidad.get()
#                    persona_actual.cantidad_asignaturas = self.desplegable_cantidad_materias.get()
#            elif activar:
#                persona_actual.estado = self.desplegable_estado.get()
#                
#            self.lector_csv_estudiantes(leer_archivo=False, modificar=True)
#            self.frame_mostrar_registro_busqueda.destroy()
#            self.boton_guardar.destroy()
#
#            self.etiqueta_excepciones.configure(text="Datos actualizados correctamente.", padx=10, pady=3)
#            self.etiqueta_excepciones.grid(row=1, column=0, columnspan=5, padx=5)
#
#        def validacion_actualizar_datos_estudiante():
#            errores = self.validar_datos_registro()
#
#            if errores:
#                self.mostrar_errores_registro(errores)
#            else:
#                actualizar_datos_estudiante()
#
#        def activacion_estudiante():
#            actualizar_datos_estudiante(actualizar=False, activar=True)
#
#        cedula_busqueda = self.entrada_id_busqueda.get()
#        carrera_busqueda = self.desplegable_carrera_busqueda.get()
#
#        def mostrar_datos_estudiante(persona_actual, carrera):
#            self.frame_mostrar_registro_busqueda.pack()
#            self.paneles_segun_carrera(self.frame_mostrar_registro_busqueda, carrera, panel_estado=True)
#            self.entrada_cedula.insert(0, persona_actual.cedula)
#            self.entrada_cedula.configure(state="readonly")
#            self.entrada_nombre.insert(0, persona_actual.nombre)
#            self.entrada_apellido.insert(0, persona_actual.apellido)
#            self.entrada_telefono.insert(0, persona_actual.telefono)
#
#            if carrera == "Ingeniería":
#                self.desplegable_semestre.set(persona_actual.semestre)
#                self.entrada_promedio.insert(0, persona_actual.promedio)
#            elif carrera == "Diseño":
#                self.desplegable_modalidad.set(persona_actual.modalidad)
#                self.desplegable_cantidad_materias.set(persona_actual.cantidad_asignaturas)
#
#            self.desplegable_estado.set(persona_actual.estado)
#
#            self.boton_guardar = CTK.CTkButton(self.frame_mostrar_registro_busqueda, text="Guardar cambios", command=validacion_actualizar_datos_estudiante)
#            self.boton_guardar.pack(pady=10)
#
#
#        def mostrar_inactivo(persona_actual):
#            self.frame_mostrar_registro_busqueda.pack()
#            self.etiqueta_excepciones.configure(text="El documento se encuentra en estado INACTIVO.", padx=10, pady=3)
#            self.etiqueta_excepciones.grid(row=1, column=0, columnspan=5, padx=5)
#
#            CTK.CTkLabel(self.frame_mostrar_registro_busqueda, text=f"Cédula: {persona_actual.cedula}").grid(row=0, column=0, padx=10, pady=10)
#            self.desplegable_estado = CTK.CTkComboBox(self.frame_mostrar_registro_busqueda, values=["ACTIVO", "INACTIVO"], state="readonly")
#            self.desplegable_estado.set(persona_actual.estado)
#            self.desplegable_estado.grid(row=0, column=1, padx=10, pady=10)
#
#            self.boton_guardar = CTK.CTkButton(self.frame_mostrar_registro_busqueda, text="Guardar cambios", command=activacion_estudiante)
#            self.boton_guardar.grid(row=1, column=0, columnspan=2)
#
#        # Buscar en Ingeniería
#        if carrera_busqueda == "Ingeniería" and cedula_busqueda in self.cedulas_estudiantes_ingenieria_lista:
#            for persona_actual in self.estudiantes_ingenieria_lista:
#                if persona_actual.cedula == cedula_busqueda:
#                    if persona_actual.estado == "ACTIVO":
#                        mostrar_datos_estudiante(persona_actual, "Ingeniería")
#                    else:
#                        mostrar_inactivo(persona_actual)
#                    return
#
#        # Buscar en Diseño
#        elif carrera_busqueda == "Diseño" and cedula_busqueda in self.cedulas_estudiantes_diseno_lista:
#            for persona_actual in self.estudiantes_diseno_lista:
#                if persona_actual.cedula == cedula_busqueda:
#                    if persona_actual.estado == "ACTIVO":
#                        mostrar_datos_estudiante(persona_actual, "Diseño")
#                    else:
#                        mostrar_inactivo(persona_actual)
#                    return
#
#        # No se encontró
#        self.etiqueta_excepciones.configure(text=f"El documento {cedula_busqueda} no existe en el sistema.", padx=10, pady=3)
#        self.etiqueta_excepciones.grid(row=1, column=0, columnspan=5, padx=5)
#        return
#        
#    def mostrar_estudiantes(self, ventana_mostrar_estudiantes):
#        self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas de cédulas u objetos
#        pantalla_validacion_carrera = CTK.CTkFrame(ventana_mostrar_estudiantes)
#        pantalla_validacion_carrera.pack(pady=10)
#        pantalla_mostrar_registros = CTK.CTkFrame(ventana_mostrar_estudiantes)
#        
#        def mostrar_estudiantes_segun_carrera(carrera):
#            pantalla_validacion_carrera.destroy()
#            pantalla_mostrar_registros.pack(pady=10)
#            
#            if carrera == "Ingeniería":
#                lista = self.estudiantes_ingenieria_lista
#            if carrera == "Diseño":
#                lista = self.estudiantes_diseno_lista
#            
#            for numero_registro, registro in enumerate(lista):
#                try:
#                    registro_lista = registro.convertir_lista_ingenieria()
#                except:
#                    try:
#                        registro_lista = registro.convertir_lista_diseno()
#                    except:
#                        etiqueta_error_conversion = CTK.CTkLabel(pantalla_validacion_carrera, text="Error al convertir a listas.", height=15)
#                        etiqueta_error_conversion.grid(row=2, column=0, columnspan=3, padx=3)
#                
#                if numero_registro % 2 == 1:
#                    color_fondo = "#4b4b4b" 
#                else:
#                    color_fondo = None
#                        
#                if numero_registro == 0:
#                    for numero, dato in enumerate(registro_lista):
#                        CTK.CTkLabel(pantalla_mostrar_registros, text=dato, fg_color=color_fondo, height= 33, width=70, wraplength=70).grid(row=numero_registro+1, column=numero, pady=3)
#                else:
#                    for numero, dato in enumerate(registro_lista):
#                        etiqueta_entrada_registro = CTK.CTkEntry(pantalla_mostrar_registros, fg_color=color_fondo, height= 33, width=70, corner_radius=0, border_width=0)
#                        etiqueta_entrada_registro.insert(0,dato)
#                        etiqueta_entrada_registro.configure(state="readonly")
#                        etiqueta_entrada_registro.grid(row=numero_registro+1, column=numero)
#        
#        def mostar_estudiantes_boton():
#            mostrar_estudiantes_segun_carrera(desplegable_carrera.get())
#            
#        etiqueta_carrera = CTK.CTkLabel(pantalla_validacion_carrera, text="Seleccionar carrera")
#        etiqueta_carrera.grid(row=0, column=0, padx=10)
#        desplegable_carrera = CTK.CTkComboBox(pantalla_validacion_carrera, values=["Ingeniería","Diseño"], state="readonly")
#        desplegable_carrera.set("Ingeniería")
#        desplegable_carrera.grid(row=0, column=1, padx=10)
#        boton_buscar_carrera = CTK.CTkButton(pantalla_validacion_carrera, text="🔍", font=(None,20), width=28, command=mostar_estudiantes_boton)
#        boton_buscar_carrera.grid(row=0, column=2, padx=10)
#