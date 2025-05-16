import csv
import customtkinter as CTK
import Objetos
import Pagina_Inicial
   
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
            cedula, nombre, apellido, telefono, semestre, promedio, estado, serial = estudiante
            self.estudiantes_ingenieria_lista.append(Objetos.ESTUDIANTE_INGENIERIA(cedula, nombre, apellido, telefono, semestre, promedio, estado, serial))
                
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
            cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, estado, serial = registro
            self.estudiantes_diseno_lista.append(Objetos.ESTUDIANTE_DISENO(cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, estado, serial))

    def registrar_estudiantes_validacion_carrera(self,ventana_registro_estudiantes):
            
        self.lector_csv_estudiantes()
        self.ventana_registro_estudiantes = CTK.CTkFrame(ventana_registro_estudiantes)
        self.ventana_registro_estudiantes.pack()
        self.frame_validacion_carrera = CTK.CTkFrame(self.ventana_registro_estudiantes)
        self.frame_validacion_carrera.pack()
        self.etiqueta_carrera = CTK.CTkLabel(self.frame_validacion_carrera, text="¿Qué carrera está estudiando?")
        self.etiqueta_carrera.grid(row=0, column=0, columnspan=2,padx=20,pady=10)
        self.desplegable_carrera = CTK.CTkComboBox(self.frame_validacion_carrera, values=["Ingeniería","Diseño"], state="readonly",width=200, height=33)
        self.desplegable_carrera.set("Ingeniería")
        self.desplegable_carrera.grid(row=1, column=0, columnspan=2, padx=5)
        self.boton_carrera = CTK.CTkButton(self.frame_validacion_carrera, text="Continuar", command=self.registro_segun_eleccion_carrera, width=170)
        self.boton_carrera.grid(row=2, column=0, columnspan=2, pady=10)

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
        
        self.boton_validacion = CTK.CTkButton(self.frame_eleccion_carrera, text="Registrar", command=self.validacion_errores_registro, width=170)
        self.boton_validacion.grid(row=7,column=0, columnspan=2,pady=5,padx=10)

            
    def validacion_errores_registro(self):
        self.ventana_errores_registro = CTK.CTkToplevel()
        self.ventana_errores_registro.focus()
        self.ventana_errores_registro.grab_set()
        self.ventana_errores_registro.geometry("270x150+300+100")
        self.ventana_errores_registro.resizable(False,False)
        self.frame_errores_registro = CTK.CTkScrollableFrame(self.ventana_errores_registro,width=250)
        self.lista_errores_registro = []
        self.mensaje_error = CTK.CTkLabel(self.ventana_errores_registro, text="", wraplength=245)
        self.mensaje_error.pack(padx=10)
        
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
            self.mensaje_error.configure(text="Inconsistencias detectadas:")
            self.frame_errores_registro.pack(pady=5,padx=10)
            for numero, elemento in enumerate(self.lista_errores_registro):
                CTK.CTkLabel(self.frame_errores_registro, text=f"{numero+1}. {elemento}", justify="left", anchor="w",wraplength=225).pack(padx=5,anchor="w")
            return

        else:
            if self.eleccion_carrera == "Ingeniería":
                self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas
                cedula = self.entrada_cedula.get()
                nombre = self.entrada_nombre.get()
                apellido = self.entrada_apellido.get()
                telefono = self.entrada_telefono.get()
                semestre = self.desplegable_semestre.get()
                promedio = self.entrada_promedio.get()
                registro_no_existe = True
                            
                for registro_actual in self.cedulas_estudiantes_ingenieria_lista:
                    if registro_actual == self.entrada_cedula.get():
                        self.mensaje_error.configure(text=f"El documento {cedula} ya existe en el sistema.")
                        registro_no_existe = False
                        break
                if registro_no_existe:
                    registro = Objetos.ESTUDIANTE_INGENIERIA(cedula,nombre,apellido,telefono,semestre,promedio)
                    self.Escritor_Ingenieria.writerow(registro.convertir_lista())
                    self.mensaje_error.configure(text="El registro se ha completado exitosamente.", pady=55)
                
                elif len(self.cedulas_estudiantes_ingenieria_lista) == 0:
                    registro = Objetos.ESTUDIANTE_INGENIERIA(cedula,nombre,apellido,telefono,semestre,promedio)
                    self.Escritor_Ingenieria.writerow(registro.convertir_lista())
                    self.mensaje_error.configure(text="El registro se ha completado exitosamente.", pady=55)
                        
            elif self.eleccion_carrera == "Diseño":
                self.lector_csv_estudiantes() # Ejecución de método lector para usar las listas
                cedula = self.entrada_cedula.get()
                nombre = self.entrada_nombre.get()
                apellido = self.entrada_apellido.get()
                telefono = self.entrada_telefono.get()
                modalidad = self.desplegable_modalidad.get()
                cantidad_materias = self.desplegable_cantidad_materias.get()
                registro_no_existe = True

                for registro_actual in self.cedulas_estudiantes_diseno_lista:
                    if registro_actual == self.entrada_cedula.get():
                        self.mensaje_error.configure(text=f"El documento {cedula} ya existe en el sistema.")
                        registro_no_existe = False
                        break
                if registro_no_existe:
                    registro = Objetos.ESTUDIANTE_DISENO(cedula,nombre,apellido,telefono,modalidad,cantidad_materias)
                    self.Escritor_Diseno.writerow(registro.convertir_lista())
                    self.mensaje_error.configure(text="El registro se ha completado exitosamente.", pady=55)
                    
                if len(self.cedulas_estudiantes_diseno_lista) == 0:
                    registro = Objetos.ESTUDIANTE_DISENO(cedula,nombre,apellido,telefono,modalidad,cantidad_materias)
                    self.Escritor_Diseno.writerow(registro.convertir_lista())
                    self.mensaje_error.configure(text="El registro se ha completado exitosamente.", pady=55)

        self.Estudiantes_ingenieria_csv.close()
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