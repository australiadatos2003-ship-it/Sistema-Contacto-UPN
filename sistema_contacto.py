
from solicitud import Solicitud
from gestor_solicitudes import obtener_operaciones

class SistemaContactoUPN:
    def __init__(self, gestor):

        self.gestor = gestor

    def seleccionar_consulta(self):
        print("\nTipo de consulta:")
        print("1. Matrícula")
        print("2. Trámites")
        print("3. Becas")
        print("4. Otros")
        opcion = input("Seleccione una opción: ").strip()

        consultas = {
            "1": "Matrícula",
            "2": "Trámites",
            "3": "Becas",
            "4": "Otros"
        }

        if opcion not in consultas:
            print("Opción no válida.")
            return ""

        consulta = consultas[opcion]
        if opcion == "4":
            detalle = input("Especifique brevemente su consulta: ").strip()
            if not detalle:
                print("La consulta no puede estar vacía.")
                return ""
            consulta = "Otros: " + detalle

        return consulta

    def mostrar_menu(self):
        print("\n===== CONTACTO UPN =====")
        print("1. Registrar solicitud")
        print("2. Buscar solicitud")
        print("3. Modificar solicitud")
        print("4. Eliminar solicitud")
        print("5. Mostrar solicitudes")
        print("6. Ordenar por nombre (burbuja)")
        print("7. Ordenar por nombre (selección)")
        print("8. Mostrar solicitudes en una matriz")
        print("9. Buscar por nombre (texto parcial)")
        print("10. Marcar solicitud como atendida")
        print("11. Reporte por tipo de consulta")
        print("12. Estadísticas por estado (recursivo)")
        print("13. Ver bitácora de operaciones")
        print("0. Salir")

    def ejecutar(self):
        print("Solicitudes cargadas desde el archivo:", self.gestor.total())

        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                codigo = input("Código de identificación: ").strip()
                nombre = input("Nombre del estudiante: ").strip()
                consulta = self.seleccionar_consulta()
                if consulta:
                    solicitud = Solicitud(codigo, nombre, consulta)
                    self.gestor.registrar(solicitud)

            elif opcion == "2":
                codigo = input("Código de identificación: ").strip()
                self.gestor.buscar(codigo)

            elif opcion == "3":
                codigo = input("Código de la solicitud que desea modificar: ").strip()
                nombre = input("Nuevo nombre del estudiante: ").strip()
                consulta = self.seleccionar_consulta()
                if consulta:
                    self.gestor.modificar(codigo, nombre, consulta)

            elif opcion == "4":
                codigo = input("Código de la solicitud que desea eliminar: ").strip()
                self.gestor.eliminar(codigo)

            elif opcion == "5":
                self.gestor.mostrar_todas()

            elif opcion == "6":
                self.gestor.ordenar_por_nombre()
                self.gestor.mostrar_todas()

            elif opcion == "7":
                self.gestor.ordenar_por_nombre_seleccion()
                self.gestor.mostrar_todas()

            elif opcion == "8":
                self.gestor.mostrar_matriz()

            elif opcion == "9":
                texto = input("Texto a buscar en el nombre: ").strip()
                self.gestor.buscar_por_nombre(texto)

            elif opcion == "10":
                codigo = input("Código de la solicitud atendida: ").strip()
                self.gestor.atender(codigo)

            elif opcion == "11":
                self.gestor.reporte_por_tipo()

            elif opcion == "12":
                self.gestor.mostrar_estadisticas()

            elif opcion == "13":
                self.gestor.mostrar_bitacora()

            elif opcion == "0":
                print("Fin del programa.")
                print("Registros, modificaciones y eliminaciones realizadas:", obtener_operaciones())
                break

            else:
                print("Opción no válida. Intente nuevamente.")
