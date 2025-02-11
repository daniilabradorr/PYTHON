import tkinter as tk
from tkinter import messagebox
import timeit
import random

# ------------------------------
# CLASE PARA MANEJAR EL TEXTO
# ------------------------------
class Texto():
    def __init__(self, texto):
        """Inicializa la clase con un texto y lo divide en frases separadas por puntos o comas."""
        self.texto = texto
        # Separa las frases reemplazando comas por puntos y dividiendo en fragmentos
        self.frases = [frase.strip() for frase in texto.replace(",", ".").split(".") if frase.strip()]

    def obtener_frase(self):
        """Devuelve una frase aleatoria sin repetir inmediatamente hasta que se agoten todas."""
        if not hasattr(self, 'frases_disponibles') or not self.frases_disponibles:
            # Cuando se terminan las frases, se vuelve a mezclar toda la lista
            self.frases_disponibles = random.sample(self.frases, len(self.frases))
        return self.frases_disponibles.pop()
    
# ------------------------------------------
# CLASE PRINCIPAL QUE CONTROLA LA INTERFAZ
# ------------------------------------------
class PruebaEscritura:
    def __init__(self, root, texto):
        """Inicializa la interfaz gráfica y configura la prueba de escritura."""
        self.root = root
        self.texto = texto
        self.inicio_tiempo = None  # Variable para registrar el tiempo de inicio

        # Configuración de la ventana principal
        self.root.title("Prueba de Escritura Veloz")
        self.root.geometry("800x400")

        # Etiqueta que mostrará la frase a escribir
        self.label_frase = tk.Label(root, text="", font=("Arial", 14), wraplength=500, justify="center")
        self.label_frase.pack(pady=20)

        # Campo de entrada donde el usuario escribirá la frase
        self.entrada_texto = tk.Entry(root, font=("Arial", 12), width=50)
        self.entrada_texto.pack(pady=10)
        self.entrada_texto.bind("<KeyPress>", self.iniciar_tiempo)  # Detecta cuando el usuario empieza a escribir
        self.entrada_texto.bind("<Return>", self.verificar_respuesta)  # Verifica cuando presiona Enter

        # Botón manual para verificar la respuesta
        self.boton_verificar = tk.Button(root, text="Verificar", command=self.verificar_respuesta, font=("Arial", 12))
        self.boton_verificar.pack(pady=10)

        # Etiqueta donde se mostrará el resultado
        self.label_resultado = tk.Label(root, text="", font=("Arial", 12))
        self.label_resultado.pack(pady=10)

        # Inicia la primera prueba
        self.nueva_prueba()

    def nueva_prueba(self):
        """Muestra una nueva frase aleatoria y resetea el campo de entrada."""
        self.frase_actual = self.texto.obtener_frase()
        self.label_frase.config(text=self.frase_actual)
        self.entrada_texto.delete(0, tk.END)  # Borra el texto ingresado anteriormente
        self.label_resultado.config(text="")  # Borra el resultado anterior
        self.inicio_tiempo = None  # Resetea el tiempo de inicio

    def iniciar_tiempo(self, event):
        """Inicia el cronómetro en la primera pulsación de tecla."""
        if self.inicio_tiempo is None:
            self.inicio_tiempo = timeit.default_timer()

    def verificar_respuesta(self, event=None):
        """Verifica si la entrada del usuario es correcta y muestra el tiempo transcurrido."""
        if self.inicio_tiempo is None:
            messagebox.showwarning("Error", "Debes empezar a escribir antes de enviar.")
            return

        tiempo_transcurrido = timeit.default_timer() - self.inicio_tiempo
        entrada_usuario = self.entrada_texto.get().strip()

        if entrada_usuario == self.frase_actual:
            mensaje = f"¡Correcto! Tiempo: {tiempo_transcurrido:.2f} segundos"
            self.label_resultado.config(text=mensaje, fg="green")
        else:
            mensaje = "Error en la escritura. Intenta de nuevo."
            self.label_resultado.config(text=mensaje, fg="red")

        self.root.after(2000, self.nueva_prueba)  # Muestra una nueva frase después de 2 segundos

# ------------------------------------------
# INICIALIZACIÓN DEL PROGRAMA
# ------------------------------------------
if __name__ == "__main__":
    texto_prueba = (
        "La programación es una habilidad fundamental en el mundo actual. "
        "Con Python, se pueden realizar tareas complejas de forma sencilla. "
        "Este programa te ayudará a mejorar tu velocidad y precisión al escribir. "
        "Recuerda que la práctica hace al maestro. "
        "¿Cuánto tiempo tardarás en escribir correctamente cada frase? "
        "Pon a prueba tu velocidad y mejora cada día. "
        "Aprender a programar es un viaje emocionante y lleno de retos. "
        "¡Buena suerte en tu prueba de escritura veloz!"
    )
    root = tk.Tk()
    app = PruebaEscritura(root, Texto(texto_prueba))
    root.mainloop()
