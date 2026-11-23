
class Solicitud:
    def __init__(self, codigo, nombre, consulta):
        self.codigo = codigo
        self.nombre = nombre
        self.consulta = consulta
        self.estado = "Pendiente"

    def mostrar(self):
        print("Código:", self.codigo)
        print("Estudiante:", self.nombre)
        print("Consulta:", self.consulta)
        print("Estado:", self.estado)

    def como_fila(self):
        return [self.codigo, self.nombre, self.consulta, self.estado]
