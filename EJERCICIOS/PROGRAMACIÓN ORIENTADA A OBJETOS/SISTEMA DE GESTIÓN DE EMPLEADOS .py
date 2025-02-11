<<<<<<< HEAD
""" SISTEMA DE GESTIÓN DE EMPLEADOS 
Supongamos que estás construyendo un sistema de gestión de empleados 
para una empresa. Crea un sistema de clases que maneje la información de 
los empleados, incluyendo empleados a tiempo completo y empleados a 
tiempo parcial.- Clase base: `Empleado`
  - Atributos: nombre, apellido, salario base- Clase derivada: `EmpleadoTiempoCompleto` (hereda de `Empleado`)
  - Atributo adicional: bono anual- Clase derivada: `EmpleadoTiempoParcial` (hereda de `Empleado`)
  - Atributo adicional: horas trabajadas por semana
Resuelve el problema creando instancias de estas clases y calculando los 
salarios totales para diferentes tipos de empleados. """

#Creamos la Clase padre "Empleado".
class Empleado:
    def __init__(self,nombre, apellido, salario_base):
        self.nombre = nombre
        self.apellido = apellido
        self.salario_base = salario_base
#Creamos la clase derivada de Empleado, Empleado a tiempo completo.
class EmpleadoTiempoCompleto(Empleado):
    def __init__(self, nombre, apellido, salario_base, bono_anual):
        #Llamamos a la superclase.
        super().__init__(nombre, apellido, salario_base)
        self.bono_anual = bono_anual
    #Agregamos un módulo para calcular el salario total del empleado a tiempo completo
    def calcular_salario_total(self):
        return(self.salario_base + self.bono_anual)
    
#Creamos la clase derivada de Empleado, Empleado a tiempo parcial.
class EmpleadoTiempoParcial(Empleado):
    def __init__(self, nombre, apellido, salario_base, horas_trabajadas_semana):
        super().__init__(nombre, apellido, salario_base)
        self.horas_trabajadas_semana = horas_trabajadas_semana
    #Agregamos el módulo para calcular su salario total del emeplado a tiempo parcial.
    def calcular_salario_total(self):
        return(self.salario_base + 1.5 * self.horas_trabajadas_semana*4*12)
    
#EJEMPLO DE USO.
#Podríamos hacerlo con inputs para que el usuario lo introdujera pero es un ejemplo de uso.
empleado_tiempo_completo = EmpleadoTiempoCompleto("Juan", "Rodriguez", 50000, 3000)
print("El salario total del empleado a tiempo completo es:", empleado_tiempo_completo.calcular_salario_total())

empleado_tiempo_parcial = EmpleadoTiempoParcial("Ana", "Martinez", 30000, 25)
=======
""" SISTEMA DE GESTIÓN DE EMPLEADOS 
Supongamos que estás construyendo un sistema de gestión de empleados 
para una empresa. Crea un sistema de clases que maneje la información de 
los empleados, incluyendo empleados a tiempo completo y empleados a 
tiempo parcial.- Clase base: `Empleado`
  - Atributos: nombre, apellido, salario base- Clase derivada: `EmpleadoTiempoCompleto` (hereda de `Empleado`)
  - Atributo adicional: bono anual- Clase derivada: `EmpleadoTiempoParcial` (hereda de `Empleado`)
  - Atributo adicional: horas trabajadas por semana
Resuelve el problema creando instancias de estas clases y calculando los 
salarios totales para diferentes tipos de empleados. """

#Creamos la Clase padre "Empleado".
class Empleado:
    def __init__(self,nombre, apellido, salario_base):
        self.nombre = nombre
        self.apellido = apellido
        self.salario_base = salario_base
#Creamos la clase derivada de Empleado, Empleado a tiempo completo.
class EmpleadoTiempoCompleto(Empleado):
    def __init__(self, nombre, apellido, salario_base, bono_anual):
        #Llamamos a la superclase.
        super().__init__(nombre, apellido, salario_base)
        self.bono_anual = bono_anual
    #Agregamos un módulo para calcular el salario total del empleado a tiempo completo
    def calcular_salario_total(self):
        return(self.salario_base + self.bono_anual)
    
#Creamos la clase derivada de Empleado, Empleado a tiempo parcial.
class EmpleadoTiempoParcial(Empleado):
    def __init__(self, nombre, apellido, salario_base, horas_trabajadas_semana):
        super().__init__(nombre, apellido, salario_base)
        self.horas_trabajadas_semana = horas_trabajadas_semana
    #Agregamos el módulo para calcular su salario total del emeplado a tiempo parcial.
    def calcular_salario_total(self):
        return(self.salario_base + 1.5 * self.horas_trabajadas_semana*4*12)
    
#EJEMPLO DE USO.
#Podríamos hacerlo con inputs para que el usuario lo introdujera pero es un ejemplo de uso.
empleado_tiempo_completo = EmpleadoTiempoCompleto("Juan", "Rodriguez", 50000, 3000)
print("El salario total del empleado a tiempo completo es:", empleado_tiempo_completo.calcular_salario_total())

empleado_tiempo_parcial = EmpleadoTiempoParcial("Ana", "Martinez", 30000, 25)
>>>>>>> 8086a913e9293b9a0f75a387e841b4f9cd77ad76
print("El salario total del empleado a tiempo parcial es:", empleado_tiempo_parcial.calcular_salario_total())