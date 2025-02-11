"""Diseña un sistema de gestión de vehículos. Debes crear clases base como Vehículo, Coche, y Moto. Incluye atributos comunes como marca, modelo, y matrícula. Cada tipo de vehículo debe tener métodos específicos (por ejemplo, encender luces para Coche y acelerar para Moto). Añade una clase GestorVehiculos que permita registrar vehículos y listar sus detalles."""

# Clase base Vehiculo
class Vehiculo:
    def __init__(self, marca, modelo, matricula):
        self.marca = marca
        self.modelo = modelo
        self.matricula = matricula

    def mostrar_detalles(self):
        return f"Marca: {self.marca}, Modelo: {self.modelo}, Matrícula: {self.matricula}"

# Clase Coche, que hereda de Vehiculo
class Coche(Vehiculo):
    def __init__(self, marca, modelo, matricula, num_puertas):
        super().__init__(marca, modelo, matricula)
        self.num_puertas = num_puertas

    def encender_luces(self):
        return "Luces del coche encendidas."

    def mostrar_detalles(self):
        detalles = super().mostrar_detalles()
        return f"{detalles}, Número de puertas: {self.num_puertas}"

# Clase Moto, que hereda de Vehiculo
class Moto(Vehiculo):
    def __init__(self, marca, modelo, matricula, tipo_motor):
        super().__init__(marca, modelo, matricula)
        self.tipo_motor = tipo_motor

    def acelerar(self):
        return "Moto acelerando."

    def mostrar_detalles(self):
        detalles = super().mostrar_detalles()
        return f"{detalles}, Tipo de motor: {self.tipo_motor}"

# Clase GestorVehiculos para gestionar los vehículos
class GestorVehiculos:
    def __init__(self):
        self.vehiculos = []

    def registrar_vehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)

    def listar_vehiculos(self):
        for vehiculo in self.vehiculos:
            print(vehiculo.mostrar_detalles())

# Creación de objetos y prueba del sistema
if __name__ == "__main__":
    # Crear vehículos
    coche1 = Coche("Toyota", "Corolla", "1234ABC", 4)
    moto1 = Moto("Yamaha", "R1", "5678XYZ", "De 1000cc")

    # Crear gestor de vehículos
    gestor = GestorVehiculos()

    # Registrar vehículos
    gestor.registrar_vehiculo(coche1)
    gestor.registrar_vehiculo(moto1)

    # Listar detalles de los vehículos registrados
    print("Detalles de los vehículos registrados:")
    gestor.listar_vehiculos()

    # Usar métodos específicos de los vehículos
    print("\nAcciones específicas de los vehículos:")
    print(coche1.encender_luces())  # Método específico de Coche
    print(moto1.acelerar())  # Método específico de Moto
