"""BATALLA POKÉMON
/*
 * Crea un programa que calcule el daño de un ataque durante
 * una batalla Pokémon.
 * - La fórmula será la siguiente: daño = 50 * (ataque / defensa) * efectividad
 * - Efectividad: x2 (súper efectivo), x1 (neutral), x0.5 (no es muy efectivo)
 * - Sólo hay 4 tipos de Pokémon: Agua, Fuego, Planta y Eléctrico 
 *   (buscar su efectividad)
 * - El programa recibe los siguientes parámetros:
 *  - Tipo del Pokémon atacante.
 *  - Tipo del Pokémon defensor.
 *  - Ataque: Entre 1 y 100.
 *  - Defensa: Entre 1 y 100.
 */
 """

class Pokemon:
    # Diccionario que contiene las efectividades entre tipos de Pokémon
    efectividad = {
        ("Agua", "Fuego"): 2,
        ("Agua", "Planta"): 0.5,
        ("Agua", "Eléctrico"): 0.5,
        ("Fuego", "Planta"): 2,
        ("Fuego", "Agua"): 0.5,
        ("Fuego", "Eléctrico"): 1,
        ("Planta", "Agua"): 2,
        ("Planta", "Fuego"): 0.5,
        ("Planta", "Eléctrico"): 1,
        ("Eléctrico", "Agua"): 2,
        ("Eléctrico", "Fuego"): 1,
        ("Eléctrico", "Planta"): 1
    }
    
    def __init__(self, tipo, ataque, defensa, hp):
        # Inicializa los atributos del Pokémon
        self.tipo = tipo
        self.ataque = ataque
        self.defensa = defensa
        self.hp = hp  # Vida del Pokémon
    
    def calcular_efectividad(self, tipo_defensor):
        # Calcula la efectividad del ataque según el tipo del defensor
        return self.efectividad.get((self.tipo, tipo_defensor), 1)
    
    def calcular_dano(self, tipo_defensor, defensa):
        # Calcula el daño usando la fórmula dada y la efectividad
        efectividad = self.calcular_efectividad(tipo_defensor)
        return 50 * (self.ataque / defensa) * efectividad
    
    def recibir_dano(self, dano):
        # Reduce la vida (HP) del Pokémon al recibir daño
        self.hp -= dano
        if self.hp < 0:  # Asegura que HP no sea menor que 0
            self.hp = 0

def batalla_pokemon(pokemon1, pokemon2):
    turno = 1
    # Bucle hasta que uno de los Pokémon quede sin vida
    while pokemon1.hp > 0 and pokemon2.hp > 0:
        print(f"--- Turno {turno} ---")
        
        # El Pokémon 1 ataca al Pokémon 2
        dano1 = pokemon1.calcular_dano(pokemon2.tipo, pokemon2.defensa)
        pokemon2.recibir_dano(dano1)
        print(f"{pokemon1.tipo} ataca a {pokemon2.tipo} causando {dano1:.2f} de daño. {pokemon2.tipo} tiene {pokemon2.hp} de HP restante.")
        
        if pokemon2.hp <= 0:
            print(f"{pokemon2.tipo} ha sido derrotado. ¡{pokemon1.tipo} gana!")
            break
        
        # El Pokémon 2 ataca al Pokémon 1
        dano2 = pokemon2.calcular_dano(pokemon1.tipo, pokemon1.defensa)
        pokemon1.recibir_dano(dano2)
        print(f"{pokemon2.tipo} ataca a {pokemon1.tipo} causando {dano2:.2f} de daño. {pokemon1.tipo} tiene {pokemon1.hp} de HP restante.")
        
        if pokemon1.hp <= 0:
            print(f"{pokemon1.tipo} ha sido derrotado. ¡{pokemon2.tipo} gana!")
            break
        
        turno += 1

# Ejemplo de uso
pokemon1 = Pokemon("Agua", 70, 50, 200)
pokemon2 = Pokemon("Fuego", 60, 45, 180)

# Simula la batalla entre los dos Pokémon
batalla_pokemon(pokemon1, pokemon2)