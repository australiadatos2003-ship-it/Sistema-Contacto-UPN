
from gestor_solicitudes import GestorSolicitudes
from sistema_contacto import SistemaContactoUPN


def main():
    gestor = GestorSolicitudes()
    sistema = SistemaContactoUPN(gestor)
    sistema.ejecutar()


if __name__ == "__main__":
    main()
