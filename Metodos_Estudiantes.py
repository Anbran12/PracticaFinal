import csv
import customtkinter as CTK
from Objetos import ESTUDIANTE_INGENIERIA, ESTUDIANTE_DISENO, ADMIN
from Generico import Utilidades
   
class Metodos_Estudiantes:
    def __init__(self, frame, datos_login=None):
        self.frame = frame
        self.datos_login = datos_login
        self.widgets = {}
        self.label_mensaje = None
        self.Ut = Utilidades()
        
        # Configuración de archivos
        self.configuracion_usuarios = self.Ut.configuracion_usuarios()
        
        # Configuración de campos
        self.config_campos = self.Ut.configuracion_campos_usuarios()

    def registrar_estudiante(self):
        self.Ut.limpiar_frame(self.frame)
        
        CTK.CTkLabel(self.frame, text="Registro de Estudiantes", font=("", 18, "bold")).pack(pady=5)
        
        pestanas = CTK.CTkTabview(self.frame, border_width=1, border_color="gray", height=300)
        pestanas.pack()
        
        pestanas.add("Usuarios")
        pestana_usuarios = pestanas.tab("Usuarios")
            
        # Selector de tipo
        tipo_usuarios = []
        for i in self.configuracion_usuarios.keys():
            if i != "Administrador":
                tipo_usuarios.append(i)

        if self.datos_login:
            if self.datos_login["rol"] == "Administrador":
                tipo_usuarios.append("Administrador")

        combo_tipo = CTK.CTkOptionMenu(pestana_usuarios, values=list(tipo_usuarios), width= 200,command=self.actualizar_campos, state="readonly")
        combo_tipo.set("Estudiante Ingeniería")
        combo_tipo.pack(pady=5)
        self.widgets["tipo"] = combo_tipo
        
        # Campos comunes
        self.widgets["identificacion"] = self.Ut.crear_campo(pestana_usuarios,"identificacion",self.config_campos)
        self.widgets["nombre"] = self.Ut.crear_campo(pestana_usuarios,"nombre",self.config_campos)
        self.widgets["apellido"] = self.Ut.crear_campo(pestana_usuarios,"apellido",self.config_campos)
        self.widgets["telefono"] = self.Ut.crear_campo(pestana_usuarios,"telefono",self.config_campos)
        
        # Campos específicos
        self.widgets["semestre"] = self.Ut.crear_campo(pestana_usuarios,"semestre",self.config_campos)
        self.widgets["promedio"] = self.Ut.crear_campo(pestana_usuarios,"promedio",self.config_campos)
        self.widgets["modalidad"] = self.Ut.crear_campo(pestana_usuarios,"modalidad",self.config_campos)
        self.widgets["cantidad_asignaturas"] = self.Ut.crear_campo(pestana_usuarios,"cantidad_asignaturas",self.config_campos)
                
        self.actualizar_campos()
        
        CTK.CTkButton(self.frame, text="Guardar usuario", command=self.guardar_usuario,font=("", 12, "bold"), width=170).pack(pady=5)
    
    def actualizar_campos(self, seleccion=None):
        """Habilita/deshabilita campos según el tipo"""
        tipo_seleccionado = self.widgets["tipo"].get()
        
        # Campos específicos por tipo
        if tipo_seleccionado == "Estudiante Ingeniería":
            self.widgets["telefono"].configure(state="normal")
            self.widgets["semestre"].configure(state="readonly")
            self.widgets["promedio"].configure(state="normal")
            self.widgets["modalidad"].configure(state="disabled")
            self.widgets["cantidad_asignaturas"].configure(state="disabled")

        elif tipo_seleccionado == "Estudiante Diseño":
            self.widgets["telefono"].configure(state="normal")
            self.widgets["semestre"].configure(state="disabled")
            self.widgets["promedio"].configure(state="disabled")
            self.widgets["modalidad"].configure(state="readonly")
            self.widgets["cantidad_asignaturas"].configure(state="readonly")

        elif tipo_seleccionado == "Administrador":
            self.widgets["telefono"].configure(state="disabled")
            self.widgets["semestre"].configure(state="disabled")
            self.widgets["promedio"].configure(state="disabled")
            self.widgets["modalidad"].configure(state="disabled")
            self.widgets["cantidad_asignaturas"].configure(state="disabled")

    def guardar_usuario(self):
        """Guarda el usuario nuevo"""
        try:
            tipo_seleccionado = self.widgets["tipo"].get()
            datos_usuario = {}

            # Obtener datos de campos comunes
            for campo in ["identificacion", "nombre", "apellido"]:
                datos_usuario[campo] = self.widgets[campo].get()
                if not self.Ut.validar_campo(self.frame, datos_usuario[campo], campo, self.config_campos, self.config_campos[campo]["longitud"]):
                    return
            # Obtener datos específicos según tipo
            if tipo_seleccionado == "Estudiante Ingeniería":
                for campo in ["telefono", "promedio"]:
                    datos_usuario[campo] = self.widgets[campo].get()
                    if not self.Ut.validar_campo(self.frame, datos_usuario[campo], campo, self.config_campos, self.config_campos[campo]["longitud"]):
                        return
                for campo in ["semestre"]:
                    datos_usuario[campo] = self.widgets[campo].get()

            elif tipo_seleccionado == "Estudiante Diseño":
                for campo in ["telefono"]:
                    datos_usuario[campo] = self.widgets[campo].get()
                    if not self.Ut.validar_campo(self.frame, datos_usuario[campo], campo, self.config_campos, self.config_campos[campo]["longitud"]):
                        return
                for campo in ["modalidad", "cantidad_asignaturas"]:
                    datos_usuario[campo] = self.widgets[campo].get()

            # Verificar serial duplicado
            if self.Ut.identificador_existe(self.frame, datos_usuario["identificacion"], self.configuracion_usuarios):
                self.Ut.mostrar_mensaje(self.frame, "✗ Ya existe un usuario con este id", "red")
                return

            # Crear objeto usuario
            if tipo_seleccionado == "Estudiante Ingeniería":
                nuevo_usuario = ESTUDIANTE_INGENIERIA(datos_usuario["identificacion"], datos_usuario["nombre"], datos_usuario["apellido"], datos_usuario["telefono"], datos_usuario["semestre"], datos_usuario["promedio"], estado="ACTIVO")
            elif tipo_seleccionado == "Estudiante Diseño":
                nuevo_usuario = ESTUDIANTE_DISENO(datos_usuario["identificacion"], datos_usuario["nombre"], datos_usuario["apellido"], datos_usuario["telefono"], datos_usuario["modalidad"], datos_usuario["cantidad_asignaturas"], estado="ACTIVO")
            elif tipo_seleccionado == "Administrador":
                nuevo_usuario = ADMIN(datos_usuario["identificacion"], datos_usuario["nombre"], datos_usuario["apellido"], estado="ACTIVO")

            # Guardar
            nombre_archivo, encabezados = self.configuracion_usuarios[tipo_seleccionado]    
            self.Ut.escribir_csv(self.frame, nuevo_usuario, nombre_archivo, encabezados)
            self.Ut.mostrar_mensaje(self.frame, "✓ Usuario guardado correctamente", "green")
            self.limpiar_formulario()

        except Exception as error:
            self.Ut.mostrar_mensaje(self.frame, f"✗ Error al guardar: {str(error)}", "red")

    def limpiar_formulario(self):
        """Limpia el formulario después de guardar"""
        for clave, widget in self.widgets.items():
            if clave != "tipo" and hasattr(widget, "delete"):
                widget.configure(state="normal")
                widget.delete(0, "end")
        self.widgets["tipo"].set("Estudiante Ingeniería")
        self.actualizar_campos()
                    
    # =================== MOSTRAR USUARIOS ===================
    
    def mostrar_usuarios(self):
        """Muestra todos los usuarios"""
        self.Ut.limpiar_frame(self.frame)
        
        contenedor_principal = CTK.CTkTabview(self.frame, border_width=1, border_color="gray")
        contenedor_principal.pack()
        
        contenedor_secundario = {}
        for tipo in self.configuracion_usuarios.keys():
            contenedor_secundario[tipo] = contenedor_principal.add(tipo)
                
        fila_actual = 0
        hay_usuarios = False
        
        for tipo_usuario, (nombre_archivo, encabezados) in self.configuracion_usuarios.items():
            datos_usuarios = self.Ut.leer_csv(self.frame, nombre_archivo)
            contenedor = contenedor_secundario[tipo_usuario]
            if not datos_usuarios:
                continue
            
            hay_usuarios = True
            
            # Título del tipo
            CTK.CTkLabel(contenedor, text=f"📊 {tipo_usuario}", font=("Arial", 14, "bold"),text_color="#4CAF50").grid(row=fila_actual, column=0, columnspan=len(encabezados),pady=(8, 5), sticky="w")
            fila_actual += 1
            
            # Configurar columnas
            for columna in range(len(encabezados)):
                contenedor.grid_columnconfigure(columna, weight=1, minsize=87)
            
            # Encabezados
            for columna, campo in enumerate(encabezados):
                if campo not in ["rol"]:
                    nombre_campo = self.formatear_campo(campo)
                    CTK.CTkLabel(contenedor, text=nombre_campo, font=("Arial", 10, "bold"),text_color="white", fg_color="#2E2E2E", width=90, height=40).grid(row=fila_actual, column=columna, padx=1, pady=1, sticky="nsew")
            fila_actual += 1
            
            # Datos
            for indice_usuario, usuario in enumerate(datos_usuarios):
                color_fila = "#3A3A3A" if indice_usuario % 2 == 0 else "#2A2A2A"
                
                for columna, campo in enumerate(encabezados):
                    valor_campo = usuario.get(campo, "N/A")
                    if campo not in ["rol"]:
                        # Formatear valores especiales
                        if campo == "estado":
                            color_fila = "#4CAF50" if valor_campo.lower() == "activo" else "#F44336"
                        
                        CTK.CTkLabel(contenedor, text=str(valor_campo), font=("Arial", 9),text_color="white", fg_color=color_fila, width=90, height=40,wraplength=85).grid(row=fila_actual, column=columna, padx=1, pady=0, sticky="nsew")
                
                fila_actual += 1
                    
        if not hay_usuarios:
            CTK.CTkLabel(contenedor, text="📋 No hay usuarios registrados", font=("Arial", 14),text_color="#888888").grid(row=0, column=0, pady=30)
        
        # Botón actualizar
        CTK.CTkButton(self.frame, text="🔄 Actualizar", command=self.mostrar_usuarios,font=("Arial", 10, "bold"), width=120, height=28).pack(pady=8)

    def formatear_campo(self, nombre_campo):
        """Formatea nombres de campos para mostrar"""

        formatos_campos = {
            "identificacion": "ID",
            "telefono": "Teléfono",
            "cantidad_asignaturas": "C. asignaturas"}

        return formatos_campos.get(nombre_campo, nombre_campo.title())

    # =================== MODIFICAR USUARIOS ===================
    
    def modificar_usuario(self):
        """Inicia modificación de usuario"""
        self.Ut.limpiar_frame(self.frame)
        
        CTK.CTkLabel(self.frame, text="Modificar usuario", font=("", 18, "bold")).pack(pady=15)
        CTK.CTkLabel(self.frame, text="Ingrese la identificación del usuario:", font=("", 12)).pack(pady=5)
        
        entrada_identificacion = CTK.CTkEntry(self.frame, placeholder_text="Identificación (máx 15 caracteres)", width=200)
        entrada_identificacion.pack(pady=10)
        
        # Validación de longitud
        def validar_serial(evento):
            if len(entrada_identificacion.get()) > 15:
                entrada_identificacion.delete(15, "end")
                self.Ut.mostrar_mensaje(self.frame, "⚠ Identificación limitado a 15 caracteres", "orange")
        entrada_identificacion.bind("<KeyRelease>", validar_serial)
        
        frame_botones = CTK.CTkFrame(self.frame)
        frame_botones.pack(pady=15)
        
        CTK.CTkButton(frame_botones, text="Buscar usuario",command=lambda: self.buscar_usuario(entrada_identificacion.get().strip())).pack(side="left", padx=5)
        CTK.CTkButton(frame_botones, text="Limpiar",command=lambda: entrada_identificacion.delete(0, "end")).pack(side="left", padx=5)

    def buscar_usuario(self, identificacion_buscar, tipo_rol="Administrador"):
        """Busca un usuario por identificación"""
        if not identificacion_buscar:
            self.Ut.mostrar_mensaje(self.frame, "✗ Ingrese un número de identificación", "red")
            return
        
        if len(identificacion_buscar) < 3 or len(identificacion_buscar) > 15:
            self.Ut.mostrar_mensaje(self.frame, "✗ La identificación debe tener entre 3 y 15 caracteres", "red")
            return
        
        for tipo_usuario, (nombre_archivo, encabezados) in self.configuracion_usuarios.items():
            lista_usuarios = self.Ut.leer_csv(self.frame, nombre_archivo)
            for indice, usuario in enumerate(lista_usuarios):
                if usuario.get("identificacion", "").strip().lower() == identificacion_buscar.lower():
                    self.mostrar_formulario_modificacion(usuario, lista_usuarios, nombre_archivo, encabezados, indice, tipo_usuario, tipo_rol)
                    return
        
        self.Ut.mostrar_mensaje(self.frame, "✗ Usuario no encontrado", "red")

    def mostrar_formulario_modificacion(self, usuario_encontrado, lista_usuarios, nombre_archivo, encabezados, indice_usuario, tipo_usuario, tipo_rol):
        """Muestra formulario de modificación"""
        self.Ut.limpiar_frame(self.frame)
        
        CTK.CTkLabel(self.frame, text=f"Datos personales: {usuario_encontrado["identificacion"]}", font=("", 18, "bold")).pack(pady=10)
        CTK.CTkLabel(self.frame, text=f"Tipo: {tipo_usuario}", font=("", 14, "bold"), text_color="lightblue").pack(pady=5)
        
        frame_campos = CTK.CTkFrame(self.frame)
        frame_campos.pack()
        
        entradas_campos = {}
        
        for campo in encabezados:
            if tipo_rol == "Administrador":        
                if campo in ["identificacion", "estado"]:
                    entrada_campo = self.Ut.crear_campo(frame_campos, campo, self.config_campos, usuario_encontrado[campo])
                    entradas_campos[campo] = entrada_campo
        
            if campo not in ["identificacion","estado","serial","rol"]:
                entrada_campo = self.Ut.crear_campo(frame_campos, campo, self.config_campos, usuario_encontrado[campo])
                entradas_campos[campo] = entrada_campo
        
        frame_botones_mod = CTK.CTkFrame(self.frame)
        frame_botones_mod.pack(pady=20)
        
        CTK.CTkButton(frame_botones_mod, text="Guardar Cambios",command=lambda: self.guardar_modificacion(usuario_encontrado, lista_usuarios, nombre_archivo, encabezados, indice_usuario, entradas_campos, tipo_usuario, tipo_rol),font=("", 12, "bold")).pack(side="left", padx=5)
        if tipo_rol == "Administrador":
            CTK.CTkButton(frame_botones_mod, text="Cancelar",command=self.modificar_usuario).pack(side="left", padx=5)

    def guardar_modificacion(self, usuario_original, lista_usuarios, nombre_archivo, encabezados, indice_usuario, entradas_campos, tipo_usuario, tipo_rol):
        """Guarda las modificaciones"""
        try:
            
            # Actualizar datos
            for campo, entrada in entradas_campos.items():
                if tipo_rol == "Administrador":
                    if campo in ["identificacion", "estado"]:
                        lista_usuarios[indice_usuario][campo] = entrada.get().strip()
                    if lista_usuarios[indice_usuario]["estado"].lower() == "inactivo":
                        if nombre_archivo in ["Estudiantes_ingenieria.csv", "Estudiantes_diseno.csv"]:
                            lista_usuarios[indice_usuario]["serial"] = ""
        
                if campo not in ["identificacion","estado","serial","rol"]:
                    lista_usuarios[indice_usuario][campo] = entrada.get().strip()
            
            # Escribir archivo
            with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=encabezados)
                escritor.writeheader()
                escritor.writerows(lista_usuarios)
            
            # Mostrar éxito
            self.Ut.limpiar_frame(self.frame)
            CTK.CTkLabel(self.frame, text=f"✓ Usuario {usuario_original["identificacion"]} modificado correctamente",font=("", 16, "bold"), text_color="green").pack(pady=20)
            if tipo_rol == "Administrador":
                CTK.CTkButton(self.frame, text="Modificar usuario",command=self.modificar_usuario, font=("", 12, "bold")).pack(padx=10)
            
        except Exception as error:
            self.Ut.mostrar_mensaje(self.frame, f"✗ Error al guardar: {str(error)}", "red")