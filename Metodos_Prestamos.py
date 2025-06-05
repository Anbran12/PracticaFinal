import csv
import customtkinter as CTK
from Objetos import ESTUDIANTE_INGENIERIA, ESTUDIANTE_DISENO, ADMIN
from Generico import Utilidades

class Metodos_Prestamos:
    
    def __init__(self, frame, datos_login=None):
        self.frame = frame
        self.datos_login = datos_login
        self.widgets = {}
        self.label_mensaje = None
        self.Ut = Utilidades()
        
        # Configuración de archivos
        self.configuracion_usuarios = self.Ut.configuracion_usuarios()
        self.configuracion_equipos = self.Ut.configuracion_equipos()
        
        # Configuración de campos
        self.config_campos_usuarios = self.Ut.configuracion_campos_usuarios()
        self.config_campos_equipos = self.Ut.configuracion_campos_equipos()

    # =================== MOSTRAR PRESTAMOS ===================
    
    def mostrar_prestamos(self):
        """Muestra todos los prestamos"""
        self.Ut.limpiar_frame(self.frame)
        
        contenedor_principal = CTK.CTkTabview(self.frame, border_width=1, border_color="gray")
        contenedor_principal.pack()
        
        contenedor_secundario = {}
        for tipo in self.configuracion_usuarios.keys():
            if tipo not in ["Administrador"]:
                contenedor_secundario[tipo] = contenedor_principal.add(tipo)
                
        fila_actual = 0
        hay_usuarios = False
        
        for tipo_usuario, (nombre_archivo, encabezados) in self.configuracion_usuarios.items():
            if tipo_usuario not in ["Administrador"]:
                datos_usuarios = self.Ut.leer_csv(self.frame, nombre_archivo)
                contenedor = contenedor_secundario[tipo_usuario]
                if not datos_usuarios:
                    continue
                
                hay_usuarios = True
                
                # Título del tipo
                CTK.CTkLabel(contenedor, text=f"📊 Prestamos {tipo_usuario}", font=("Arial", 14, "bold"),text_color="#4CAF50").grid(row=fila_actual, column=0, columnspan=len(encabezados),pady=(8, 5), sticky="w")
                fila_actual += 1
                
                excepciones = ["telefono", "semestre", "promedio", "modalidad", "cantidad_asignaturas", "estado", "rol"]
                
                # Configurar columnas
                for columna in range(len(encabezados)-len(excepciones)):
                    contenedor.grid_columnconfigure(columna, weight=1, minsize=90)
                
                # Encabezados
                for columna, campo in enumerate(encabezados):
                    if campo not in excepciones:
                        nombre_campo = self.formatear_campo(campo)
                        CTK.CTkLabel(contenedor, text=nombre_campo, font=("Arial", 10, "bold"),text_color="white", fg_color="#2E2E2E", width=90, height=40).grid(row=fila_actual, column=columna, padx=1, pady=1, sticky="nsew")
                    else:
                        columna -=1
                fila_actual += 1
                
                # Datos
                indice_usuario_no_aplica = 0                
                for indice_usuario, usuario in enumerate(datos_usuarios):
                    color_fila = "#3A3A3A" if (indice_usuario - indice_usuario_no_aplica) % 2 == 0 else "#2A2A2A"
                    
                    if usuario.get("serial","") != "":
                        for columna, campo in enumerate(encabezados):
                            valor_campo = usuario.get(campo, "N/A")
                            if campo not in excepciones:
                                    CTK.CTkLabel(contenedor, text=str(valor_campo), font=("Arial", 9),text_color="white", fg_color=color_fila, width=90, height=40,wraplength=85).grid(row=fila_actual, column=columna, padx=1, pady=0, sticky="nsew")
                            else:
                                columna -=1
                        fila_actual += 1
                    else:
                        indice_usuario_no_aplica += 1
                        
        if not hay_usuarios:
            CTK.CTkLabel(contenedor, text="📋 No hay prestamos registrados", font=("Arial", 14),text_color="#888888").grid(row=0, column=0, pady=30)
        
        # Botón actualizar
        CTK.CTkButton(self.frame, text="🔄 Actualizar", command=self.mostrar_prestamos,font=("Arial", 10, "bold"), width=120, height=28).pack(pady=8)

    def formatear_campo(self, nombre_campo):
        """Formatea nombres de campos para mostrar"""

        formatos_campos = {
            "identificacion": "ID",
            "telefono": "Teléfono",
            "cantidad_asignaturas": "C. asignaturas"}

        return formatos_campos.get(nombre_campo, nombre_campo.title())

    # =================== MODIFICAR USUARIOS ===================
    
    def modificar_prestamo(self):
        """Inicia modificación de usuario"""
        self.Ut.limpiar_frame(self.frame)
        
        CTK.CTkLabel(self.frame, text="Prestamos", font=("", 18, "bold")).pack(pady=15)
        CTK.CTkLabel(self.frame, text="Ingrese la identificación o serial:", font=("", 12)).pack(pady=5)
        
        entrada_serial_identificacion = CTK.CTkEntry(self.frame, placeholder_text="Identificación o serial (máx 15 caracteres)", width=200)
        entrada_serial_identificacion.pack(pady=10)
        
        # Validación de longitud
        def validar_serial(evento):
            if len(entrada_serial_identificacion.get()) > 15:
                entrada_serial_identificacion.delete(15, "end")
                self.Ut.mostrar_mensaje(self.frame, "⚠ Identificación o serial limitado a 15 caracteres", "orange")
        entrada_serial_identificacion.bind("<KeyRelease>", validar_serial)
        
        frame_botones = CTK.CTkFrame(self.frame)
        frame_botones.pack(pady=15)
        
        CTK.CTkButton(frame_botones, text="Buscar",command=lambda: self.buscar_usuario_equipo(entrada_serial_identificacion.get().strip())).pack(side="left", padx=5)
        CTK.CTkButton(frame_botones, text="Limpiar",command=lambda: entrada_serial_identificacion.delete(0, "end")).pack(side="left", padx=5)

    def buscar_usuario_equipo(self, identificacion_buscar, tipo_rol="Administrador"):
        """Busca un usuario o equipo por identificación o serial"""
        if not identificacion_buscar:
            self.Ut.mostrar_mensaje(self.frame, "✗ Ingrese un número de identificación o serial", "red")
            return
        
        if len(identificacion_buscar) < 3 or len(identificacion_buscar) > 15:
            self.Ut.mostrar_mensaje(self.frame, "✗ La identificación o serial debe tener entre 3 y 15 caracteres", "red")
            return
        
        for tipo_usuario, (nombre_archivo, encabezados) in self.configuracion_usuarios.items():
            lista_usuarios = self.Ut.leer_csv(self.frame, nombre_archivo)
            for indice, usuario in enumerate(lista_usuarios):
                if usuario.get("identificacion", "").strip().lower() == identificacion_buscar.lower() or usuario.get("serial", "").strip().lower() == identificacion_buscar.lower():
                    if usuario.get("estado", "").strip().lower() == "activo":
                        self.mostrar_formulario_modificacion(usuario, lista_usuarios, nombre_archivo, encabezados, indice, tipo_usuario, tipo_rol)
                        return
                    else:
                        self.Ut.mostrar_mensaje(self.frame, f"✗ La identificación {identificacion_buscar} se encuentra en estado inactivo", "red")
                        return
        
        self.Ut.mostrar_mensaje(self.frame, "✗ Registro no encontrado", "red")

    def mostrar_formulario_modificacion(self, usuario_encontrado, lista_usuarios, nombre_archivo, encabezados, indice_usuario, tipo_usuario, tipo_rol):
        """Muestra formulario de modificación"""
        self.Ut.limpiar_frame(self.frame)
        
        CTK.CTkLabel(self.frame, text=f"Prestamo: {usuario_encontrado["identificacion"]}", font=("", 18, "bold")).pack(pady=10)
        CTK.CTkLabel(self.frame, text=f"Tipo: {tipo_usuario}", font=("", 14, "bold"), text_color="lightblue").pack(pady=5)
        
        frame_campos = CTK.CTkFrame(self.frame)
        frame_campos.pack()
        
        entradas_campos = {}
        
        for campo in encabezados:
            if campo in ["identificacion", "nombre", "apellido", "serial"]:
                entrada_campo = self.Ut.crear_campo(frame_campos, campo, self.config_campos_usuarios, usuario_encontrado[campo])
                entrada_campo.configure(state="readonly")
                entradas_campos[campo] = entrada_campo
                
        if tipo_usuario == "Administrador":
            self.Ut.mostrar_mensaje(self.frame, "✗ Usuario no apto para prestamos", "red")
            return
        elif tipo_usuario == "Estudiante Ingeniería":
            datos = self.Ut.leer_csv(self.frame, "Computadores_Portatiles.csv")
        else: # Estudiantes Diseño
            datos = self.Ut.leer_csv(self.frame, "Tabletas_Graficas.csv")
        
        prestados = []
        disponibles = []
                    
        for indice_equipo in range(len(datos)):
            if datos[indice_equipo]["estado"].lower() == "activo":
                disponibles.append(datos[indice_equipo].get("serial","").lower())
        for indice, usuario in enumerate(lista_usuarios):
            if usuario["serial"] != "":
                prestados.append(usuario.get("serial","N/A").lower())        
        
        disponibles = [i for i in disponibles if i not in prestados]
        
        entradas_campos["serial"].configure(values=disponibles)
        valor = "Seleccionar" if usuario_encontrado["serial"] == "" else usuario_encontrado["serial"]
        entradas_campos["serial"].set(valor)
                
        frame_botones_mod = CTK.CTkFrame(self.frame)
        frame_botones_mod.pack(pady=20)
        
        CTK.CTkButton(frame_botones_mod, text="Guardar Cambios",command=lambda: self.guardar_modificacion(usuario_encontrado, lista_usuarios, nombre_archivo, encabezados, indice_usuario, entradas_campos, tipo_usuario, tipo_rol, False),font=("", 12, "bold")).pack(side="left", padx=5)
        CTK.CTkButton(frame_botones_mod, text="Devolver equipo",command=lambda: self.guardar_modificacion(usuario_encontrado, lista_usuarios, nombre_archivo, encabezados, indice_usuario, entradas_campos, tipo_usuario, tipo_rol, True),font=("", 12, "bold")).pack(side="left", padx=5)
        if tipo_rol == "Administrador":
            CTK.CTkButton(frame_botones_mod, text="Cancelar",command=self.modificar_prestamo).pack(side="left", padx=5)

    def guardar_modificacion(self, usuario_original, lista_usuarios, nombre_archivo, encabezados, indice_usuario, entradas_campos, tipo_usuario, tipo_rol, devolver):
        """Guarda las modificaciones"""
        try:
            
            # Actualizar datos
            for campo, entrada in entradas_campos.items():
                if devolver and campo in ["serial"]:
                    entrada.set("")
                if campo in ["identificacion", "nombre", "apellido", "serial"]:
                    if entrada.get().lower() == "seleccionar":
                        self.Ut.mostrar_mensaje(self.frame, f"✗ Selecciona un equipo", "red")
                        return                        
                    else:
                        lista_usuarios[indice_usuario][campo] = entrada.get().strip()
                    
            # Escribir archivo
            with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=encabezados)
                escritor.writeheader()
                escritor.writerows(lista_usuarios)
            
            # Mostrar éxito
            self.Ut.limpiar_frame(self.frame)
            if devolver:
                CTK.CTkLabel(self.frame, text=f"✓ Devolución exitosa",font=("", 16, "bold"), text_color="green").pack(pady=20)                
            else:
                CTK.CTkLabel(self.frame, text=f"✓ Prestamo exitoso",font=("", 16, "bold"), text_color="green").pack(pady=20)
            if tipo_rol == "Administrador":
                CTK.CTkButton(self.frame, text="Modificar o realizar prestamo",command=self.modificar_prestamo, font=("", 12, "bold")).pack(padx=10)
            
        except Exception as error:
            self.Ut.mostrar_mensaje(self.frame, f"✗ Error al guardar: {str(error)}", "red")