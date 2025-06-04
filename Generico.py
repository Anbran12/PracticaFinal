import customtkinter as CTK
import csv
from Objetos import ESTUDIANTE_DISENO,ESTUDIANTE_INGENIERIA,ADMIN,COMPUTADOR_PORTATIL,TABLETA_GRAFICA

    # =================== UTILIDADES ===================
class Utilidades:
    
    def configuracion_usuarios(self):
        config_usuarios = {
            "Estudiante Ingeniería":("Estudiantes_ingenieria.csv",["identificacion", "nombre", "apellido", "telefono", "semestre", "promedio", "estado", "serial", "rol"]),
            "Estudiante Diseño":("Estudiantes_diseno.csv",["identificacion", "nombre", "apellido", "telefono", "modalidad", "cantidad_asignaturas", "estado", "serial", "rol"]),
            "Administrador":("Administradores.csv",["identificacion", "nombre", "apellido", "estado", "rol"])
        }
        return config_usuarios

    def configuracion_equipos(self):
        config_equipos = {
            "Computador Portátil": ("Computadores_Portatiles.csv",["serial", "marca", "tamano", "precio", "sistema operativo", "procesador", "estado"]),
            "Tableta Gráfica": ("Tabletas_Graficas.csv",["serial", "marca", "tamano", "precio", "almacenamiento", "peso", "estado"])
        }
        return config_equipos

    def configuracion_campos_usuarios(self):
        config_campos_usuarios = {
            "identificacion": {"label": "No. Identificación", "Tipo": "Entry", "placeholder": "No. Identificación", "longitud": 15, "tipo_dato": "numero"},
            "nombre": {"label": "Nombre", "Tipo": "Entry", "placeholder": "Nombre", "longitud": 30},
            "apellido": {"label": "Apellido", "Tipo": "Entry", "placeholder": "Apellido", "longitud": 30},
            "telefono": {"label": "Teléfono", "Tipo": "Entry", "placeholder": "Teléfono", "longitud": 15, "tipo_dato": "numero"},
            "estado": {"label": "Estado", "Tipo": "CTkOptionMenu", "values": ["ACTIVO","INACTIVO"]},
            "serial": {"label": "Serial", "Tipo": "CTkOptionMenu", "values": []},
            "rol": {"label": "Rol", "Tipo": "CTkOptionMenu", "values": ["Estudiante", "Administrador"]},            
            "semestre": {"label": "Semestre", "Tipo": "CTkOptionMenu", "values": [str(i+1) for i in range(12)]},
            "promedio": {"label": "Promedio", "Tipo": "Entry", "placeholder": "Promedio", "longitud": 4, "tipo_dato": "numero"},
            "modalidad": {"label": "Modalidad", "Tipo": "CTkOptionMenu", "values": ["Presencial","Virtual","Mixta"]},
            "cantidad_asignaturas": {"label": "Cantidad asignaturas", "Tipo": "CTkOptionMenu", "values": [str(i+1) for i in range(15)]}
        }
        return config_campos_usuarios
    
    def configuracion_campos_equipos(self):
        config_campos_equipos = {
            "serial": {"label": "Serial", "Tipo": "Entry", "placeholder": "Número de serie", "longitud": 15},
            "marca": {"label": "Marca", "Tipo": "CTkOptionMenu", "values": ["HP","Dell","Lenovo","ASUS","Acer","Apple","MSI","Samsung","Toshiba","Microsoft","Sony","LG","Huawei","Gateway"]},
            "tamano": {"label": "Tamaño", "Tipo": "Entry", "placeholder": "Ej: 15.6, 10.8", "tipo_dato": "numero", "longitud": 5},
            "precio": {"label": "Precio", "Tipo": "Entry", "placeholder": "Precio en pesos", "tipo_dato": "numero", "longitud": 15},
            "sistema operativo": {"label": "Sistema Operativo", "Tipo": "CTkOptionMenu", "values": ["Windows 10","Windows 11","Ubuntu","Debian","Fedora","Linux Mint","macOS"]},
            "procesador": {"label": "Procesador", "Tipo": "CTkOptionMenu", "values": ["Intel Core i3", "Intel Core i5", "Intel Core i7", "Intel Core i9","AMD Ryzen 3", "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9","Apple M1", "Apple M2", "Apple M3"]},
            "almacenamiento": {"label": "Almacenamiento", "Tipo": "CTkOptionMenu", "values": ["128 GB", "256 GB", "512 GB", "1 TB", "2 TB"]},
            "peso": {"label": "Peso", "Tipo": "Entry", "placeholder": "Ej: 350", "tipo_dato": "numero", "longitud": 5},
            "estado": {"label": "Estado", "Tipo": "CTkOptionMenu", "values": ["ACTIVO","INACTIVO"]}
        }
        return config_campos_equipos

    def limpiar_frame(self, frame):
        """Limpia todos los widgets del frame"""
        for widget in frame.winfo_children():
            widget.destroy()
        self.label_mensaje = None
        self.widgets = {}

    def mostrar_mensaje(self, frame, mensaje, color="white"):
        """Muestra un mensaje en la interfaz"""
        if self.label_mensaje:
            self.label_mensaje.destroy()
        self.label_mensaje = CTK.CTkLabel(frame, text=mensaje, text_color=color)
        self.label_mensaje.pack(pady=5)
        frame.update_idletasks()

    def leer_csv(self, frame, nombre_archivo):
        """Lee un archivo CSV"""
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as archivo:
                return list(csv.DictReader(archivo))
        except FileNotFoundError:
            return []
        except Exception as error:
            self.mostrar_mensaje(frame, f"✗ Error al leer archivo: {error}", "red")
            return []

    def escribir_csv(self, frame, objeto, nombre_archivo, encabezados):
        """Escribe un objeto al CSV"""
        try:
            # Verificar si el archivo necesita encabezados
            archivo_existe = False
            try:
                with open(nombre_archivo, "r", encoding="utf-8") as archivo:
                    archivo_existe = archivo.read(1) != ""
            except FileNotFoundError:
                pass

            with open(nombre_archivo, "a", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                if not archivo_existe:
                    escritor.writerow(encabezados)

                if isinstance(objeto, ADMIN):
                    escritor.writerow(objeto.convertir_lista_admin())
                elif isinstance(objeto, ESTUDIANTE_INGENIERIA):
                    escritor.writerow(objeto.convertir_lista_ingenieria())
                elif isinstance(objeto, ESTUDIANTE_DISENO):
                    escritor.writerow(objeto.convertir_lista_diseno())
                elif isinstance(objeto, COMPUTADOR_PORTATIL):
                    escritor.writerow(objeto.convertir_lista_computador())
                elif isinstance(objeto, TABLETA_GRAFICA):
                    escritor.writerow(objeto.convertir_lista_tableta())

        except Exception as error:
            self.mostrar_mensaje(frame, f"✗ Error al escribir CSV: {error}", "red")

    def validar_campo(self,frame, valor, clave_campo, config_campos, longitud=15):
        """Valida un campo según su configuración"""
        valor = valor.strip()
        
        # Validar vacío
        if not valor:
            self.mostrar_mensaje(frame, f"✗ El campo {config_campos[clave_campo]["label"]} es obligatorio", "red")
            return False
        
        # Validar longitud
        if len(valor) > longitud:
            self.mostrar_mensaje(frame, f"✗ {config_campos[clave_campo]["label"]} no puede exceder {longitud} caracteres", "red")
            return False
        
        # Validar números
        if config_campos[clave_campo].get("tipo_dato") == "numero":
            try:
                numero = float(valor)
                if numero <= 0:
                    self.mostrar_mensaje(frame, f"✗ {config_campos[clave_campo]["label"]} debe ser mayor a 0", "red")
                    return False
            except ValueError:
                self.mostrar_mensaje(frame, f"✗ {config_campos[clave_campo]["label"]} debe ser un número válido", "red")
                return False
        
        return True

    def crear_campo(self, frame, clave_campo, config_campos, valor_inicial=""):
        """Crea un campo de entrada con validación"""
        configuracion = config_campos[clave_campo]
        frame_campo = CTK.CTkFrame(frame, bg_color="transparent")
        
        CTK.CTkLabel(frame_campo, text=configuracion["label"] + ":", width=130).grid(row=0, column=0, padx=5)
        widget = None
        if configuracion["Tipo"] == "Entry":
            entrada = CTK.CTkEntry(frame_campo, placeholder_text=configuracion["placeholder"])
            if valor_inicial:
                entrada.insert(0, valor_inicial)
            entrada.grid(row=0, column=1, padx=5)
            widget = entrada

            # Validación de longitud en tiempo real
            def validar_longitud(evento):
                if len(entrada.get()) > configuracion["longitud"]:
                    entrada.delete(configuracion["longitud"], "end")
                    self.mostrar_mensaje(frame, f"⚠ {configuracion['label']} limitado a {configuracion['longitud']} caracteres", "orange")
            entrada.bind("<KeyRelease>", validar_longitud)

        elif configuracion["Tipo"] == "CTkOptionMenu":
#            desplegable = CTK.CTkComboBox(frame_campo, values=configuracion["values"])            
            desplegable = CTK.CTkOptionMenu(frame_campo, values=configuracion["values"])
            if valor_inicial:
                desplegable.set(valor_inicial)
            desplegable.grid(row=0, column=1, padx=5)
            widget = desplegable

        frame_campo.pack(pady=2, anchor="w")
        return widget
    
    def identificador_existe(self, frame, identificador, config_archivos, excluir_identificador=None):
        """Verifica si un serial o No. de identificación (identificador) ya existe"""
        identificador = identificador.strip().lower()
        for tipo_registro, (nombre_archivo, encabezados) in config_archivos.items():
            lista_registros = self.leer_csv(frame, nombre_archivo)
            for registro in lista_registros:
                identificador_registro = (registro.get("serial") or registro.get("identificacion") or "").strip().lower()
                if identificador_registro == identificador and identificador_registro != (excluir_identificador or "").lower():
                    return True
        return False
