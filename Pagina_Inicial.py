import customtkinter as CTK
import Metodos_Estudiantes,Metodos_Equipos,Metodos_Prestamos

class PANTALLA_PRINCIPAL:
    def __init__(self):
        self.pagina_inicial = CTK.CTk()
        self.pagina_inicial.geometry("+500+150")
        self.pagina_inicial.resizable(False,False)
        self.pantalla_login()

    def boton_volver_login(self):
        for elemento in self.pagina_inicial.winfo_children():
            elemento.destroy()
        self.pagina_inicial.geometry("370x230")
        self.pantalla_login()
    
    def pantalla_login(self):
        objeto_lector_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
        objeto_lector_estudiantes.lector_csv_estudiantes() # Ejecución de método lector para usar las listas

        def registrar_estudiante():
            self.pagina_inicial.geometry("370x370")
            self.frame_pantalla_busqueda.destroy()
            self.Frame_Contenedor_Principal.pack(side="left", pady=10, padx=10, fill="both", expand=True)
            objeto_registro_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
            objeto_registro_estudiantes.registrar_estudiantes_validacion_carrera(self.Frame_Contenedor_Principal)
            boton_volver_iniciar_sesion = CTK.CTkButton(self.Frame_Contenedor_Principal, text="Volver al inicio", command=self.boton_volver_login, width=170)
            boton_volver_iniciar_sesion.pack()

        def login_validacion():
            cedula_busqueda = self.entrada_busqueda.get()
            try:
                int(cedula_busqueda)
            except ValueError:
                self.entrada_busqueda.configure(border_color="#FF5844")
                self.etiqueta_busqueda_error.configure(text="Valor no valido")
                self.etiqueta_busqueda_error.grid(row=2,column=0)
                return
            if cedula_busqueda == "1234":
                # Falta validación en CSV -----------------------------------------------------------------------------
                self.pagina_inicial.title("EQUIPOS ELECTRÓNICOS SAN JUAN DE DIOS")
                self.frame_pantalla_busqueda.destroy()
                self.menu_administrador()
            else:
                self.entrada_busqueda.configure(border_color="gray")
                self.etiqueta_busqueda_error.configure(text="Usuario no existe")
                self.etiqueta_busqueda_error.grid(row=2,column=0)

        self.frame_pantalla_busqueda = CTK.CTkFrame(self.pagina_inicial, border_width=1)
        self.frame_pantalla_busqueda.pack(pady=20, padx=20, ipady=5)
#        self.frame_pantalla_busqueda.pack(pady=20, padx=20, ipady=5, anchor="center")
        
        self.pagina_inicial.title("Inicial sesión")
        self.etiqueta_busqueda = CTK.CTkLabel(self.frame_pantalla_busqueda, text="Inicial sesión", font=(None,26))
        self.etiqueta_busqueda.grid(row=0,column=0,pady=10, padx=10)

        self.entrada_busqueda = CTK.CTkEntry(self.frame_pantalla_busqueda,placeholder_text="Número de identificación",justify="center",font=(None,15),width=300,height=33)
        self.entrada_busqueda.grid(row=1,column=0,pady=5, padx=10)

        self.etiqueta_busqueda_error = CTK.CTkLabel(self.frame_pantalla_busqueda,text="",height=15)

        self.boton_busqueda = CTK.CTkButton(self.frame_pantalla_busqueda, text="Iniciar sesión", font=(None,15), command=login_validacion,width=300,height=33)
        self.boton_busqueda.grid(row=3,column=0,pady=5, padx=10)
        
        self.boton_salir_busqueda = CTK.CTkButton(self.frame_pantalla_busqueda, text="Registrarse", font=(None,15), command=registrar_estudiante,width=300,height=33)
        self.boton_salir_busqueda.grid(row=4,column=0,pady=5, padx=10)
                
        self.Frame_Botonera_Izquierda = CTK.CTkFrame(self.pagina_inicial,fg_color="transparent",width=150)
        self.Frame_Contenedor_Principal = CTK.CTkScrollableFrame(self.pagina_inicial)
    

    def menu_estudiantes(self):
        self.pagina_inicial.geometry("800x500")
        def modificacion_estudiantes():
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
            objeto_estudiantes.modificar_estudiantes()
        def registrar_prestamos():
            objeto_prestamos = Metodos_Prestamos.Metodos_Prestamos()
            objeto_prestamos.registrar_prestamo()

        self.Frame_Botonera_Izquierda.grid(row=1, column=0, ipady=10, ipadx=10)
        
        boton_modificacion_datos = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Modificar", command=modificacion_estudiantes)
        boton_modificacion_datos.pack(pady=3, padx=10)
        boton_prestamo_equipos = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Prestar equipo", command=registrar_prestamos)
        boton_prestamo_equipos.pack(pady=3, padx=10)
        boton_volver_iniciar_sesion = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Volver al inicio", command=self.boton_volver_login)
        boton_volver_iniciar_sesion.pack(pady=3, padx=10)
                
    def menu_administrador(self):
        self.pagina_inicial.geometry("800x500")
        def limpiar_contenedor():
            for elemento in self.Frame_Contenedor_Principal.winfo_children():
                elemento.destroy()
        def registrar_estudiantes():
            limpiar_contenedor()
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
            objeto_estudiantes.registrar_estudiantes_validacion_carrera(self.Frame_Contenedor_Principal)
        def modificar_estudiantes():
            limpiar_contenedor()
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
            objeto_estudiantes.busqueda_estudiantes(self.Frame_Contenedor_Principal)
        def mostrar_estudiantes():
            limpiar_contenedor()
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
            objeto_estudiantes.mostrar_estudiantes(self.Frame_Contenedor_Principal)
        def registrar_equipos():
            limpiar_contenedor()
            objeto_equipos = Metodos_Equipos.Metodos_Equipos()
#            objeto_equipos.registrar_equipo()
        def modificar_equipos():
            limpiar_contenedor()
            objeto_equipos = Metodos_Equipos.Metodos_Equipos()
#            objeto_equipos.registrar_equipo()
        def mostrar_equipos():
            limpiar_contenedor()
            objeto_equipos = Metodos_Equipos.Metodos_Equipos()
#            objeto_equipos.registrar_equipo()
        def registrar_prestamos():
            limpiar_contenedor()
            objeto_prestamos = Metodos_Prestamos.Metodos_Prestamos()
#            objeto_prestamos.registrar_prestamo()
        def modificar_prestamos():
            limpiar_contenedor()
            objeto_prestamos = Metodos_Prestamos.Metodos_Prestamos()
#            objeto_prestamos.registrar_prestamo()
        def mostrar_prestamos():
            limpiar_contenedor()
            objeto_prestamos = Metodos_Prestamos.Metodos_Prestamos()
#            objeto_prestamos.registrar_prestamo()

        self.Frame_Botonera_Izquierda.pack(side="left", ipady=10, ipadx=10, fill="y", expand=False)
        self.Frame_Contenedor_Principal.pack(side="left", pady=10, padx=10, fill="both", expand=True)

#        self.Frame_Botonera_Izquierda.grid(row=1, column=0, ipady=10, ipadx=10)
#        self.Frame_Contenedor_Principal.grid(row=1, column=1, pady=10, padx=10)
                
        etiqueta_menu = CTK.CTkLabel(self.Frame_Botonera_Izquierda, text="Panel de control",font=(None, 15))
        etiqueta_menu.pack(pady=5, padx=10)
        boton_registar_estudiantes = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Registar estudiantes", command=registrar_estudiantes)
        boton_registar_estudiantes.pack(pady=3, padx=10)
        boton_modificar_estudiantes = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Modificar estudiantes", command=modificar_estudiantes)
        boton_modificar_estudiantes.pack(pady=3, padx=10)
        boton_mostrar_estudiantes = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Mostrar estudiantes", command=mostrar_estudiantes)
        boton_mostrar_estudiantes.pack(pady=3, padx=10)
        boton_registrar_equipos = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Registrar equipos", command=registrar_equipos)
        boton_registrar_equipos.pack(pady=3, padx=10)
        boton_modificar_equipos = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Modificar equipos", command=modificar_equipos)
        boton_modificar_equipos.pack(pady=3, padx=10)
        boton_mostrar_equipos = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Mostrar equipos", command=mostrar_equipos)
        boton_mostrar_equipos.pack(pady=3, padx=10)
        boton_registrar_prestamos = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Registrar prestamos", command=registrar_prestamos)
        boton_registrar_prestamos.pack(pady=3, padx=10)
        boton_modificar_prestamos = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Modificar prestamos", command=modificar_prestamos)
        boton_modificar_prestamos.pack(pady=3, padx=10)
        boton_mostrar_prestamos = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Mostrar prestamos", command=mostrar_prestamos)
        boton_mostrar_prestamos.pack(pady=3, padx=10)
        boton_volver_iniciar_sesion = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Volver al inicio", command=self.boton_volver_login)
        boton_volver_iniciar_sesion.pack(pady=3, padx=10)

