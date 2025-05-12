import customtkinter as CTK
import Metodos_Estudiantes,Metodos_Equipos,Metodos_Prestamos

class PANTALLA_PRINCIPAL:
    def __init__(self):
        self.pagina_inicial = CTK.CTk()
        self.pagina_inicial.geometry("+300+100")
        self.pantalla_login()
    
    def pantalla_login(self):
        objeto_lector_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
        objeto_lector_estudiantes.lector_csv_estudiantes() # Ejecución de método lector para usar las listas
        def registrar_estudiante():
            objeto_registro_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
            objeto_registro_estudiantes.registrar_estudiantes_validacion_carrera()
        def login_validacion():
            cedula_busqueda = self.entrada_busqueda.get()
            try:
                cedula_busqueda = int(cedula_busqueda)
            except ValueError:
                self.entrada_busqueda.configure(border_color="#FF5844")
                self.etiqueta_busqueda_error.configure(text="Valor no valido")
                return
            if cedula_busqueda == 1234:
                # Falta validación en CSV -----------------------------------------------------------------------------
                self.pagina_inicial.title("EQUIPOS ELECTRÓNICOS SAN JUAN DE DIOS")
                self.frame_pantalla_busqueda.destroy()
                self.menu_administrador()
            else:
                self.entrada_busqueda.configure(border_color="gray")
                self.etiqueta_busqueda_error.configure(text="Usuario no existe")
                self.etiqueta_busqueda_error.grid(row=2,column=0)

        self.frame_pantalla_busqueda = CTK.CTkFrame(self.pagina_inicial, border_width=1)
        self.frame_pantalla_busqueda.pack(pady=20, padx=20, ipady=5, anchor="center")
        
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
        
        objeto_lector_estudiantes.Estudiantes_ingenieria_csv.close()
        objeto_lector_estudiantes.Estudiantes_diseno_csv.close()
        
        self.frame_botonera_izquierda = CTK.CTkFrame(self.pagina_inicial)
        self.frame_panel_principal = CTK.CTkFrame(self.pagina_inicial)
        
    def menu_estudiantes(self):
        def modificacion_estudiantes():
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
            objeto_estudiantes.modificar_estudiantes()
        def registrar_prestamos():
            objeto_prestamos = Metodos_Prestamos.Metodos_Prestamos()
            objeto_prestamos.registrar_prestamo()

        self.frame_botonera_izquierda.grid(row=1, column=0, pady=10, padx=10, ipady=10, ipadx=10)
        self.frame_panel_principal.grid(row=1, column=1)
        
        boton_modificacion_datos = CTK.CTkButton(self.frame_botonera_izquierda, text="Modificar", command=modificacion_estudiantes)
        boton_modificacion_datos.pack()
        boton_prestamo_equipos = CTK.CTkButton(self.frame_botonera_izquierda, text="Prestar equipo", command=registrar_prestamos)
        boton_prestamo_equipos.pack()
                
    def menu_administrador(self):
        def registrar_estudiantes():
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
            objeto_estudiantes.registrar_estudiantes_validacion_carrera()
        def modificacion_estudiantes():
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
            objeto_estudiantes.modificar_estudiantes()
        def inactivar_estudiantes():
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
            objeto_estudiantes.inactivar_estudiantes()       
        def mostrar_estudiantes():
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes()
            objeto_estudiantes.mostrar_estudiantes()
        def registrar_equipos():
            objeto_equipos = Metodos_Equipos.Metodos_Equipos()
            objeto_equipos.registrar_equipo()
        def registrar_prestamos():
            objeto_prestamos = Metodos_Prestamos.Metodos_Prestamos()
            objeto_prestamos.registrar_prestamo()

        self.frame_botonera_izquierda.grid(row=1, column=0, pady=10, padx=10, ipady=10, ipadx=10)
        self.frame_panel_principal.grid(row=1, column=1)
                
        etiqueta_menu = CTK.CTkLabel(self.frame_botonera_izquierda, text="Panel de control",font=(None, 15))
        etiqueta_menu.pack(pady=5, padx=10)
        boton_registar_estudiantes = CTK.CTkButton(self.frame_botonera_izquierda, text="Registar estudiantes", command=registrar_estudiantes)
        boton_registar_estudiantes.pack(pady=3, padx=10)
        boton_modificar_datos = CTK.CTkButton(self.frame_botonera_izquierda, text="Modificar datos", command=modificacion_estudiantes)
        boton_modificar_datos.pack(pady=3, padx=10)
        boton_inactivar_estudiantes = CTK.CTkButton(self.frame_botonera_izquierda, text="Inactivar estudiantes", command=inactivar_estudiantes)
        boton_inactivar_estudiantes.pack(pady=3, padx=10)
        boton_mostrar_estudiantes = CTK.CTkButton(self.frame_botonera_izquierda, text="Mostrar estudiantes", command=mostrar_estudiantes)
        boton_mostrar_estudiantes.pack(pady=3, padx=10)
        boton_registrar_equipos = CTK.CTkButton(self.frame_botonera_izquierda, text="Registrar equipos", command=registrar_equipos)
        boton_registrar_equipos.pack(pady=3, padx=10)
        boton_registrar_prestamos = CTK.CTkButton(self.frame_botonera_izquierda, text="Registrar prestamos", command=registrar_prestamos)
        boton_registrar_prestamos.pack(pady=3, padx=10)

#        self.Frame_Estudiantes_Principal = Metodos_Estudiantes.Metodos_Estudiantes(self.frame_panel_principal)
#        self.Frame_Prestamos_Principal = Metodos_Prestamos.Metodos_Prestamos(self.frame_panel_principal)
#        self.Frame_Equipos_Principal = Metodos_Equipos.Metodos_Equipos(self.frame_panel_principal)
