import customtkinter as CTK
import Metodos_Estudiantes,Metodos_Equipos,Metodos_Prestamos,Objetos,csv
from Generico import Utilidades


class PANTALLA_PRINCIPAL:
    def __init__(self):
        CTK.set_appearance_mode("dark")
        CTK.set_default_color_theme("dark-blue")
        self.pagina_inicial = CTK.CTk()
        self.pagina_inicial.geometry("+500+150")
        self.pagina_inicial.resizable(False,False)
        self.pagina_inicial.iconbitmap("user.ico")
        self.Ut = Utilidades()
        self.mensaje_error = None
        self.pantalla_login()

        self.configuracion_usuarios = self.Ut.configuracion_usuarios()
        
        # Configuración de campos
        self.config_campos = {
            "identificacion": {"label": "No. Identificación", "Tipo": "Entry", "placeholder": "No. Identificación", "longitud": 15, "tipo_dato": "numero"},
        }

    def buscar_usuario(self, identificacion_buscar):
        for tipo_usuario, (nombre_archivo, encabezados) in self.configuracion_usuarios.items():
            lista_usuarios = self.Ut.leer_csv(self.Frame_Contenedor_Principal, nombre_archivo)
            for indice, usuario in enumerate(lista_usuarios):
                if usuario.get("identificacion", "").strip().lower() == identificacion_buscar.lower():
                    return tipo_usuario, usuario
        return False, False

    def boton_volver_login(self):
        self.pagina_inicial.iconbitmap("user.ico")
        for elemento in self.pagina_inicial.winfo_children():
            elemento.destroy()
        self.pagina_inicial.geometry("370x230")
        self.pantalla_login()

    def mostrar_mensaje(self, frame, mensaje, color="white"):
        """Muestra un mensaje en la interfaz"""
        if self.mensaje_error:
            self.mensaje_error.destroy()
        self.mensaje_error = CTK.CTkLabel(frame, text=mensaje, height=15, wraplength=250, text_color=color)
        self.mensaje_error.grid(row=2,column=0)
        frame.update_idletasks()
            
    def pantalla_login(self):
        def registrar_estudiante():
            self.pagina_inicial.geometry("370x500")
            self.pagina_inicial.iconbitmap("user.ico")
            self.frame_pantalla_busqueda.destroy()
            self.Frame_Contenedor_Principal.pack(side="left", pady=10, padx=10, fill="both", expand=True)
            objeto_registro_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes(self.Frame_Contenedor_Principal)
            objeto_registro_estudiantes.registrar_estudiante()
            boton_volver_iniciar_sesion = CTK.CTkButton(self.Frame_Contenedor_Principal, text="Volver al inicio", command=self.boton_volver_login, width=170, font=("", 12, "bold"))
            boton_volver_iniciar_sesion.pack()

        def login_validacion():

            identificacion_busqueda = self.entrada_busqueda.get()

            try:
                int(identificacion_busqueda)
            except ValueError:
                self.entrada_busqueda.configure(border_color="red")
                self.mostrar_mensaje(self.frame_pantalla_busqueda, f"✗ Valor no valido", "red")
                return

            tipo_usuario, datos_usuario = self.buscar_usuario(identificacion_busqueda)

            if tipo_usuario and datos_usuario:
                if datos_usuario.get("estado", "") == "INACTIVO":
                    self.entrada_busqueda.configure(border_color="gray")
                    self.mostrar_mensaje(self.frame_pantalla_busqueda, f"✗ El usuario {identificacion_busqueda} se encuentra inactivo, contacte al administrador", "red")
                    return
                else:
                    self.pagina_inicial.title("EQUIPOS ELECTRÓNICOS SAN JUAN DE DIOS")
                    self.frame_pantalla_busqueda.destroy()
                    if tipo_usuario in ["Estudiante Ingeniería","Estudiante Diseño"]:
                        self.menu_estudiantes(datos_usuario, tipo_usuario)
                    elif tipo_usuario == "Administrador":
                        self.menu_administrador(datos_usuario, tipo_usuario)
            else:
                self.entrada_busqueda.configure(border_color="gray")
                self.mostrar_mensaje(self.frame_pantalla_busqueda, f"✗ Usuario no existe", "red")
                
        self.frame_pantalla_busqueda = CTK.CTkFrame(self.pagina_inicial, border_width=1)
        self.frame_pantalla_busqueda.pack(pady=20, padx=20, ipady=5)
        
        self.pagina_inicial.title("Inicial sesión")
        self.etiqueta_busqueda = CTK.CTkLabel(self.frame_pantalla_busqueda, text="Inicial sesión", font=(None,26))
        self.etiqueta_busqueda.grid(row=0,column=0,pady=10, padx=10)

        self.entrada_busqueda = CTK.CTkEntry(self.frame_pantalla_busqueda,placeholder_text="Número de identificación",justify="center",font=(None,15),width=300,height=33)
        self.entrada_busqueda.grid(row=1,column=0,pady=5, padx=10)

        self.boton_busqueda = CTK.CTkButton(self.frame_pantalla_busqueda, text="Iniciar sesión", font=(None,15), command=login_validacion,width=300,height=33)
        self.boton_busqueda.grid(row=3,column=0,pady=5, padx=10)
        
        self.boton_salir_busqueda = CTK.CTkButton(self.frame_pantalla_busqueda, text="Registrarse", font=(None,15), command=registrar_estudiante,width=300,height=33)
        self.boton_salir_busqueda.grid(row=4,column=0,pady=5, padx=10)
                
        self.Frame_Botonera_Izquierda = CTK.CTkFrame(self.pagina_inicial,fg_color="transparent",width=150)
        self.Frame_Contenedor_Principal = CTK.CTkScrollableFrame(self.pagina_inicial)

        def validar_longitud(evento):
            if len(self.entrada_busqueda.get()) > 15:
                self.entrada_busqueda.delete(15, "end")
            try:
                int(self.entrada_busqueda.get())
            except ValueError:
                i = len(self.entrada_busqueda.get())
                self.entrada_busqueda.delete(i-1, "end")
        self.entrada_busqueda.bind("<KeyRelease>", validar_longitud)
    
    def menu_estudiantes(self, informacion_estudiante_login=None, carrera_estudiante_login=None):
        self.pagina_inicial.iconbitmap("usergen.ico")
        self.pagina_inicial.geometry("800x500")
        identificacion = informacion_estudiante_login.get("identificacion", "")
        def limpiar_contenedor():
            for elemento in self.Frame_Contenedor_Principal.winfo_children():
                elemento.destroy()
        def modificar_estudiantes():
            limpiar_contenedor()
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes(self.Frame_Contenedor_Principal, informacion_estudiante_login)
            objeto_estudiantes.buscar_usuario(identificacion, "Estudiante")
        def mostrar_equipos():
            limpiar_contenedor()
            objeto_equipos = Metodos_Equipos.Metodos_Equipos(self.Frame_Contenedor_Principal)
            objeto_equipos.mostrar_equipos()
        def registrar_prestamos():
            limpiar_contenedor()
            objeto_prestamos = Metodos_Prestamos.Metodos_Prestamos(self.Frame_Contenedor_Principal)
            objeto_prestamos.buscar_usuario_equipo(identificacion, "Estudiante")
            
        self.Frame_Botonera_Izquierda.pack(side="left", ipady=10, ipadx=10, fill="y", expand=False)
        self.Frame_Contenedor_Principal.pack(side="left", pady=10, padx=10, fill="both", expand=True)
                
        etiqueta_nombre = CTK.CTkLabel(self.Frame_Botonera_Izquierda, text=f"Hola {informacion_estudiante_login.get("nombre","")}",font=(None, 15))
        etiqueta_nombre.pack(pady=3, padx=10)
        etiqueta_menu = CTK.CTkLabel(self.Frame_Botonera_Izquierda, text="Panel de control",font=(None, 15))
        etiqueta_menu.pack(pady=5, padx=10)
        boton_modificar_estudiantes = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Datos personales", command=modificar_estudiantes)
        boton_modificar_estudiantes.pack(pady=3, padx=10)
        boton_mostrar_equipos = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Equipos", command=mostrar_equipos)
        boton_mostrar_equipos.pack(pady=3, padx=10)
        boton_registrar_prestamos = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Prestamos", command=registrar_prestamos)
        boton_registrar_prestamos.pack(pady=3, padx=10)
        boton_volver_iniciar_sesion = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Cerrar sesión", command=self.boton_volver_login)
        boton_volver_iniciar_sesion.pack(pady=3, padx=10)
                
    def menu_administrador(self, informacion_estudiante_login=None, carrera_estudiante_login=None):
        self.pagina_inicial.iconbitmap("useradd.ico")
        self.pagina_inicial.geometry("800x500")
        identificacion = informacion_estudiante_login.get("identificacion", "")
        
        def limpiar_contenedor():
            for elemento in self.Frame_Contenedor_Principal.winfo_children():
                elemento.destroy()
        def registrar_estudiantes():
            limpiar_contenedor()
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes(self.Frame_Contenedor_Principal, informacion_estudiante_login)
            objeto_estudiantes.registrar_estudiante()
        def modificar_estudiantes():
            limpiar_contenedor()
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes(self.Frame_Contenedor_Principal)
            objeto_estudiantes.modificar_usuario()
        def mostrar_estudiantes():
            limpiar_contenedor()
            objeto_estudiantes = Metodos_Estudiantes.Metodos_Estudiantes(self.Frame_Contenedor_Principal)
            objeto_estudiantes.mostrar_usuarios()
        def registrar_equipos():
            limpiar_contenedor()
            objeto_equipos = Metodos_Equipos.Metodos_Equipos(self.Frame_Contenedor_Principal)
            objeto_equipos.registrar_equipo()
        def modificar_equipos():
            limpiar_contenedor()
            objeto_equipos = Metodos_Equipos.Metodos_Equipos(self.Frame_Contenedor_Principal)
            objeto_equipos.modificar_equipo()
        def mostrar_equipos():
            limpiar_contenedor()
            objeto_equipos = Metodos_Equipos.Metodos_Equipos(self.Frame_Contenedor_Principal)
            objeto_equipos.mostrar_equipos()

        def modificar_prestamos():
            limpiar_contenedor()
            objeto_prestamos = Metodos_Prestamos.Metodos_Prestamos(self.Frame_Contenedor_Principal, informacion_estudiante_login)
            objeto_prestamos.modificar_prestamo()
    
        def mostrar_prestamos():
            limpiar_contenedor()
            objeto_prestamos = Metodos_Prestamos.Metodos_Prestamos(self.Frame_Contenedor_Principal)
            objeto_prestamos.mostrar_prestamos()
            
        self.Frame_Botonera_Izquierda.pack(side="left", ipady=10, ipadx=10, fill="y", expand=False)
        self.Frame_Contenedor_Principal.pack(side="left", pady=10, padx=10, fill="both", expand=True)

        etiqueta_nombre = CTK.CTkLabel(self.Frame_Botonera_Izquierda, text=f"Hola {informacion_estudiante_login.get("nombre","")}",font=(None, 15))
        etiqueta_nombre.pack(pady=3, padx=10)
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
        boton_modificar_prestamos = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Realizar/Modificar\nprestamos", command=modificar_prestamos)
        boton_modificar_prestamos.pack(pady=3, padx=10)
        boton_mostrar_prestamos = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Mostrar prestamos", command=mostrar_prestamos)
        boton_mostrar_prestamos.pack(pady=3, padx=10)
        boton_volver_iniciar_sesion = CTK.CTkButton(self.Frame_Botonera_Izquierda, text="Cerrar sesión", command=self.boton_volver_login)
        boton_volver_iniciar_sesion.pack(pady=3, padx=10) 

