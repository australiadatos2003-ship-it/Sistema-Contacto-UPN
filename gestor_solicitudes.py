
from solicitud import Solicitud

operaciones_realizadas = 0

def contar_operacion():
    global operaciones_realizadas
    operaciones_realizadas += 1

def obtener_operaciones():
    return operaciones_realizadas

RUTA_SOLICITUDES = "solicitudes.csv"
RUTA_BITACORA = "bitacora.txt"
SEPARADOR = ";"

def asegurar_archivo(ruta):
    archivo = open(ruta, "a", encoding="utf-8")
    archivo.close()

def guardar_solicitudes(solicitudes):
    with open(RUTA_SOLICITUDES, "w", encoding="utf-8") as archivo:
        for solicitud in solicitudes:
            campos = []
            for campo in solicitud.como_fila():
                campos.append(campo.replace(SEPARADOR, ","))
            archivo.write(SEPARADOR.join(campos) + "\n")

def cargar_solicitudes():
    solicitudes = []
    asegurar_archivo(RUTA_SOLICITUDES)
    with open(RUTA_SOLICITUDES, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if linea.strip() != "":
                campos = linea.strip().split(SEPARADOR)
                if len(campos) == 4:
                    solicitud = Solicitud(campos[0], campos[1], campos[2])
                    solicitud.estado = campos[3]
                    solicitudes.append(solicitud)
                else:
                    print("Aviso: se omitió una línea con formato incorrecto.")
    return solicitudes

def registrar_bitacora(mensaje):
    with open(RUTA_BITACORA, "a", encoding="utf-8") as archivo:
        archivo.write(mensaje + "\n")

def imprimir_bitacora():
    asegurar_archivo(RUTA_BITACORA)
    with open(RUTA_BITACORA, "r", encoding="utf-8") as archivo:
        total = len(archivo.readlines())  
        archivo.seek(0)                   
        print("Operaciones registradas en la bitácora:", total)
        for linea in archivo:
            print(linea.strip())


class GestorSolicitudes:
    def __init__(self):
        self._solicitudes = cargar_solicitudes()

    def guardar_cambios(self, detalle):
        guardar_solicitudes(self._solicitudes)
        registrar_bitacora(detalle)

    def total(self):
        return len(self._solicitudes)

    def registrar(self, solicitud):
        if (not solicitud.codigo.strip() or not solicitud.nombre.strip()
                or not solicitud.consulta.strip()):
            print("Error: todos los campos son obligatorios.")
            return False

        if self.buscar_indice(solicitud.codigo) != -1:
            print("Error: ya existe una solicitud con ese código.")
            return False

        self._solicitudes.append(solicitud)
        contar_operacion()
        self.guardar_cambios("REGISTRAR código " + solicitud.codigo)
        print("Solicitud registrada correctamente.")
        return True

    def buscar_indice(self, codigo):
        for i in range(len(self._solicitudes)):
            if self._solicitudes[i].codigo == codigo:
                return i
        return -1

    def buscar(self, codigo):
        indice = self.buscar_indice(codigo)
        if indice == -1:
            print("No se encontró una solicitud con ese código.")
        else:
            self._solicitudes[indice].mostrar()

    def modificar(self, codigo, nuevo_nombre, nueva_consulta):
        indice = self.buscar_indice(codigo)
        if indice == -1:
            print("No se encontró una solicitud con ese código.")
            return False

        if not nuevo_nombre.strip() or not nueva_consulta.strip():
            print("Error: el nombre y la consulta no pueden estar vacíos.")
            return False

        self._solicitudes[indice].nombre = nuevo_nombre.strip()
        self._solicitudes[indice].consulta = nueva_consulta.strip()
        contar_operacion()
        self.guardar_cambios("MODIFICAR código " + codigo)
        print("Solicitud modificada correctamente.")
        return True

    def eliminar(self, codigo):
        indice = self.buscar_indice(codigo)
        if indice == -1:
            print("No se encontró una solicitud con ese código.")
            return False

        self._solicitudes.pop(indice)
        contar_operacion()
        self.guardar_cambios("ELIMINAR código " + codigo)
        print("Solicitud eliminada correctamente.")
        return True

    def mostrar_todas(self):
        if len(self._solicitudes) == 0:
            print("No hay solicitudes registradas.")
            return

        for solicitud in self._solicitudes:
            print("--------------------")
            solicitud.mostrar()

    def ordenar_por_nombre(self):
        cantidad = len(self._solicitudes)
        for i in range(cantidad - 1):
            for j in range(cantidad - 1 - i):
                nombre_actual = self._solicitudes[j].nombre.lower()
                nombre_siguiente = self._solicitudes[j + 1].nombre.lower()
                if nombre_actual > nombre_siguiente:
                    temporal = self._solicitudes[j]
                    self._solicitudes[j] = self._solicitudes[j + 1]
                    self._solicitudes[j + 1] = temporal

        if cantidad > 1:
            contar_operacion()
            self.guardar_cambios("ORDENAR por nombre (burbuja)")
        print("Solicitudes ordenadas por nombre.")

    def ordenar_por_nombre_seleccion(self):
        cantidad = len(self._solicitudes)
        for i in range(cantidad - 1):
            menor = i
            for j in range(i + 1, cantidad):
                if self._solicitudes[j].nombre.lower() < self._solicitudes[menor].nombre.lower():
                    menor = j
            if menor != i:
                temporal = self._solicitudes[i]
                self._solicitudes[i] = self._solicitudes[menor]
                self._solicitudes[menor] = temporal

        if cantidad > 1:
            contar_operacion()
            self.guardar_cambios("ORDENAR por nombre (selección)")
        print("Solicitudes ordenadas por nombre mediante selección.")

    def mostrar_matriz(self):
        matriz = [["Código", "Estudiante", "Consulta", "Estado"]]
        for solicitud in self._solicitudes:
            matriz.append(solicitud.como_fila())

        for fila in matriz:
            print(" | ".join(fila))

    def buscar_por_nombre(self, texto):
        if not texto.strip():
            print("Error: debe escribir un texto para buscar.")
            return

        encontradas = 0
        for solicitud in self._solicitudes:
            if texto.strip().lower() in solicitud.nombre.lower():
                print("--------------------")
                solicitud.mostrar()
                encontradas += 1

        if encontradas == 0:
            print("No se encontraron estudiantes con ese texto.")
        else:
            print("Coincidencias encontradas:", encontradas)

    def atender(self, codigo):
        indice = self.buscar_indice(codigo)
        if indice == -1:
            print("No se encontró una solicitud con ese código.")
            return False

        if self._solicitudes[indice].estado == "Atendida":
            print("La solicitud ya estaba atendida.")
            return False

        self._solicitudes[indice].estado = "Atendida"
        contar_operacion()
        self.guardar_cambios("ATENDER código " + codigo)
        print("Solicitud marcada como atendida.")
        return True

    def reporte_por_tipo(self):
        tipos = ["Matrícula", "Trámites", "Becas", "Otros"]
        cantidades = [0, 0, 0, 0]

        for solicitud in self._solicitudes:
            for i in range(len(tipos)):
                
                if solicitud.consulta.find(tipos[i]) == 0:
                    cantidades[i] += 1

        print("Solicitudes por tipo de consulta:")
        for i in range(len(tipos)):
            print("-", tipos[i] + ":", cantidades[i])
        print("Total de solicitudes:", len(self._solicitudes))

    def contar_por_estado_recursivo(self, estado, indice):

        if indice == len(self._solicitudes):
            return 0

        if self._solicitudes[indice].estado == estado:
            return 1 + self.contar_por_estado_recursivo(estado, indice + 1)
        return self.contar_por_estado_recursivo(estado, indice + 1)

    def mostrar_estadisticas(self):
        pendientes = self.contar_por_estado_recursivo("Pendiente", 0)
        atendidas = self.contar_por_estado_recursivo("Atendida", 0)
        print("Solicitudes pendientes:", pendientes)
        print("Solicitudes atendidas:", atendidas)
        print("Total:", pendientes + atendidas)

    def mostrar_bitacora(self):
        imprimir_bitacora()
