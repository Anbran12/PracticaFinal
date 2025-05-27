import csv
import customtkinter as CTK
from Objetos import COMPUTADOR_PORTATIL, TABLETA_GRAFICA

class Metodos_Equipos:
    def __init__(self, frame):
        self.frame = frame
        self.archivos = {
            "Computador Portátil": (
                "Computadores_Portatiles.csv",
                ['serial', 'marca', 'tamano', 'precio', 'sistema_operativo', 'procesador', 'estado']
            ),
            "Tableta Gráfica": (
                "Tabletas_Graficas.csv",
                ['serial', 'marca', 'tamano', 'precio', 'almacenamiento', 'peso', 'estado']
            )
        }
        self.widgets = {}

    def leer_csv(self, archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            return []

    def escribir_csv(self, equipo, archivo, encabezados):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                tiene_contenido = f.read(1) != ''
        except FileNotFoundError:
            tiene_contenido = False

        with open(archivo, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not tiene_contenido:
                writer.writerow(encabezados)
            writer.writerow(
                equipo.convertir_lista_computador() if isinstance(equipo, COMPUTADOR_PORTATIL)
                else equipo.convertir_lista_tableta()
            )

    def limpiar_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def crear_entrada(self, campo, placeholder=""):
        CTK.CTkLabel(self.frame, text=campo + ":").pack(pady=5)
        entrada = CTK.CTkEntry(self.frame, placeholder_text=placeholder)
        entrada.pack(pady=5)
        return entrada

    def registrar_equipo(self):
        self.limpiar_frame()
        self.widgets = {}

        CTK.CTkLabel(self.frame, text="Tipo de Equipo:").pack(pady=5)
        tipo = CTK.CTkComboBox(self.frame, values=list(self.archivos.keys()))
        tipo.pack(pady=5)
        tipo.set("Computador Portátil")
        self.widgets["tipo"] = tipo

        campos_base = [("Serial", ""), ("Marca", ""), ("Tamaño", ""), ("Precio", "")]
        for nombre, texto in campos_base:
            clave = nombre.lower().replace("ñ", "n")
            self.widgets[clave] = self.crear_entrada(nombre, texto)

        self.widgets["sistema_operativo"] = self.crear_entrada("Sistema Operativo", "Ej: Windows 11")
        self.widgets["procesador"] = self.crear_entrada("Procesador", "Ej: Intel i5")
        self.widgets["almacenamiento"] = self.crear_entrada("Almacenamiento", "Ej: 64 GB")
        self.widgets["peso"] = self.crear_entrada("Peso", "Ej: 350 g")

        def actualizar_campos(event=None):
            tipo_equipo = tipo.get()
            if tipo_equipo == "Computador Portátil":
                self.widgets["sistema_operativo"].configure(state="normal")
                self.widgets["procesador"].configure(state="normal")
                self.widgets["almacenamiento"].configure(state="disabled")
                self.widgets["peso"].configure(state="disabled")
            else:
                self.widgets["sistema_operativo"].configure(state="disabled")
                self.widgets["procesador"].configure(state="disabled")
                self.widgets["almacenamiento"].configure(state="normal")
                self.widgets["peso"].configure(state="normal")

        tipo.bind("<<ComboboxSelected>>", actualizar_campos)
        self.frame.after(100, actualizar_campos)

        CTK.CTkButton(self.frame, text="Guardar", command=self.guardar_equipo).pack(pady=10)

    def guardar_equipo(self):
        datos = {k: w.get() for k, w in self.widgets.items() if isinstance(w, CTK.CTkEntry) or isinstance(w, CTK.CTkComboBox)}
        tipo = datos['tipo']
        archivo, headers = self.archivos[tipo]

        try:
            precio = float(datos['precio'])
        except ValueError:
            CTK.CTkLabel(self.frame, text="Precio inválido").pack()
            return

        if tipo == "Computador Portátil":
            equipo = COMPUTADOR_PORTATIL(
                datos['serial'], datos['marca'], datos['tamano'], precio,
                datos['sistema_operativo'], datos['procesador'], "Activo"
            )
        else:
            equipo = TABLETA_GRAFICA(
                datos['serial'], datos['marca'], datos['tamano'], precio,
                datos['almacenamiento'], datos['peso'], "Activo"
            )

        self.escribir_csv(equipo, archivo, headers)
        CTK.CTkLabel(self.frame, text="Equipo guardado correctamente").pack(pady=5)

    def mostrar_equipos(self):
        self.limpiar_frame()
        CTK.CTkLabel(self.frame, text="Lista de Equipos", font=("", 20)).pack(pady=10)

        for tipo, (archivo, _) in self.archivos.items():
            CTK.CTkLabel(self.frame, text=f"--- {tipo} ---", font=("", 16)).pack(pady=5)
            equipos = self.leer_csv(archivo)

            if equipos:
                caja = CTK.CTkTextbox(self.frame, width=700, height=200, wrap="word")
                caja.pack(padx=10, pady=5)
                for eq in equipos:
                    texto = ", ".join([f"{k}: {v}" for k, v in eq.items()])
                    caja.insert("end", texto + "\n")
                caja.configure(state="disabled")
            else:
                CTK.CTkLabel(self.frame, text="No hay equipos registrados.").pack(pady=5)

    def modificar_equipo(self):
        self.limpiar_frame()
        CTK.CTkLabel(self.frame, text="Serial del equipo a modificar:").pack(pady=5)
        entrada_serial = CTK.CTkEntry(self.frame)
        entrada_serial.pack(pady=5)

        def buscar():
            serial = entrada_serial.get()
            for tipo, (archivo, headers) in self.archivos.items():
                equipos = self.leer_csv(archivo)
                for equipo in equipos:
                    if equipo['serial'] == serial:
                        self.mostrar_modificacion(equipo, equipos, archivo, headers)
                        return
            CTK.CTkLabel(self.frame, text="Equipo no encontrado.").pack()

        CTK.CTkButton(self.frame, text="Buscar", command=buscar).pack(pady=10)

    def mostrar_modificacion(self, equipo, lista, archivo, headers):
        self.limpiar_frame()
        CTK.CTkLabel(self.frame, text=f"Modificando: {equipo['serial']}").pack(pady=5)
        entradas = {}

        for campo in ['marca', 'tamano', 'precio']:
            CTK.CTkLabel(self.frame, text=campo.capitalize() + ":").pack(pady=5)
            entrada = CTK.CTkEntry(self.frame)
            entrada.insert(0, equipo[campo])
            entrada.pack(pady=5)
            entradas[campo] = entrada

        def guardar():
            for campo in entradas:
                equipo[campo] = entradas[campo].get()
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(lista)
            CTK.CTkLabel(self.frame, text="Modificación guardada.").pack(pady=5)

        CTK.CTkButton(self.frame, text="Guardar cambios", command=guardar).pack(pady=10)
