class ESTUDIANTES:
    def __init__(self, cedula, nombre, apellido, telefono, estado="ACTIVO", serial=""):
        self.cedula = cedula 
        self.nombre = nombre 
        self.apellido = apellido 
        self.telefono = telefono
        self.estado = estado
        self.serial = serial

class ESTUDIANTE_INGENIERIA(ESTUDIANTES):
    def __init__(self, cedula, nombre, apellido, telefono, semestre, promedio, estado="ACTIVO", serial=""):
        super().__init__(cedula, nombre, apellido, telefono, estado, serial)
        self.semestre = semestre 
        self.promedio = promedio 

    def convertir_lista(self):
        return [
            self.cedula, self.nombre, self.apellido,
            self.telefono, self.semestre, self.promedio,
            self.estado, self.serial
        ]

class ESTUDIANTE_DISENO(ESTUDIANTES):
    def __init__(self, cedula, nombre, apellido, telefono, modalidad, cantidad_asignaturas, estado="ACTIVO", serial=""):
        super().__init__(cedula, nombre, apellido, telefono, estado, serial)
        self.modalidad = modalidad 
        self.cantidad_asignaturas = cantidad_asignaturas 

    def convertir_lista(self):
        return [
            self.cedula, self.nombre, self.apellido,
            self.telefono, self.modalidad, self.cantidad_asignaturas,
            self.estado, self.serial
        ]

class DISPOSITIVOS:
    def __init__(self, serial, marca, tamano, precio, estado="ACTIVO"):
        self.serial = serial 
        self.marca = marca 
        self.tamano = tamano 
        self.precio = precio 
        self.estado = estado
    
class TABLETA_GRAFICA(DISPOSITIVOS):
    def __init__(self, serial, marca, tamano, precio, almacenamiento, peso, estado="ACTIVO"):
        super().__init__(serial, marca, tamano, precio, estado)
        self.almacenamiento = almacenamiento 
        self.peso = peso

    def convertir_lista(self):
        return [
            self.serial, self.marca, self.tamano,
            self.precio, self.almacenamiento, self.peso,
            self.estado
        ]

class COMPUTADOR_PORTATIL(DISPOSITIVOS):
    def __init__(self, serial, marca, tamano, precio, sistema_operativo, procesador, estado="ACTIVO"):
        super().__init__(serial, marca, tamano, precio, estado)
        self.sistema_operativo = sistema_operativo 
        self.procesador = procesador

    def convertir_lista(self):
        return [
            self.serial, self.marca, self.tamano,
            self.precio, self.sistema_operativo, self.procesador,
            self.estado
        ]
