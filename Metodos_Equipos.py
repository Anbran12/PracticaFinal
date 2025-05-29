import csv
import customtkinter as CTK
from Objetos import COMPUTADOR_PORTATIL, TABLETA_GRAFICA

class Metodos_Equipos:
    def __init__(self, frame):
        self.frame = frame
        self.widgets = {}
        self.label_mensaje = None
        
        # Configuración de archivos
        self.config_archivos = {
            "Computador Portátil": ("Computadores_Portatiles.csv",
                                   ['serial', 'marca', 'tamano', 'precio', 'sistema_operativo', 'procesador', 'estado']),
            "Tableta Gráfica": ("Tabletas_Graficas.csv",
                              ['serial', 'marca', 'tamano', 'precio', 'almacenamiento', 'peso', 'estado'])
        }
        
        # Configuración de campos
        self.config_campos = {
            "serial": {"label": "Serial", "placeholder": "Número de serie (máximo 12 caracteres)"},
            "marca": {"label": "Marca", "placeholder": "Ej: Dell, HP (máximo 12 caracteres)"},
            "tamano": {"label": "Tamaño", "placeholder": "Ej: 15.6, 10.8 (máximo 12 caracteres)", "tipo": "numero"},
            "precio": {"label": "Precio", "placeholder": "Precio en pesos (máximo 12 caracteres)", "tipo": "numero"},
            "sistema_operativo": {"label": "Sistema Operativo", "placeholder": "Ej: Windows 11 (máximo 12 caracteres)"},
            "procesador": {"label": "Procesador", "placeholder": "Ej: Intel i5 (máximo 12 caracteres)"},
            "almacenamiento": {"label": "Almacenamiento", "placeholder": "Ej: 64 GB (máximo 12 caracteres)"},
            "peso": {"label": "Peso", "placeholder": "Ej: 350 (máximo 12 caracteres)", "tipo": "numero"}
        }

    # =================== UTILIDADES ===================
    
    def limpiar_frame(self):
        """Limpia todos los widgets del frame"""
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.label_mensaje = None
        self.widgets = {}

    def mostrar_mensaje(self, mensaje, color="white"):
        """Muestra un mensaje en la interfaz"""
        if self.label_mensaje:
            self.label_mensaje.destroy()
        self.label_mensaje = CTK.CTkLabel(self.frame, text=mensaje, text_color=color)
        self.label_mensaje.pack(pady=5)
        self.frame.update_idletasks()

    def leer_csv(self, nombre_archivo):
        """Lee un archivo CSV"""
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                return list(csv.DictReader(archivo))
        except FileNotFoundError:
            return []
        except Exception as error:
            self.mostrar_mensaje(f"✗ Error al leer archivo: {error}", "red")
            return []

    def escribir_csv(self, equipo, nombre_archivo, encabezados):
        """Escribe un equipo al CSV"""
        try:
            # Verificar si el archivo necesita headers
            archivo_existe = False
            try:
                with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                    archivo_existe = archivo.read(1) != ''
            except FileNotFoundError:
                pass

            with open(nombre_archivo, 'a', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                if not archivo_existe:
                    escritor.writerow(encabezados)

                if isinstance(equipo, COMPUTADOR_PORTATIL):
                    escritor.writerow(equipo.convertir_lista_computador())
                elif isinstance(equipo, TABLETA_GRAFICA):
                    escritor.writerow(equipo.convertir_lista_tableta())

        except Exception as error:
            self.mostrar_mensaje(f"✗ Error al escribir CSV: {error}", "red")

    def validar_campo(self, valor, clave_campo):
        """Valida un campo según su configuración"""
        valor = valor.strip()
        
        # Validar vacío
        if not valor:
            self.mostrar_mensaje(f"✗ El campo {self.config_campos[clave_campo]['label']} es obligatorio", "red")
            return False
        
        # Validar longitud
        if len(valor) > 12:
            self.mostrar_mensaje(f"✗ {self.config_campos[clave_campo]['label']} no puede exceder 12 caracteres", "red")
            return False
        
        # Validar números
        if self.config_campos[clave_campo].get("tipo") == "numero":
            try:
                numero = float(valor)
                if numero <= 0:
                    self.mostrar_mensaje(f"✗ {self.config_campos[clave_campo]['label']} debe ser mayor a 0", "red")
                    return False
            except ValueError:
                self.mostrar_mensaje(f"✗ {self.config_campos[clave_campo]['label']} debe ser un número válido", "red")
                return False
        
        return True

    def crear_campo(self, clave_campo, valor_inicial=""):
        """Crea un campo de entrada con validación"""
        configuracion = self.config_campos[clave_campo]
        
        CTK.CTkLabel(self.frame, text=configuracion["label"] + ":").pack(pady=5)
        entrada = CTK.CTkEntry(self.frame, placeholder_text=configuracion["placeholder"])
        if valor_inicial:
            entrada.insert(0, valor_inicial)
        entrada.pack(pady=5)
        
        # Validación de longitud en tiempo real
        def validar_longitud(evento):
            if len(entrada.get()) > 12:
                entrada.delete(12, 'end')
                self.mostrar_mensaje(f"⚠ {configuracion['label']} limitado a 12 caracteres", "orange")
        
        entrada.bind('<KeyRelease>', validar_longitud)
        return entrada

    def serial_existe(self, serial, excluir_serial=None):
        """Verifica si un serial ya existe"""
        serial = serial.strip().lower()
        for tipo_equipo, (nombre_archivo, encabezados) in self.config_archivos.items():
            lista_equipos = self.leer_csv(nombre_archivo)
            for equipo in lista_equipos:
                serial_equipo = equipo.get('serial', '').strip().lower()
                if serial_equipo == serial and serial_equipo != (excluir_serial or "").lower():
                    return True
        return False

    # =================== REGISTRO ===================
    
    def registrar_equipo(self):
        """Formulario para registrar nuevo equipo"""
        self.limpiar_frame()
        
        CTK.CTkLabel(self.frame, text="Registro de Equipo", font=("", 18, "bold")).pack(pady=10)
        
        # Selector de tipo
        CTK.CTkLabel(self.frame, text="Tipo de Equipo:", font=("", 12, "bold")).pack(pady=5)
        combo_tipo = CTK.CTkComboBox(self.frame, values=list(self.config_archivos.keys()),
                                command=self.actualizar_campos, state="readonly")
        combo_tipo.set("Computador Portátil")
        combo_tipo.pack(pady=5)
        self.widgets["tipo"] = combo_tipo
        
        # Campos comunes
        self.widgets["serial"] = self.crear_campo("serial")
        self.widgets["marca"] = self.crear_campo("marca")
        self.widgets["tamano"] = self.crear_campo("tamano")
        self.widgets["precio"] = self.crear_campo("precio")
        
        # Campos específicos
        self.widgets["sistema_operativo"] = self.crear_campo("sistema_operativo")
        self.widgets["procesador"] = self.crear_campo("procesador")
        self.widgets["almacenamiento"] = self.crear_campo("almacenamiento")
        self.widgets["peso"] = self.crear_campo("peso")
        
        self.actualizar_campos()
        
        CTK.CTkButton(self.frame, text="Guardar Equipo", command=self.guardar_equipo,
                     font=("", 12, "bold")).pack(pady=15)

    def actualizar_campos(self, seleccion=None):
        """Habilita/deshabilita campos según el tipo"""
        tipo_seleccionado = self.widgets["tipo"].get()
        
        # Campos específicos por tipo
        if tipo_seleccionado == "Computador Portátil":
            self.widgets["sistema_operativo"].configure(state="normal")
            self.widgets["procesador"].configure(state="normal")
            self.widgets["almacenamiento"].configure(state="disabled")
            self.widgets["peso"].configure(state="disabled")
            # Limpiar campos deshabilitados
            self.widgets["almacenamiento"].delete(0, 'end')
            self.widgets["peso"].delete(0, 'end')
        else:  # Tableta Gráfica
            self.widgets["sistema_operativo"].configure(state="disabled")
            self.widgets["procesador"].configure(state="disabled")
            self.widgets["almacenamiento"].configure(state="normal")
            self.widgets["peso"].configure(state="normal")
            # Limpiar campos deshabilitados
            self.widgets["sistema_operativo"].delete(0, 'end')
            self.widgets["procesador"].delete(0, 'end')

    def guardar_equipo(self):
        """Guarda el equipo nuevo"""
        try:
            tipo_seleccionado = self.widgets["tipo"].get()
            datos_equipo = {}
            
            # Obtener datos de campos comunes
            for campo in ["serial", "marca", "tamano", "precio"]:
                datos_equipo[campo] = self.widgets[campo].get()
                if not self.validar_campo(datos_equipo[campo], campo):
                    return
            
            # Obtener datos específicos según tipo
            if tipo_seleccionado == "Computador Portátil":
                for campo in ["sistema_operativo", "procesador"]:
                    datos_equipo[campo] = self.widgets[campo].get()
                    if not self.validar_campo(datos_equipo[campo], campo):
                        return
            else:  # Tableta Gráfica
                for campo in ["almacenamiento", "peso"]:
                    datos_equipo[campo] = self.widgets[campo].get()
                    if not self.validar_campo(datos_equipo[campo], campo):
                        return
            
            # Verificar serial duplicado
            if self.serial_existe(datos_equipo['serial']):
                self.mostrar_mensaje("✗ Ya existe un equipo con este serial", "red")
                return
            
            # Crear objeto equipo
            precio_equipo = float(datos_equipo['precio'])
            if tipo_seleccionado == "Computador Portátil":
                nuevo_equipo = COMPUTADOR_PORTATIL(
                    serial=datos_equipo['serial'], marca=datos_equipo['marca'], tamano=datos_equipo['tamano'],
                    precio=precio_equipo, sistema_operativo=datos_equipo['sistema_operativo'],
                    procesador=datos_equipo['procesador'], estado="Activo"
                )
            else:
                peso_equipo = float(datos_equipo['peso'])
                nuevo_equipo = TABLETA_GRAFICA(
                    serial=datos_equipo['serial'], marca=datos_equipo['marca'], tamano=datos_equipo['tamano'],
                    precio=precio_equipo, almacenamiento=datos_equipo['almacenamiento'],
                    peso=peso_equipo, estado="Activo"
                )
            
            # Guardar
            nombre_archivo, encabezados = self.config_archivos[tipo_seleccionado]
            self.escribir_csv(nuevo_equipo, nombre_archivo, encabezados)
            self.mostrar_mensaje("✓ Equipo guardado correctamente", "green")
            self.limpiar_formulario()
            
        except Exception as error:
            self.mostrar_mensaje(f"✗ Error al guardar: {str(error)}", "red")

    def limpiar_formulario(self):
        """Limpia el formulario después de guardar"""
        for clave, widget in self.widgets.items():
            if clave != "tipo" and hasattr(widget, 'delete'):
                widget.configure(state="normal")
                widget.delete(0, 'end')
        self.widgets["tipo"].set("Computador Portátil")
        self.actualizar_campos()

    # =================== MOSTRAR EQUIPOS ===================
    
    def MostrarEquipos(self):
        """Muestra todos los equipos"""
        self.limpiar_frame()
        
        contenedor_principal = CTK.CTkFrame(self.frame)
        contenedor_principal.pack(padx=15, pady=15, fill="both", expand=True)
        
        fila_actual = 0
        hay_equipos = False
        
        for tipo_equipo, (nombre_archivo, encabezados) in self.config_archivos.items():
            datos_equipos = self.leer_csv(nombre_archivo)
            if not datos_equipos:
                continue
            
            hay_equipos = True
            
            # Título del tipo
            CTK.CTkLabel(contenedor_principal, text=f"📊 {tipo_equipo}", font=("Arial", 14, "bold"),
                        text_color="#4CAF50").grid(row=fila_actual, column=0, columnspan=len(encabezados),
                                                  pady=(8, 5), sticky="w")
            fila_actual += 1
            
            # Configurar columnas
            for columna in range(len(encabezados)):
                contenedor_principal.grid_columnconfigure(columna, weight=1, minsize=90)
            
            # Encabezados
            for columna, campo in enumerate(encabezados):
                nombre_campo = self.formatear_campo(campo)
                CTK.CTkLabel(contenedor_principal, text=nombre_campo, font=("Arial", 10, "bold"),
                           text_color="white", fg_color="#2E2E2E", width=90, height=40
                ).grid(row=fila_actual, column=columna, padx=1, pady=1, sticky="nsew")
            fila_actual += 1
            
            # Datos
            for indice_equipo, equipo in enumerate(datos_equipos):
                color_fila = "#3A3A3A" if indice_equipo % 2 == 0 else "#2A2A2A"
                
                for columna, campo in enumerate(encabezados):
                    valor_campo = equipo.get(campo, "N/A")
                    
                    # Formatear valores especiales
                    if campo == "precio" and valor_campo != "N/A":
                        try:
                            valor_campo = f"${float(valor_campo):,.0f}"
                        except:
                            valor_campo = f"${valor_campo}"
                    elif campo == "estado":
                        color_fila = "#4CAF50" if valor_campo.lower() == "activo" else "#F44336"
                    
                    CTK.CTkLabel(contenedor_principal, text=str(valor_campo), font=("Arial", 9),
                               text_color="white", fg_color=color_fila, width=90, height=40,
                               wraplength=85
                    ).grid(row=fila_actual, column=columna, padx=1, pady=0, sticky="nsew")
                
                fila_actual += 1
            
            # Contador
            CTK.CTkLabel(contenedor_principal, text=f"Total: {len(datos_equipos)}", font=("Arial", 9, "italic"),
                        text_color="#888888").grid(row=fila_actual, column=0, columnspan=len(encabezados),
                                                  pady=(2, 8), sticky="w")
            fila_actual += 1
        
        if not hay_equipos:
            CTK.CTkLabel(contenedor_principal, text="📋 No hay equipos registrados", font=("Arial", 14),
                        text_color="#888888").grid(row=0, column=0, pady=30)
        
        # Botón actualizar
        CTK.CTkButton(self.frame, text="🔄 Actualizar", command=self.MostrarEquipos,
                     font=("Arial", 10, "bold"), width=120, height=28).pack(pady=8)

    def formatear_campo(self, nombre_campo):
        """Formatea nombres de campos para mostrar"""
        formatos_campos = {
            "tamano": "Tamaño",
            "sistema_operativo": "S.O.",
            "almacenamiento": "Almacen."
        }
        return formatos_campos.get(nombre_campo, nombre_campo.replace("_", " ").title())

    # =================== MODIFICAR EQUIPOS ===================
    
    def modificar_equipo(self):
        """Inicia modificación de equipo"""
        self.limpiar_frame()
        
        CTK.CTkLabel(self.frame, text="Modificar Equipo", font=("", 18, "bold")).pack(pady=15)
        CTK.CTkLabel(self.frame, text="Ingrese el serial del equipo:", font=("", 12)).pack(pady=5)
        
        entrada_serial = CTK.CTkEntry(self.frame, placeholder_text="Serial (máx 12 caracteres)", width=200)
        entrada_serial.pack(pady=10)
        
        # Validación de longitud
        def validar_serial(evento):
            if len(entrada_serial.get()) > 12:
                entrada_serial.delete(12, 'end')
                self.mostrar_mensaje("⚠ Serial limitado a 12 caracteres", "orange")
        entrada_serial.bind('<KeyRelease>', validar_serial)
        
        frame_botones = CTK.CTkFrame(self.frame)
        frame_botones.pack(pady=15)
        
        CTK.CTkButton(frame_botones, text="Buscar Equipo",
                     command=lambda: self.buscar_equipo(entrada_serial.get().strip())).pack(side="left", padx=5)
        CTK.CTkButton(frame_botones, text="Limpiar",
                     command=lambda: entrada_serial.delete(0, 'end')).pack(side="left", padx=5)

    def buscar_equipo(self, serial_buscar):
        """Busca un equipo por serial"""
        if not serial_buscar:
            self.mostrar_mensaje("✗ Ingrese un serial", "red")
            return
        
        if len(serial_buscar) < 3 or len(serial_buscar) > 12:
            self.mostrar_mensaje("✗ El serial debe tener entre 3 y 12 caracteres", "red")
            return
        
        for tipo_equipo, (nombre_archivo, encabezados) in self.config_archivos.items():
            lista_equipos = self.leer_csv(nombre_archivo)
            for indice, equipo in enumerate(lista_equipos):
                if equipo.get('serial', '').strip().lower() == serial_buscar.lower():
                    self.mostrar_formulario_modificacion(equipo, lista_equipos, nombre_archivo, encabezados, indice, tipo_equipo)
                    return
        
        self.mostrar_mensaje("✗ Equipo no encontrado", "red")

    def mostrar_formulario_modificacion(self, equipo_encontrado, lista_equipos, nombre_archivo, encabezados, indice_equipo, tipo_equipo):
        """Muestra formulario de modificación"""
        self.limpiar_frame()
        
        CTK.CTkLabel(self.frame, text=f"Modificando: {equipo_encontrado['serial']}", font=("", 18, "bold")).pack(pady=10)
        CTK.CTkLabel(self.frame, text=f"Tipo: {tipo_equipo}", font=("", 14, "bold"), text_color="lightblue").pack(pady=5)
        
        contenedor_scroll = CTK.CTkScrollableFrame(self.frame, width=600, height=400)
        contenedor_scroll.pack(padx=20, pady=10, fill="both", expand=True)
        
        entradas_campos = {}
        
        # Crear campos (excluir serial y estado)
        for campo in encabezados:
            if campo not in ['serial', 'estado']:
                configuracion = self.config_campos[campo]
                CTK.CTkLabel(contenedor_scroll, text=configuracion["label"] + ": *", font=("", 12, "bold")).pack(pady=(10, 2))
                entrada_campo = CTK.CTkEntry(contenedor_scroll, width=400, placeholder_text=configuracion["placeholder"])
                entrada_campo.insert(0, equipo_encontrado.get(campo, ''))
                entrada_campo.pack(pady=2)
                entradas_campos[campo] = entrada_campo
                
                # Validación de longitud
                def crear_validador(entrada, nombre_campo):
                    def validar(evento):
                        if len(entrada.get()) > 12:
                            entrada.delete(12, 'end')
                            self.mostrar_mensaje(f"⚠ {nombre_campo} limitado a 12 caracteres", "orange")
                    return validar
                entrada_campo.bind('<KeyRelease>', crear_validador(entrada_campo, configuracion["label"]))
        
        frame_botones_mod = CTK.CTkFrame(contenedor_scroll)
        frame_botones_mod.pack(pady=20)
        
        CTK.CTkButton(frame_botones_mod, text="Guardar Cambios",
                     command=lambda: self.guardar_modificacion(equipo_encontrado, lista_equipos, nombre_archivo, encabezados, indice_equipo, entradas_campos, tipo_equipo),
                     font=("", 12, "bold")).pack(side="left", padx=5)
        CTK.CTkButton(frame_botones_mod, text="Cancelar",
                     command=self.modificar_equipo).pack(side="left", padx=5)

    def guardar_modificacion(self, equipo_original, lista_equipos, nombre_archivo, encabezados, indice_equipo, entradas_campos, tipo_equipo):
        """Guarda las modificaciones"""
        try:
            # Validar todos los campos
            for campo, entrada in entradas_campos.items():
                valor_entrada = entrada.get().strip()
                if not self.validar_campo(valor_entrada, campo):
                    return
            
            # Actualizar datos
            for campo, entrada in entradas_campos.items():
                lista_equipos[indice_equipo][campo] = entrada.get().strip()
            
            # Escribir archivo
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=encabezados)
                escritor.writeheader()
                escritor.writerows(lista_equipos)
            
            # Mostrar éxito
            self.limpiar_frame()
            CTK.CTkLabel(self.frame, text="✓ Equipo modificado correctamente",
                        font=("", 16, "bold"), text_color="green").pack(pady=20)
            CTK.CTkLabel(self.frame, text=f"Equipo: {equipo_original['serial']}",
                        font=("", 12)).pack(pady=5)
            
            frame_botones_final = CTK.CTkFrame(self.frame)
            frame_botones_final.pack(pady=20)
            
            CTK.CTkButton(frame_botones_final, text="Modificar Otro",
                         command=self.modificar_equipo, font=("", 12, "bold")).pack(side="left", padx=10)
            CTK.CTkButton(frame_botones_final, text="Modificar Este Nuevamente",
                         command=lambda: self.buscar_equipo(equipo_original['serial']),
                         font=("", 12, "bold")).pack(side="left", padx=10)
            
        except Exception as error:
            self.mostrar_mensaje(f"✗ Error al guardar: {str(error)}", "red")