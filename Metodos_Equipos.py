import csv
import customtkinter as CTK
from Objetos import COMPUTADOR_PORTATIL, TABLETA_GRAFICA
from Generico import Utilidades

class Metodos_Equipos:
    def __init__(self, frame):
        self.frame = frame
        self.widgets = {}
        self.label_mensaje = None
        self.Ut = Utilidades()
        
        # Configuración de archivos
        self.configuracion_equipos = self.Ut.configuracion_equipos()
        
        # Configuración de campos
        self.config_campos = self.Ut.configuracion_campos_equipos()

    # =================== REGISTRO ===================
    
    def registrar_equipo(self):
        """Formulario para registrar nuevo equipo"""
        self.Ut.limpiar_frame(self.frame)
        
        CTK.CTkLabel(self.frame, text="Registro de Equipo", font=("", 18, "bold")).pack(pady=5)

        pestanas = CTK.CTkTabview(self.frame, border_width=1, border_color="gray", height=300)
        pestanas.pack()
        
        pestanas.add("Equipos")
        pestana_equipos = pestanas.tab("Equipos")
        
        # Selector de tipo
        combo_tipo = CTK.CTkOptionMenu(pestana_equipos, values=list(self.configuracion_equipos.keys()), width= 200,command=self.actualizar_campos, state="readonly")
        combo_tipo.set("Computador Portátil")
        combo_tipo.pack(pady=5)
        self.widgets["tipo"] = combo_tipo
        
        # Campos comunes
        self.widgets["serial"] = self.Ut.crear_campo(pestana_equipos, "serial", self.config_campos)
        self.widgets["marca"] = self.Ut.crear_campo(pestana_equipos, "marca", self.config_campos)
        self.widgets["marca"].configure(state="readonly")
        self.widgets["tamano"] = self.Ut.crear_campo(pestana_equipos, "tamano", self.config_campos)
        self.widgets["precio"] = self.Ut.crear_campo(pestana_equipos, "precio", self.config_campos)
        
        # Campos específicos
        self.widgets["sistema operativo"] = self.Ut.crear_campo(pestana_equipos, "sistema operativo", self.config_campos)
        self.widgets["procesador"] = self.Ut.crear_campo(pestana_equipos, "procesador", self.config_campos)
        self.widgets["almacenamiento"] = self.Ut.crear_campo(pestana_equipos, "almacenamiento", self.config_campos)
        self.widgets["peso"] = self.Ut.crear_campo(pestana_equipos, "peso", self.config_campos)
        
        self.actualizar_campos()
        
        CTK.CTkButton(self.frame, text="Guardar Equipo", command=self.guardar_equipo, font=("", 12, "bold")).pack(pady=15)

    def actualizar_campos(self, seleccion=None):
        """Habilita/deshabilita campos según el tipo"""
        tipo_seleccionado = self.widgets["tipo"].get()
        
        # Campos específicos por tipo
        if tipo_seleccionado == "Computador Portátil":
            self.widgets["marca"].configure(values=["HP","Dell","Lenovo","ASUS","Acer","Apple","MSI","Samsung","Toshiba","Microsoft","Sony","LG","Huawei","Gateway"])
            self.widgets["marca"].set("HP")
            self.widgets["sistema operativo"].configure(state="readonly")
            self.widgets["procesador"].configure(state="readonly")
            self.widgets["almacenamiento"].configure(state="disabled")
            self.widgets["peso"].configure(state="disabled")
            # Limpiar campos deshabilitados
            self.widgets["peso"].delete(0, "end")
        else:  # Tableta Gráfica
            self.widgets["marca"].configure(values=["Wacom","Huion","XP-Pen","Gaomon","Veikk","Ugee","Parblo","Monoprice","Artisul","Bosto","Turcom"])
            self.widgets["marca"].set("Wacom")
            self.widgets["sistema operativo"].configure(state="disabled")
            self.widgets["procesador"].configure(state="disabled")
            self.widgets["almacenamiento"].configure(state="readonly")
            self.widgets["peso"].configure(state="normal")

    def guardar_equipo(self):
        """Guarda el equipo nuevo"""
        #try:
        tipo_seleccionado = self.widgets["tipo"].get()
        datos_equipo = {}
        
        # Obtener datos de campos comunes
        for campo in ["serial", "tamano", "precio"]:
            datos_equipo[campo] = self.widgets[campo].get()
            if not self.Ut.validar_campo(self.frame, datos_equipo[campo], campo, self.config_campos, self.config_campos[campo]["longitud"]):
                return
        for campo in ["marca"]:
            datos_equipo[campo] = self.widgets[campo].get()
        
        # Obtener datos específicos según tipo
        if tipo_seleccionado == "Computador Portátil":
            for campo in ["sistema operativo", "procesador"]:
                datos_equipo[campo] = self.widgets[campo].get()
        else:  # Tableta Gráfica
            for campo in ["peso"]:
                datos_equipo[campo] = self.widgets[campo].get()
                if not self.Ut.validar_campo(self.frame, datos_equipo[campo], campo, self.config_campos, self.config_campos[campo]["longitud"]):
                    return
            for campo in ["almacenamiento"]:
                datos_equipo[campo] = self.widgets[campo].get()
        
        # Verificar serial duplicado
        if self.Ut.identificador_existe(self.frame, datos_equipo["serial"], self.configuracion_equipos):
            self.Ut.mostrar_mensaje(self.frame, "✗ Ya existe un equipo con este serial", "red")
            return
        
        # Crear objeto equipo
        precio_equipo = float(datos_equipo["precio"])
        if tipo_seleccionado == "Computador Portátil":
            nuevo_equipo = COMPUTADOR_PORTATIL(serial=datos_equipo["serial"], marca=datos_equipo["marca"], tamano=datos_equipo["tamano"],precio=precio_equipo, sistema_operativo=datos_equipo["sistema operativo"],procesador=datos_equipo["procesador"], estado="ACTIVO")
        else:
            peso_equipo = float(datos_equipo["peso"])
            nuevo_equipo = TABLETA_GRAFICA(serial=datos_equipo["serial"], marca=datos_equipo["marca"], tamano=datos_equipo["tamano"],precio=precio_equipo, almacenamiento=datos_equipo["almacenamiento"],peso=peso_equipo, estado="ACTIVO")
        
        # Guardar
        nombre_archivo, encabezados = self.configuracion_equipos[tipo_seleccionado]
        self.Ut.escribir_csv(self.frame, nuevo_equipo, nombre_archivo, encabezados)
        self.Ut.mostrar_mensaje(self.frame, "✓ Equipo guardado correctamente", "green")
        self.limpiar_formulario()
        
        #except Exception as error:
        #    self.Ut.mostrar_mensaje(self.frame, f"✗ Error al guardar: {str(error)}", "red")

    def limpiar_formulario(self):
        """Limpia el formulario después de guardar"""
        for clave, widget in self.widgets.items():
            if clave != "tipo" and hasattr(widget, "delete"):
                widget.configure(state="normal")
                widget.delete(0, "end")
        self.widgets["tipo"].set("Computador Portátil")
        self.actualizar_campos()

    # =================== MOSTRAR EQUIPOS ===================
    
    def mostrar_equipos(self):
        """Muestra todos los equipos"""
        self.Ut.limpiar_frame(self.frame)
                
        contenedor_principal = CTK.CTkTabview(self.frame)
        contenedor_principal.pack()

        contenedor_secundario = {}
        for tipo in self.configuracion_equipos.keys():
            contenedor_secundario[tipo] = contenedor_principal.add(tipo)
        
        fila_actual = 0
        hay_equipos = False
        
        for tipo_equipo, (nombre_archivo, encabezados) in self.configuracion_equipos.items():
            datos_equipos = self.Ut.leer_csv(self.frame, nombre_archivo)
            contenedor = contenedor_secundario[tipo_equipo]
            if not datos_equipos:
                continue
            
            hay_equipos = True
            
            # Título del tipo
            CTK.CTkLabel(contenedor, text=f"📊 {tipo_equipo}", font=("Arial", 14, "bold"),text_color="#4CAF50").grid(row=fila_actual, column=0, columnspan=len(encabezados),pady=(8, 5), sticky="w")
            fila_actual += 1
            
            # Configurar columnas
            for columna in range(len(encabezados)):
                contenedor.grid_columnconfigure(columna, weight=1, minsize=90)
            
            # Encabezados
            for columna, campo in enumerate(encabezados):
                nombre_campo = self.formatear_campo(campo)
                CTK.CTkLabel(contenedor, text=nombre_campo, font=("Arial", 10, "bold"),text_color="white", fg_color="#2E2E2E", width=90, height=40).grid(row=fila_actual, column=columna, padx=1, pady=1, sticky="nsew")
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
                    
                    CTK.CTkLabel(contenedor, text=str(valor_campo), font=("Arial", 9),text_color="white", fg_color=color_fila, width=90, height=40,wraplength=85).grid(row=fila_actual, column=columna, padx=1, pady=0, sticky="nsew")
                
                fila_actual += 1
                    
        if not hay_equipos:
            CTK.CTkLabel(contenedor, text="📋 No hay equipos registrados", font=("Arial", 14),text_color="#888888").grid(row=0, column=0, pady=30)
        
        # Botón actualizar
        CTK.CTkButton(self.frame, text="🔄 Actualizar", command=self.mostrar_equipos,font=("Arial", 10, "bold"), width=120, height=28).pack(pady=8)

    def formatear_campo(self, nombre_campo):
        """Formatea nombres de campos para mostrar"""
        formatos_campos = {
            "tamano": "Tamaño",
            "sistema operativo": "S.O.",
            "almacenamiento": "Almacen."
        }
        return formatos_campos.get(nombre_campo, nombre_campo.title())

    # =================== MODIFICAR EQUIPOS ===================
    
    def modificar_equipo(self):
        """Inicia modificación de equipo"""
        self.Ut.limpiar_frame(self.frame)
        
        CTK.CTkLabel(self.frame, text="Modificar Equipo", font=("", 18, "bold")).pack(pady=15)
        CTK.CTkLabel(self.frame, text="Ingrese el serial del equipo:", font=("", 12)).pack(pady=5)
        
        entrada_serial = CTK.CTkEntry(self.frame, placeholder_text="Serial (máx 12 caracteres)", width=200)
        entrada_serial.pack(pady=10)
        
        # Validación de longitud
        def validar_serial(evento):
            if len(entrada_serial.get()) > 12:
                entrada_serial.delete(12, "end")
                self.Ut.mostrar_mensaje(self.frame, "⚠ Serial limitado a 12 caracteres", "orange")
        entrada_serial.bind("<KeyRelease>", validar_serial)
        
        frame_botones = CTK.CTkFrame(self.frame)
        frame_botones.pack(pady=15)
        
        CTK.CTkButton(frame_botones, text="Buscar Equipo",command=lambda: self.buscar_equipo(entrada_serial.get().strip())).pack(side="left", padx=5)
        CTK.CTkButton(frame_botones, text="Limpiar",command=lambda: entrada_serial.delete(0, "end")).pack(side="left", padx=5)

    def buscar_equipo(self, serial_buscar, tipo_rol="Administrador"):
        """Busca un equipo por serial"""
        if not serial_buscar:
            self.Ut.mostrar_mensaje(self.frame, "✗ Ingrese un serial", "red")
            return
        
        if len(serial_buscar) < 3 or len(serial_buscar) > 12:
            self.Ut.mostrar_mensaje(self.frame, "✗ El serial debe tener entre 3 y 12 caracteres", "red")
            return
        
        for tipo_equipo, (nombre_archivo, encabezados) in self.configuracion_equipos.items():
            lista_equipos = self.Ut.leer_csv(self.frame, nombre_archivo)
            for indice, equipo in enumerate(lista_equipos):
                if equipo.get("serial", "").strip().lower() == serial_buscar.lower():
                    self.mostrar_formulario_modificacion(equipo, lista_equipos, nombre_archivo, encabezados, indice, tipo_equipo, tipo_rol)
                    return
        
        self.Ut.mostrar_mensaje(self.frame, "✗ Equipo no encontrado", "red")

    def mostrar_formulario_modificacion(self, equipo_encontrado, lista_equipos, nombre_archivo, encabezados, indice_equipo, tipo_equipo, tipo_rol):
        """Muestra formulario de modificación"""
        self.Ut.limpiar_frame(self.frame)
        
        CTK.CTkLabel(self.frame, text=f"Modificando: {equipo_encontrado["serial"]}", font=("", 18, "bold")).pack(pady=10)
        CTK.CTkLabel(self.frame, text=f"Tipo: {tipo_equipo}", font=("", 14, "bold"), text_color="lightblue").pack(pady=5)
                
        frame_campos = CTK.CTkFrame(self.frame)
        frame_campos.pack()

        entradas_campos = {}

        for campo in encabezados:
            entrada_campo = self.Ut.crear_campo(frame_campos, campo, self.config_campos, equipo_encontrado[campo])

            entradas_campos[campo] = entrada_campo

            if tipo_equipo == "Computador Portátil" and campo == "marca":
                entradas_campos["marca"].configure(values=["HP","Dell","Lenovo","ASUS","Acer","Apple","MSI","Samsung","Toshiba","Microsoft","Sony","LG","Huawei","Gateway"])
            elif tipo_equipo == "Tableta Gráfica" and campo == "marca":
                entradas_campos["marca"].configure(values=["Wacom","Huion","XP-Pen","Gaomon","Veikk","Ugee","Parblo","Monoprice","Artisul","Bosto","Turcom"])
                        
        frame_botones_mod = CTK.CTkFrame(self.frame)
        frame_botones_mod.pack(pady=20)
        
        CTK.CTkButton(frame_botones_mod, text="Guardar Cambios",command=lambda: self.guardar_modificacion(equipo_encontrado, lista_equipos, nombre_archivo, encabezados, indice_equipo, entradas_campos, tipo_equipo),font=("", 12, "bold")).pack(side="left", padx=5)
        CTK.CTkButton(frame_botones_mod, text="Cancelar",command=self.modificar_equipo).pack(side="left", padx=5)

    def guardar_modificacion(self, equipo_original, lista_equipos, nombre_archivo, encabezados, indice_equipo, entradas_campos, tipo_equipo):
        """Guarda las modificaciones"""
        try:
            # Actualizar datos
            for campo, entrada in entradas_campos.items():
                lista_equipos[indice_equipo][campo] = entrada.get().strip()
                        
            # Escribir archivo
            with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=encabezados)
                escritor.writeheader()
                escritor.writerows(lista_equipos)
            
            # Mostrar éxito
            self.Ut.limpiar_frame(self.frame)
            CTK.CTkLabel(self.frame, text=f"✓ Equipo {equipo_original["serial"]} modificado correctamente",font=("", 16, "bold"), text_color="green").pack(pady=20)
            CTK.CTkButton(self.frame, text="Modificar equipo",command=self.modificar_equipo, font=("", 12, "bold")).pack(padx=10)
            
        except Exception as error:
            self.Ut.mostrar_mensaje(self.frame, f"✗ Error al guardar: {str(error)}", "red")