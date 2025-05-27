# Importamos las librerías necesarias
import customtkinter as CTK  # Biblioteca para interfaz gráfica moderna
import csv  # Para manipulación de archivos CSV
from datetime import datetime  # Para trabajar con fechas y horas actuales
from dateutil.parser import parse  # Para analizar y validar formatos de fecha y hora

class Metodos_Prestamos:
    # Constructor: recibe el frame donde se mostrarán los widgets
    def __init__(self, frame_principal):
        self.frame_principal = frame_principal  # Contenedor gráfico principal
        self.archivo_prestamos = "Prestamos.csv"  # Nombre del archivo donde se guardan los préstamos
        self.widgets_prestamo = {}  # Diccionario para guardar widgets de entrada y acceder a ellos fácilmente

    # Función para leer todos los préstamos del archivo CSV
    def leer_prestamos(self):
        prestamos = []
        try:
            # Si el archivo existe, lo abrimos y leemos con DictReader
            with open(self.archivo_prestamos, 'r', newline='', encoding='utf-8') as archivo_csv:
                lector_csv = csv.DictReader(archivo_csv)
                for prestamo in lector_csv:
                    prestamos.append(prestamo)
        except FileNotFoundError:
            # Si no existe el archivo, lo creamos con encabezados
            with open(self.archivo_prestamos, 'w', newline='', encoding='utf-8') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv)
                escritor_csv.writerow([
                    'id_prestamo', 'cedula_estudiante', 'serial_equipo',
                    'fecha_prestamo', 'fecha_devolucion_esperada',
                    'fecha_devolucion_real', 'estado_prestamo'
                ])
        return prestamos

    # Función para escribir un nuevo préstamo en el archivo
    def escribir_prestamo(self, prestamo):
        with open(self.archivo_prestamos, 'a', newline='', encoding='utf-8') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow([
                prestamo['id_prestamo'], prestamo['cedula_estudiante'],
                prestamo['serial_equipo'], prestamo['fecha_prestamo'],
                prestamo['fecha_devolucion_esperada'], prestamo['fecha_devolucion_real'],
                prestamo['estado_prestamo']
            ])

    # Interfaz gráfica para registrar un préstamo nuevo
    def registrar_prestamo(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()  # Limpiar el frame antes de mostrar nuevos elementos

        CTK.CTkLabel(self.frame_principal, text="Registrar Préstamo", font=('', 20)).pack(pady=10)

        # Cédula del estudiante
        etiqueta_cedula = CTK.CTkLabel(self.frame_principal, text="Cédula del Estudiante:")
        etiqueta_cedula.pack(pady=5)
        entrada_cedula = CTK.CTkEntry(self.frame_principal)
        entrada_cedula.pack(pady=5)
        self.widgets_prestamo['cedula_estudiante'] = entrada_cedula

        # Serial del equipo
        etiqueta_serial = CTK.CTkLabel(self.frame_principal, text="Serial del Equipo:")
        etiqueta_serial.pack(pady=5)
        entrada_serial = CTK.CTkEntry(self.frame_principal)
        entrada_serial.pack(pady=5)
        self.widgets_prestamo['serial_equipo'] = entrada_serial

        # Fecha esperada de devolución
        etiqueta_fecha_devolucion = CTK.CTkLabel(
            self.frame_principal,
            text="Fecha de Devolución Esperada (YYYY-MM-DD HH:MM:SS):"
        )
        etiqueta_fecha_devolucion.pack(pady=5)
        entrada_fecha_devolucion = CTK.CTkEntry(self.frame_principal)
        entrada_fecha_devolucion.pack(pady=5)
        self.widgets_prestamo['fecha_devolucion_esperada'] = entrada_fecha_devolucion

        # Botón para guardar préstamo
        boton_guardar = CTK.CTkButton(self.frame_principal, text="Guardar Préstamo", command=self.guardar_prestamo)
        boton_guardar.pack(pady=10)

        # Mensajes de éxito o error
        self.label_mensaje = CTK.CTkLabel(self.frame_principal, text="")
        self.label_mensaje.pack(pady=5)

    # Función para guardar el préstamo con validaciones
    def guardar_prestamo(self):
        cedula_estudiante = self.widgets_prestamo['cedula_estudiante'].get()
        serial_equipo = self.widgets_prestamo['serial_equipo'].get()
        fecha_devolucion_esperada = self.widgets_prestamo['fecha_devolucion_esperada'].get()

        try:
            parse(fecha_devolucion_esperada)  # Valida el formato de fecha
        except ValueError:
            self.label_mensaje.configure(text="Error: Formato de fecha inválido (YYYY-MM-DD HH:MM:SS)")
            return

        # Se generan automáticamente la fecha actual y el ID único
        id_prestamo = datetime.now().strftime("%Y%m%d%H%M%S")
        fecha_prestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Diccionario con los datos del préstamo
        nuevo_prestamo = {
            'id_prestamo': id_prestamo,
            'cedula_estudiante': cedula_estudiante,
            'serial_equipo': serial_equipo,
            'fecha_prestamo': fecha_prestamo,
            'fecha_devolucion_esperada': fecha_devolucion_esperada,
            'fecha_devolucion_real': '',
            'estado_prestamo': 'Activo'
        }

        self.escribir_prestamo(nuevo_prestamo)
        self.label_mensaje.configure(text="Préstamo registrado exitosamente.")

    # Interfaz para modificar un préstamo
    def modificar_prestamo(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        CTK.CTkLabel(self.frame_principal, text="Modificar Préstamo", font=('', 20)).pack(pady=10)

        etiqueta_id_prestamo = CTK.CTkLabel(self.frame_principal, text="ID del Préstamo a Modificar:")
        etiqueta_id_prestamo.pack(pady=5)
        entrada_id_prestamo = CTK.CTkEntry(self.frame_principal)
        entrada_id_prestamo.pack(pady=5)

        boton_buscar = CTK.CTkButton(
            self.frame_principal,
            text="Buscar Préstamo",
            command=lambda: self.buscar_y_mostrar_prestamo(entrada_id_prestamo.get())
        )
        boton_buscar.pack(pady=10)

        self.frame_modificacion = CTK.CTkFrame(self.frame_principal)
        self.frame_modificacion.pack(pady=10, fill="x")

        self.label_mensaje = CTK.CTkLabel(self.frame_principal, text="")
        self.label_mensaje.pack(pady=5)

    # Busca y muestra la información de un préstamo por su ID
    def buscar_y_mostrar_prestamo(self, id_prestamo):
        prestamos = self.leer_prestamos()
        prestamo_encontrado = next((p for p in prestamos if p['id_prestamo'] == id_prestamo), None)

        if prestamo_encontrado:
            for widget in self.frame_modificacion.winfo_children():
                widget.destroy()

            CTK.CTkLabel(self.frame_modificacion, text="Datos del Préstamo:").pack(pady=5)
            for key, value in prestamo_encontrado.items():
                CTK.CTkLabel(self.frame_modificacion, text=f"{key.capitalize()}: {value}").pack(pady=2)

            entrada_cedula = CTK.CTkEntry(self.frame_modificacion)
            entrada_cedula.insert(0, prestamo_encontrado.get('cedula_estudiante', ''))
            entrada_cedula.pack(pady=2)

            entrada_serial = CTK.CTkEntry(self.frame_modificacion)
            entrada_serial.insert(0, prestamo_encontrado.get('serial_equipo', ''))
            entrada_serial.pack(pady=2)

            entrada_fecha_devolucion = CTK.CTkEntry(self.frame_modificacion)
            entrada_fecha_devolucion.insert(0, prestamo_encontrado.get('fecha_devolucion_esperada', ''))
            entrada_fecha_devolucion.pack(pady=2)

            CTK.CTkButton(
                self.frame_modificacion, text="Guardar Cambios",
                command=lambda: self.guardar_modificacion_prestamo(
                    id_prestamo, entrada_cedula.get(), entrada_serial.get(), entrada_fecha_devolucion.get()
                )
            ).pack(pady=10)
        else:
            self.label_mensaje.configure(text="Préstamo no encontrado.")

    # Guarda los cambios de un préstamo modificado
    def guardar_modificacion_prestamo(self, id_prestamo, nueva_cedula, nuevo_serial, nueva_fecha_devolucion):
        prestamos = self.leer_prestamos()
        for prestamo in prestamos:
            if prestamo['id_prestamo'] == id_prestamo:
                if nueva_cedula:
                    prestamo['cedula_estudiante'] = nueva_cedula
                if nuevo_serial:
                    prestamo['serial_equipo'] = nuevo_serial
                if nueva_fecha_devolucion:
                    prestamo['fecha_devolucion_esperada'] = nueva_fecha_devolucion
                break
        self.reescribir_prestamos(prestamos)
        self.label_mensaje.configure(text="Préstamo modificado exitosamente.")

    # Reescribe el archivo con todos los préstamos actualizados
    def reescribir_prestamos(self, prestamos):
        with open(self.archivo_prestamos, 'w', newline='', encoding='utf-8') as archivo_csv:
            escritor_csv = csv.DictWriter(archivo_csv, fieldnames=prestamos[0].keys())
            escritor_csv.writeheader()
            escritor_csv.writerows(prestamos)

    # Interfaz para registrar la devolución de un préstamo
    def devolucion_prestamo(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        CTK.CTkLabel(self.frame_principal, text="Devolución de Préstamo", font=('', 20)).pack(pady=10)

        etiqueta_id_prestamo = CTK.CTkLabel(self.frame_principal, text="ID del Préstamo a Devolver:")
        etiqueta_id_prestamo.pack(pady=5)
        entrada_id_prestamo = CTK.CTkEntry(self.frame_principal)
        entrada_id_prestamo.pack(pady=5)

        CTK.CTkButton(
            self.frame_principal, text="Devolver Préstamo",
            command=lambda: self.registrar_devolucion(entrada_id_prestamo.get())
        ).pack(pady=10)

        self.label_mensaje = CTK.CTkLabel(self.frame_principal, text="")
        self.label_mensaje.pack(pady=5)

    # Registra la devolución de un equipo y cambia su estado
    def registrar_devolucion(self, id_prestamo):
        prestamos = self.leer_prestamos()
        for prestamo in prestamos:
            if prestamo['id_prestamo'] == id_prestamo:
                prestamo['fecha_devolucion_real'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                prestamo['estado_prestamo'] = "Devuelto"
                break
        else:
            self.label_mensaje.configure(text="Préstamo no encontrado.")
            return

        self.reescribir_prestamos(prestamos)
        self.label_mensaje.configure(text="Devolución registrada exitosamente.")

    # Muestra todos los préstamos registrados
    def mostrar_prestamos(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        CTK.CTkLabel(self.frame_principal, text="Lista de Préstamos", font=('', 20)).pack(pady=10)

        prestamos = self.leer_prestamos()
        if not prestamos:
            CTK.CTkLabel(self.frame_principal, text="No hay préstamos registrados.").pack(pady=10)
            return

        for prestamo in prestamos:
            info = (f"ID: {prestamo['id_prestamo']} | "
                    f"Cédula: {prestamo['cedula_estudiante']} | "
                    f"Equipo: {prestamo['serial_equipo']} | "
                    f"Fecha Préstamo: {prestamo['fecha_prestamo']} | "
                    f"Fecha Devolución Esperada: {prestamo['fecha_devolucion_esperada']} | "
                    f"Devuelto: {prestamo['fecha_devolucion_real']} | "
                    f"Estado: {prestamo['estado_prestamo']}")
            CTK.CTkLabel(self.frame_principal, text=info, anchor='w', justify='left', wraplength=800).pack(pady=2)

    # Método adicional que permite iniciar el registro usando un frame externo
    def registrar_prestamo_validacion_carrera(self, frame, informacion_estudiante, carrera_estudiante):
        self.frame_principal = frame
        self.registrar_prestamo()