import csv
import customtkinter as CTK
import Objetos
import Pagina_Inicial
   
class Metodos_Estudiantes:
    # Lee ambos archivos .csv donde se almancenan los estudiantes.
    def lector_csv_estudiantes(self, adicionar_uno=True, modificar=False):
        def adicionar_estudiante_csv():
            self.Estudiantes_ingenieria_csv = open("PracticaFinal/Estudiantes_Ingenieria.csv", "a+", newline="", encoding='utf-8')
            self.Estudiantes_ingenieria_csv.seek(0)
            self.Lector_Ingenieria = csv.reader(self.Estudiantes_ingenieria_csv)
            self.Escritor_Ingenieria = csv.writer(self.Estudiantes_ingenieria_csv)
            self.cedulas_estudiantes_ingenieria_lista = []
            self.estudiantes_ingenieria_lista = []
            
            # Extrae el indice 0 y crea un lista con los valores extraidos, (lista de cédulas de ingenieria)
            for estudiante in self.Lector_Ingenieria:
                cedula, nombre, apellido, telefono, semestre, promedio, estado, serial = estudiante
                self.cedulas_estudiantes_ingenieria_lista.append(cedula)

            # Extrae toda la información del archivo, convierte los valores en objetos y crea un lista (lista de objetos de ingenieria)
                self.estudiantes_ingenieria_lista.append(Objetos.ESTUDIANTE_INGENIERIA(cedula, nombre, apellido, telefono, semestre, promedio, estado, serial))

            self.Estudiantes_diseno_csv = open("PracticaFinal/Estudiantes_Diseno.csv", "a+", newline="", encoding='utf-8')
            self.Estudiantes_diseno_csv.seek(0)
            self.Lector_Diseno = csv.reader(self.Estudiantes_diseno_csv)
            self.Escritor_Diseno = csv.writer(self.Estudiantes_diseno_csv)
            self.cedulas_estudiantes_diseno_lista = []
            self.estudiantes_diseno_lista = []

            # Extrae el indice 0 y crea un lista con los valores extraidos, (lista de cédulas de diseño)
            for estudiante in self.Lector_Diseno:
                cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, estado, serial = estudiante
                self.cedulas_estudiantes_diseno_lista.append(cedula)

            # Extrae toda la información del archivo, convierte los valores en objetos y crea un lista (lista de objetos de diseño)
                self.estudiantes_diseno_lista.append(Objetos.ESTUDIANTE_DISENO(cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, estado, serial))
                
        def modificar_csv_estudiante():
            with open("PracticaFinal/Estudiantes_Ingenieria.csv", "w", newline="", encoding='utf-8') as Estudiantes_ingenieria_csv:
                Escritor_Ingenieria = csv.writer(Estudiantes_ingenieria_csv)
                for estudiante in self.estudiantes_ingenieria_lista:
                    self.Escritor_Ingenieria.writerow(estudiante.convertir_lista())

            with open("PracticaFinal/Estudiantes_Diseno.csv", "w", newline="", encoding='utf-8') as Estudiantes_diseno_csv:
                Escritor_Diseno = csv.writer(Estudiantes_diseno_csv)
                for estudiante in self.estudiantes_diseno_lista:
                    Escritor_Diseno.writerow(estudiante.convertir_lista())
        
        if adicionar_uno:
            adicionar_estudiante_csv()
        elif modificar:
            modificar_csv_estudiante()


    def registrar_estudiantes_validacion_carrera(self,ventana_registro_estudiantes):

        self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas de cédulas u objetos

        def usar_paneles_para_registro():
            self.paneles_segun_carrera(self.ventana_registro_estudiantes,self.desplegable_carrera.get())
            self.frame_validacion_carrera.destroy()
            # Boton validación de datos ingresados y posterior registro si es el caso.
            self.boton_validacion = CTK.CTkButton(self.frame_eleccion_carrera, text="Registrar", command=self.realizar_registro, width=170)
            self.boton_validacion.grid(row=7,column=0, columnspan=2,pady=5,padx=10)
            self.etiqueta_excepciones = CTK.CTkLabel(self.frame_eleccion_carrera,height=15)

        # Consulta de tipo de carrera para posteriormente mostrar las opciones según corresponda.
        self.ventana_registro_estudiantes = CTK.CTkFrame(ventana_registro_estudiantes)
        self.ventana_registro_estudiantes.pack()
        self.frame_validacion_carrera = CTK.CTkFrame(self.ventana_registro_estudiantes,fg_color="transparent")
        self.frame_validacion_carrera.pack()
        self.etiqueta_carrera = CTK.CTkLabel(self.frame_validacion_carrera, text="¿Qué carrera está estudiando?")
        self.etiqueta_carrera.grid(row=0, column=0, columnspan=2,padx=20,pady=10)
        self.desplegable_carrera = CTK.CTkComboBox(self.frame_validacion_carrera, values=["Ingeniería","Diseño"], state="readonly",width=200, height=33)
        self.desplegable_carrera.set("Ingeniería")
        self.desplegable_carrera.grid(row=1, column=0, columnspan=2, padx=5)
        self.boton_carrera = CTK.CTkButton(self.frame_validacion_carrera, text="Continuar", command=usar_paneles_para_registro, width=170)
        self.boton_carrera.grid(row=2, column=0, columnspan=2, pady=10)            

    def paneles_segun_carrera(self, frame_para_paneles, carrera_elegida):
                
        self.frame_eleccion_carrera = CTK.CTkFrame(frame_para_paneles,fg_color="transparent")
        self.frame_eleccion_carrera.pack()
        self.eleccion_carrera = carrera_elegida

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
        self.etiqueta_telefono = CTK.CTkLabel(self.frame_eleccion_carrera, text="Teléfono")
        self.etiqueta_telefono.grid(row=4,column=0,pady=5,padx=10)
        self.entrada_telefono = CTK.CTkEntry(self.frame_eleccion_carrera)
        self.entrada_telefono.grid(row=4,column=1,pady=5,padx=10)

        # Se muestra las entradas específicas para todos los estudiantes según su carrera.
        if self.eleccion_carrera == "Ingeniería":
            
            self.etiqueta_carrera = CTK.CTkLabel(self.frame_eleccion_carrera, text=f"Registro estudiante: {self.eleccion_carrera}")
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

            self.etiqueta_carrera = CTK.CTkLabel(self.frame_eleccion_carrera, text=f"Registro estudiante: {self.eleccion_carrera}")
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
        
    # Función para validar datos ingresados y si es el caso el registro
    def realizar_registro(self):
        errores = self.validar_datos_registro()

        if errores:
            self.mostrar_errores_registro(errores)
        else:
            self.guardar_registro()

    # Validar datos ingresados en los entry y combobox
    def validar_datos_registro(self):
        lista_errores_registro = []
        
        # Validación de datos comunes.
        if not self.entrada_cedula.get():
            lista_errores_registro.append("Ingresar cédula.")
        if not self.entrada_nombre.get():
            lista_errores_registro.append("Ingresar nombre.")
        if not self.entrada_apellido.get():
            lista_errores_registro.append("Ingresar apellido.")
        if not self.entrada_telefono.get():
            lista_errores_registro.append("Ingresar teléfono.")
        
        # Validación de datos según carrera.
        if self.eleccion_carrera == "Ingeniería":
            
            if not self.entrada_promedio.get():
                lista_errores_registro.append("Ingresar promedio.")
            elif self.entrada_promedio.get():
                try:
                    float(self.entrada_promedio.get())
                except ValueError:
                    lista_errores_registro.append("Promedio: Valor ingresado no válido.")

        elif self.eleccion_carrera == "Diseño":
            
            if self.desplegable_modalidad.get() == "Seleccione":
                lista_errores_registro.append("Seleccione una modalidad de estudio.")
            if self.desplegable_cantidad_materias.get() == 0:
                lista_errores_registro.append("Seleccione la cantidad de materias.")

        return lista_errores_registro

    # Si hay errores, se mustra ventana (Toplevel) con mensajes
    def mostrar_errores_registro(self, lista_errores):
        lista_errores_registro = lista_errores

        if len(lista_errores_registro) > 0:
            self.ventana_errores_registro = CTK.CTkToplevel()
            self.ventana_errores_registro.focus()
            self.ventana_errores_registro.grab_set()
            self.ventana_errores_registro.geometry("270x150+300+100")
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
    def guardar_registro(self):
        self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas de cédulas u objetos

        cedula = self.entrada_cedula.get()
        nombre = self.entrada_nombre.get()
        apellido = self.entrada_apellido.get()
        telefono = self.entrada_telefono.get()
                
        if self.eleccion_carrera == "Ingeniería":                            
            semestre = self.desplegable_semestre.get()
            promedio = self.entrada_promedio.get()
            if cedula in self.cedulas_estudiantes_ingenieria_lista:
                self.etiqueta_excepciones.configure(text=f"El documento {cedula} ya existe en el sistema.", padx=10, pady=15)
                self.etiqueta_excepciones.grid(row=8,column=0, columnspan=2,pady=5,padx=10)
                self.entrada_cedula.configure(border_color="#FF5844")
                return
                
            registro = Objetos.ESTUDIANTE_INGENIERIA(cedula,nombre,apellido,telefono,semestre,promedio)
            self.Escritor_Ingenieria.writerow(registro.convertir_lista())
                    
        elif self.eleccion_carrera == "Diseño":
            modalidad = self.desplegable_modalidad.get()
            cantidad_materias = self.desplegable_cantidad_materias.get()

            if cedula in self.cedulas_estudiantes_diseno_lista:
                self.etiqueta_excepciones.configure(text=f"El documento {cedula} ya existe en el sistema.", padx=10, pady=15)
                self.etiqueta_excepciones.grid(row=8,column=0, columnspan=2,pady=5,padx=10)
                self.entrada_cedula.configure(border_color="#FF5844")
                return

            registro = Objetos.ESTUDIANTE_DISENO(cedula,nombre,apellido,telefono,modalidad,cantidad_materias)
            self.Escritor_Diseno.writerow(registro.convertir_lista())

        self.etiqueta_excepciones.configure(text="El registro se ha completado exitosamente.", padx=10, pady=15)
        self.etiqueta_excepciones.grid(row=8,column=0, columnspan=2,pady=5,padx=10)

        self.Estudiantes_ingenieria_csv.close()
        self.Estudiantes_diseno_csv.close()
        
    def busqueda_estudiantes(self,ventana_modificacion_estudiantes):
        self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas de cédulas u objetos
        self.ventana_modificacion_estudiantes = CTK.CTkFrame(ventana_modificacion_estudiantes)
        self.ventana_modificacion_estudiantes.pack()
        self.frame_validacion_carrera = CTK.CTkFrame(self.ventana_modificacion_estudiantes,fg_color="transparent")
        self.frame_validacion_carrera.pack()
        self.frame_mostrar_registro_busqueda = CTK.CTkFrame(self.ventana_modificacion_estudiantes,fg_color="transparent")

        self.etiqueta_id_busqueda = CTK.CTkLabel(self.frame_validacion_carrera, text="Id")
        self.etiqueta_id_busqueda.grid(row=0, column=0, padx=5, pady=10)
        self.entrada_id_busqueda = CTK.CTkEntry(self.frame_validacion_carrera)
        self.entrada_id_busqueda.grid(row=0, column=1, padx=5, pady=10)

        self.etiqueta_carrera_busqueda = CTK.CTkLabel(self.frame_validacion_carrera, text="Carrera")
        self.etiqueta_carrera_busqueda.grid(row=0, column=2, padx=5, pady=10)
        self.desplegable_carrera_busqueda = CTK.CTkComboBox(self.frame_validacion_carrera, values=["Ingeniería","Diseño"], state="readonly")
        self.desplegable_carrera_busqueda.set("Ingeniería")
        self.desplegable_carrera_busqueda.grid(row=0, column=3, padx=5, pady=10)
        self.boton_carrera_busqueda = CTK.CTkButton(self.frame_validacion_carrera, text="Buscar", command=self.buscar_registro_modificar)
        self.boton_carrera_busqueda.grid(row=0, column=4, padx=5, pady=10)
        self.etiqueta_excepciones = CTK.CTkLabel(self.frame_validacion_carrera,height=15)
        
    def buscar_registro_modificar(self):
        if self.frame_mostrar_registro_busqueda:
            for elementos in self.frame_mostrar_registro_busqueda.winfo_children():
                elementos.destroy()
                self.boton_guardar.destroy()
        self.entrada_id_busqueda.configure(border_color="gray")
        self.etiqueta_excepciones.configure(text="", padx=0, pady=0)        
        try:
            int(self.entrada_id_busqueda.get())
        except ValueError:
            self.entrada_id_busqueda.configure(border_color="#FF5844")
            self.etiqueta_excepciones.configure(text=f"Valor no valido", padx=10, pady=3)
            self.etiqueta_excepciones.grid(row=1, column=0, columnspan=5, padx=5)
            return
            
        cedula_busqueda = self.entrada_id_busqueda.get()
        carrera_busqueda = self.desplegable_carrera_busqueda.get()

        def activacion_estudiante():
            actualizar_datos_estudiante(actualizar=False, activar=True)
        
        if carrera_busqueda == "Ingeniería":
            if cedula_busqueda in self.cedulas_estudiantes_ingenieria_lista:
                for persona in self.estudiantes_ingenieria_lista:
                    if persona.cedula == cedula_busqueda:
                        if persona.estado == "ACTIVO":
                            self.frame_mostrar_registro_busqueda.pack()
                            self.paneles_segun_carrera(self.frame_mostrar_registro_busqueda,"Ingeniería")
                            self.entrada_cedula.insert(0,persona.cedula)
                            self.entrada_cedula.configure(state="readonly")
                            self.entrada_nombre.insert(0,persona.nombre)
                            self.entrada_apellido.insert(0,persona.apellido)
                            self.entrada_telefono.insert(0,persona.telefono)
                            self.desplegable_semestre.set(persona.semestre)
                            self.entrada_promedio.insert(0,persona.promedio)
                            self.desplegable_estado = CTK.CTkComboBox(self.frame_mostrar_registro_busqueda, values=["ACTIVO","INACTIVO"], state="readonly")
                            self.desplegable_estado.set(persona.estado)
                            self.desplegable_estado.pack()
                            break
                        else:
                            self.frame_mostrar_registro_busqueda.pack()
                            self.etiqueta_excepciones.configure(text=f"El documento {cedula_busqueda} se encuentra en estado INACTIVO.", padx=10, pady=3)
                            self.etiqueta_excepciones.grid(row=1, column=0, columnspan=5, padx=5)
                            CTK.CTkLabel(self.frame_mostrar_registro_busqueda, text=f"Cédula: {persona.cedula}").pack(pady=10)
                            self.desplegable_estado = CTK.CTkComboBox(self.frame_mostrar_registro_busqueda, values=["ACTIVO","INACTIVO"], state="readonly")
                            self.desplegable_estado.set(persona.estado)
                            self.desplegable_estado.pack(pady=10)
                            self.boton_guardar = CTK.CTkButton(self.frame_mostrar_registro_busqueda, text="Guardar cambios", command=activacion_estudiante)
                            self.boton_guardar.pack(pady=10)
                            return

            else:
                self.etiqueta_excepciones.configure(text=f"El documento {cedula_busqueda} no existe en el sistema.", padx=10, pady=3)
                self.etiqueta_excepciones.grid(row=1, column=0, columnspan=5, padx=5)
                return
        if carrera_busqueda == "Diseño":
            if cedula_busqueda in self.cedulas_estudiantes_diseno_lista:
                for persona in self.estudiantes_diseno_lista:
                    if persona.cedula == cedula_busqueda:
                        if persona.estado == "ACTIVO":
                            self.frame_mostrar_registro_busqueda.pack()
                            self.paneles_segun_carrera(self.frame_mostrar_registro_busqueda,"Diseño")
                            self.entrada_cedula.insert(0,persona.cedula)
                            self.entrada_nombre.insert(0,persona.nombre)
                            self.entrada_apellido.insert(0,persona.apellido)
                            self.entrada_telefono.insert(0,persona.telefono)
                            self.desplegable_modalidad.set(persona.modalidad)
                            self.desplegable_cantidad_materias.set(persona.cantidad_materias)
                            self.desplegable_estado = CTK.CTkComboBox(self.frame_mostrar_registro_busqueda, values=["ACTIVO","INACTIVO"], state="readonly")
                            self.desplegable_estado.set(persona.estado)
                            self.desplegable_estado.pack()
                            break
                        else:
                            self.frame_mostrar_registro_busqueda.pack()
                            self.etiqueta_excepciones.configure(text=f"El documento {cedula_busqueda} se encuentra en estado INACTIVO.", padx=10, pady=3)
                            self.etiqueta_excepciones.grid(row=1, column=0, columnspan=5, padx=5)
                            CTK.CTkLabel(self.frame_mostrar_registro_busqueda, text=f"Cédula: {persona.cedula}").pack(pady=10)
                            self.desplegable_estado = CTK.CTkComboBox(self.frame_mostrar_registro_busqueda, values=["ACTIVO","INACTIVO"], state="readonly")
                            self.desplegable_estado.set(persona.estado)
                            self.desplegable_estado.pack(pady=10)
                            self.boton_guardar = CTK.CTkButton(self.frame_mostrar_registro_busqueda, text="Guardar cambios", command=activacion_estudiante)
                            self.boton_guardar.pack(pady=10)
                            return

            else:
                self.etiqueta_excepciones.configure(text=f"El documento {cedula_busqueda} no existe en el sistema.", padx=10, pady=3)
                self.etiqueta_excepciones.grid(row=1, column=0, columnspan=5, padx=5)
                return
            
        def validacion_actualizar_datos_estudiante():
            errores = self.validar_datos_registro()

            if errores:
                self.mostrar_errores_registro(errores)
            else:
                actualizar_datos_estudiante()
            
        def actualizar_datos_estudiante(actualizar=True, activar=False):
            if actualizar:
                persona.cedula = self.entrada_cedula.get()
                persona.nombre = self.entrada_nombre.get()
                persona.apellido = self.entrada_apellido.get()
                persona.telefono = self.entrada_telefono.get()
                persona.estado = self.desplegable_estado.get()
                        
                if self.eleccion_carrera == "Ingeniería":
                    persona.semestre = self.desplegable_semestre.get()
                    persona.promedio = self.entrada_promedio.get()
                                            
                elif self.eleccion_carrera == "Diseño":
                    persona.modalidad = self.desplegable_modalidad.get()
                    persona.cantidad_materias = self.desplegable_cantidad_materias.get()
            elif activar:
                persona.estado = self.desplegable_estado.get()
                
            self.lector_csv_estudiantes(adicionar_uno=False, modificar=True)
            self.frame_mostrar_registro_busqueda.destroy()
            self.boton_guardar.destroy()

            self.etiqueta_excepciones.configure(text="Datos actualizados correctamente.", padx=10, pady=3)
            self.etiqueta_excepciones.grid(row=1, column=0, columnspan=5, padx=5)

            self.Estudiantes_ingenieria_csv.close()
            self.Estudiantes_diseno_csv.close()
        
        self.boton_guardar = CTK.CTkButton(self.frame_mostrar_registro_busqueda, text="Guardar cambios", command=validacion_actualizar_datos_estudiante)
        self.boton_guardar.pack(pady=10)
        
    def inactivar_estudiantes(self):
        pass
    
    def mostrar_estudiantes(self):
        self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas de cédulas u objetos
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