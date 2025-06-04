class ESTUDIANTES:
    def __init__(self, identificacion, nombre, apellido, telefono, estado="ACTIVO", serial="", rol=""):
        self.identificacion = identificacion 
        self.nombre = nombre 
        self.apellido = apellido 
        self.telefono = telefono
        self.estado = estado
        self.serial = serial 
        self.rol = rol

class ESTUDIANTE_INGENIERIA(ESTUDIANTES):
    def __init__(self, identificacion, nombre, apellido, telefono, semestre, promedio, estado="ACTIVO", serial="", rol="Estudiante"):
        super().__init__(identificacion, nombre, apellido, telefono, estado, serial, rol)
        self.semestre = semestre 
        self.promedio = promedio 

    def convertir_lista_ingenieria(self):
        return [self.identificacion,self.nombre,self.apellido,self.telefono,self.semestre,self.promedio,self.estado,self.serial,self.rol]
        
class ESTUDIANTE_DISENO(ESTUDIANTES):
    def __init__(self, identificacion, nombre, apellido, telefono, modalidad, cantidad_asignaturas, estado="ACTIVO", serial="", rol="Estudiante"):
        super().__init__(identificacion, nombre, apellido, telefono, estado, serial, rol)
        self.modalidad = modalidad 
        self.cantidad_asignaturas = cantidad_asignaturas 

    def convertir_lista_diseno(self):
        return [self.identificacion,self.nombre,self.apellido,self.telefono,self.modalidad,self.cantidad_asignaturas,self.estado,self.serial,self.rol]

class ADMIN(ESTUDIANTES):
    def __init__(self, identificacion, nombre, apellido, estado="ACTIVO", rol="Administrador"):
        super().__init__(identificacion, nombre, apellido, estado, rol)
        
    def convertir_lista_admin(self):
        return [self.identificacion,self.nombre,self.apellido,self.estado,self.rol]

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

    def convertir_lista_tableta(self):
        return [self.serial,self.marca,self.tamano,self.precio,self.almacenamiento,self.peso,self.estado]
        
class COMPUTADOR_PORTATIL(DISPOSITIVOS):
    def __init__(self, serial, marca, tamano, precio, sistema_operativo, procesador, estado="ACTIVO"):
        super().__init__(serial, marca, tamano, precio, estado)
        self.sistema_operativo = sistema_operativo 
        self.procesador = procesador

    def convertir_lista_computador(self):
        return [self.serial,self.marca,self.tamano,self.precio,self.sistema_operativo,self.procesador,self.estado]