"""Interfaz gráfica del laboratorio."""

import tkinter as tk


def iniciar_aplicacion():
    """Muestra la ventana inicial de la versión 0.1."""
    ventana = tk.Tk()
    ventana.title("Método de bisección")
    ventana.geometry("480x220")
    ventana.resizable(False, False)

    titulo = tk.Label(
        ventana,
        text="Método de bisección",
        font=("Arial", 18, "bold"),
    )
    titulo.pack(pady=(55, 12))

    descripcion = tk.Label(
        ventana,
        text="Hola porfavor sirve - versión 0.1",
        font=("Arial", 11),
    )
    descripcion.pack()

    ventana.mainloop()
