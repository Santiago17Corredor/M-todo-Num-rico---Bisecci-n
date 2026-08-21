"""Interfaz gráfica del laboratorio."""

import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from biseccion import interpretar_polinomio, metodo_biseccion


AZUL_OSCURO = "#17375e"
AZUL = "#245a91"
DORADO = "#c6a15b"
FONDO = "#f3f5f8"
GRIS = "#7a8491"
PLACEHOLDER = "Ejemplo: x^3 - 4x + 1"


def centrar_ventana(ventana, ancho, alto):
    """Ubica la ventana en el centro de la pantalla."""
    posicion_x = (ventana.winfo_screenwidth() - ancho) // 2
    posicion_y = (ventana.winfo_screenheight() - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{posicion_x}+{posicion_y}")


def crear_campo(contenedor):
    """Crea un campo de entrada con el estilo general del formulario."""
    return tk.Entry(
        contenedor,
        font=("Segoe UI", 11),
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground="#cbd2da",
        highlightcolor=AZUL,
    )


def crear_figura_polinomio(polinomio, xi, xs, raiz):
    """Crea la figura con la curva, el intervalo y la raíz encontrada."""
    funcion = interpretar_polinomio(polinomio)
    margen = max((xs - xi) * 0.15, 0.1)
    inicio = xi - margen
    fin = xs + margen
    cantidad_puntos = 500
    paso = (fin - inicio) / (cantidad_puntos - 1)
    valores_x = [inicio + indice * paso for indice in range(cantidad_puntos)]
    valores_y = [funcion(x) for x in valores_x]

    figura = Figure(figsize=(8.5, 5.2), dpi=100, facecolor="white")
    grafica = figura.add_subplot(111)

    grafica.plot(valores_x, valores_y, color=AZUL, linewidth=2.2, label="f(x)")
    grafica.axhline(0, color="#4d5966", linewidth=1)
    grafica.axvline(0, color="#4d5966", linewidth=1)
    grafica.axvspan(
        xi,
        xs,
        color=DORADO,
        alpha=0.14,
        label=f"Intervalo [{xi:g}, {xs:g}]",
    )
    grafica.axvline(xi, color=DORADO, linestyle="--", linewidth=1)
    grafica.axvline(xs, color=DORADO, linestyle="--", linewidth=1)
    grafica.scatter(
        [raiz],
        [0],
        color="#b23a48",
        edgecolor="white",
        linewidth=1,
        s=75,
        zorder=5,
        label="Raíz encontrada",
    )
    grafica.annotate(
        f"x ≈ {raiz:.6f}",
        xy=(raiz, 0),
        xytext=(12, 18),
        textcoords="offset points",
        color="#8f2633",
        fontweight="bold",
        arrowprops={"arrowstyle": "->", "color": "#8f2633"},
        bbox={"boxstyle": "round,pad=0.3", "fc": "white", "ec": "#d9dee5"},
    )

    grafica.set_title(f"Gráfica de f(x) = {polinomio}", color=AZUL_OSCURO, pad=14)
    grafica.set_xlabel("x")
    grafica.set_ylabel("f(x)")
    grafica.set_xlim(inicio, fin)
    grafica.grid(True, color="#dfe4ea", linewidth=0.7, alpha=0.8)
    grafica.legend(loc="best", frameon=True)
    figura.tight_layout()
    return figura


def crear_tabla_iteraciones(contenedor, iteraciones, ventana):
    """Crea la tabla desplazable con el paso a paso de la bisección."""
    tk.Label(
        contenedor,
        text="Tabla de iteraciones",
        bg="white",
        fg=AZUL_OSCURO,
        font=("Segoe UI", 13, "bold"),
    ).pack(anchor="w", padx=18, pady=(15, 3))

    estado = (
        f"{len(iteraciones)} iteraciones registradas"
        if iteraciones
        else "No se realizaron iteraciones"
    )
    tk.Label(
        contenedor,
        text=estado,
        bg="white",
        fg=GRIS,
        font=("Segoe UI", 9),
    ).pack(anchor="w", padx=18, pady=(0, 10))

    marco_tabla = tk.Frame(contenedor, bg="white")
    marco_tabla.pack(fill="both", expand=True, padx=18, pady=(0, 16))
    marco_tabla.rowconfigure(0, weight=1)
    marco_tabla.columnconfigure(0, weight=1)

    columnas = (
        "iteracion",
        "xi",
        "xs",
        "xr",
        "f_xi",
        "f_xs",
        "f_xr",
        "error",
    )
    titulos = (
        "Iteración",
        "Xi",
        "Xs",
        "Xr",
        "f(Xi)",
        "f(Xs)",
        "f(Xr)",
        "Error",
    )
    anchos = (75, 90, 90, 90, 100, 100, 100, 90)

    estilo = ttk.Style(ventana)
    estilo.configure(
        "Iteraciones.Treeview",
        background="white",
        fieldbackground="white",
        foreground="#283747",
        font=("Segoe UI", 9),
        rowheight=26,
    )
    estilo.configure(
        "Iteraciones.Treeview.Heading",
        background=AZUL,
        foreground="white",
        font=("Segoe UI", 9, "bold"),
    )
    estilo.map(
        "Iteraciones.Treeview",
        background=[("selected", "#d7e6f5")],
        foreground=[("selected", AZUL_OSCURO)],
    )

    tabla = ttk.Treeview(
        marco_tabla,
        columns=columnas,
        show="headings",
        style="Iteraciones.Treeview",
    )
    for columna, titulo, ancho in zip(columnas, titulos, anchos):
        tabla.heading(columna, text=titulo)
        tabla.column(columna, width=ancho, minwidth=70, anchor="center")

    for paso in iteraciones:
        error = "---" if paso["error"] is None else f'{paso["error"]:.6f}'
        tabla.insert(
            "",
            "end",
            values=(
                paso["iteracion"],
                f'{paso["xi"]:.6f}',
                f'{paso["xs"]:.6f}',
                f'{paso["xr"]:.6f}',
                f'{paso["f_xi"]:.6f}',
                f'{paso["f_xs"]:.6f}',
                f'{paso["f_xr"]:.6f}',
                error,
            ),
        )

    desplazamiento_y = ttk.Scrollbar(
        marco_tabla, orient="vertical", command=tabla.yview
    )
    desplazamiento_x = ttk.Scrollbar(
        marco_tabla, orient="horizontal", command=tabla.xview
    )
    tabla.configure(
        yscrollcommand=desplazamiento_y.set,
        xscrollcommand=desplazamiento_x.set,
    )

    tabla.grid(row=0, column=0, sticky="nsew")
    desplazamiento_y.grid(row=0, column=1, sticky="ns")
    desplazamiento_x.grid(row=1, column=0, sticky="ew")
    return tabla


def crear_resumen(contenedor, resultado, xi, xs, ancho_ventana):
    """Muestra los datos finales y genera una conclusión breve."""
    iteraciones = resultado["iteraciones"]
    total = len(iteraciones)

    tk.Label(
        contenedor,
        text="Resumen del procedimiento",
        bg="white",
        fg=AZUL_OSCURO,
        font=("Segoe UI", 12, "bold"),
    ).pack(anchor="w", padx=20, pady=(13, 8))

    datos = tk.Frame(contenedor, bg="white")
    datos.pack(fill="x", padx=20)
    for columna in range(4):
        datos.columnconfigure(columna, weight=1)

    resumen = (
        ("Raíz encontrada", f'{resultado["raiz"]:.6f}'),
        ("Total de iteraciones", str(total)),
        ("Error final", f'{resultado["error_final"]:.6f}'),
        ("Intervalo utilizado", f"[{xi:.6f}, {xs:.6f}]"),
    )
    for columna, (titulo, valor) in enumerate(resumen):
        bloque = tk.Frame(datos, bg="white")
        bloque.grid(row=0, column=columna, sticky="ew", padx=(0, 18))
        tk.Label(
            bloque,
            text=titulo,
            bg="white",
            fg=GRIS,
            font=("Segoe UI", 8),
        ).pack(anchor="w")
        tk.Label(
            bloque,
            text=valor,
            bg="white",
            fg=AZUL_OSCURO,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")

    if resultado["extremo_raiz"]:
        conclusion = (
            f'El límite {resultado["extremo_raiz"]} ingresado corresponde '
            "exactamente a una raíz del polinomio, por lo que no fue necesario "
            "aplicar iteraciones del método de bisección."
        )
    else:
        palabra_iteracion = "iteración" if total == 1 else "iteraciones"
        conclusion = (
            f'Se encontró una raíz aproximada en x = {resultado["raiz"]:.6f} '
            f"después de {total} {palabra_iteracion}, cumpliendo con la "
            "tolerancia establecida."
        )

    tk.Label(
        contenedor,
        text="Conclusión: " + conclusion,
        bg="white",
        fg="#3f4a56",
        font=("Segoe UI", 9),
        justify="left",
        anchor="w",
        wraplength=ancho_ventana - 90,
    ).pack(fill="x", padx=20, pady=(10, 13))


def mostrar_ventana_resultados(ventana_entrada, polinomio, xi, xs, resultado):
    """Oculta el formulario y muestra la integración completa de resultados."""
    ventana_entrada.withdraw()

    ventana_resultado = tk.Toplevel(ventana_entrada)
    ventana_resultado.title("Resultados - Método de bisección")
    ventana_resultado.configure(bg=FONDO)
    ancho = min(1450, ventana_resultado.winfo_screenwidth() - 60)
    alto = min(850, ventana_resultado.winfo_screenheight() - 80)
    ventana_resultado.minsize(min(1050, ancho), min(650, alto))
    centrar_ventana(ventana_resultado, ancho, alto)

    encabezado = tk.Frame(ventana_resultado, bg=AZUL_OSCURO, height=74)
    encabezado.pack(fill="x")
    encabezado.pack_propagate(False)
    tk.Label(
        encabezado,
        text="Resultados del método de bisección",
        bg=AZUL_OSCURO,
        fg="white",
        font=("Segoe UI", 18, "bold"),
    ).pack(pady=(14, 1))
    tk.Label(
        encabezado,
        text=f"f(x) = {polinomio}",
        bg=AZUL_OSCURO,
        fg="#dce6f1",
        font=("Segoe UI", 9),
    ).pack()

    contenido = tk.Frame(ventana_resultado, bg=FONDO)
    contenido.pack(fill="both", expand=True, padx=22, pady=(18, 10))
    contenido.rowconfigure(0, weight=1)
    contenido.columnconfigure(0, weight=5)
    contenido.columnconfigure(1, weight=6)

    contenedor_grafica = tk.Frame(contenido, bg="white", bd=1, relief="solid")
    contenedor_grafica.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
    tk.Label(
        contenedor_grafica,
        text="Gráfica del polinomio",
        bg="white",
        fg=AZUL_OSCURO,
        font=("Segoe UI", 13, "bold"),
    ).pack(anchor="w", padx=18, pady=(15, 3))
    tk.Label(
        contenedor_grafica,
        text="El área dorada representa el intervalo utilizado",
        bg="white",
        fg=GRIS,
        font=("Segoe UI", 9),
    ).pack(anchor="w", padx=18, pady=(0, 4))

    figura = crear_figura_polinomio(polinomio, xi, xs, resultado["raiz"])
    lienzo = FigureCanvasTkAgg(figura, master=contenedor_grafica)
    lienzo.draw()
    lienzo.get_tk_widget().pack(fill="both", expand=True)
    ventana_resultado.lienzo = lienzo

    contenedor_tabla = tk.Frame(contenido, bg="white", bd=1, relief="solid")
    contenedor_tabla.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
    tabla = crear_tabla_iteraciones(
        contenedor_tabla, resultado["iteraciones"], ventana_resultado
    )
    ventana_resultado.tabla = tabla

    contenedor_resumen = tk.Frame(
        ventana_resultado, bg="white", bd=1, relief="solid"
    )
    contenedor_resumen.pack(fill="x", padx=22, pady=(0, 10))
    crear_resumen(contenedor_resumen, resultado, xi, xs, ancho)

    def volver():
        ventana_resultado.destroy()
        ventana_entrada.deiconify()

    acciones = tk.Frame(ventana_resultado, bg=FONDO)
    acciones.pack(fill="x", padx=22, pady=(0, 16))
    tk.Button(
        acciones,
        text="Nueva consulta",
        command=volver,
        bg=AZUL,
        fg="white",
        activebackground=AZUL_OSCURO,
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=18,
        pady=7,
    ).pack(side="right")

    ventana_resultado.protocol("WM_DELETE_WINDOW", ventana_entrada.destroy)


def crear_ventana_entrada():
    """Construye la ventana para ingresar los datos del método."""
    ventana = tk.Tk()
    ventana.title("Método de bisección")
    ventana.configure(bg=FONDO)
    ventana.resizable(False, False)
    centrar_ventana(ventana, 640, 555)

    encabezado = tk.Frame(ventana, bg=AZUL_OSCURO, height=120)
    encabezado.pack(fill="x")
    encabezado.pack_propagate(False)

    tk.Label(
        encabezado,
        text="Método de bisección",
        bg=AZUL_OSCURO,
        fg="white",
        font=("Segoe UI", 21, "bold"),
    ).pack(pady=(24, 4))
    tk.Label(
        encabezado,
        text="Laboratorio de Métodos Numéricos",
        bg=AZUL_OSCURO,
        fg="#dce6f1",
        font=("Segoe UI", 10),
    ).pack()

    tk.Frame(ventana, bg=DORADO, height=4).pack(fill="x")

    formulario = tk.Frame(ventana, bg="white", padx=35, pady=25)
    formulario.pack(fill="both", padx=55, pady=28)
    formulario.columnconfigure(0, weight=1)
    formulario.columnconfigure(1, weight=1)

    estilo_etiqueta = {
        "bg": "white",
        "fg": AZUL_OSCURO,
        "font": ("Segoe UI", 10, "bold"),
        "anchor": "w",
    }

    tk.Label(formulario, text="Polinomio f(x)", **estilo_etiqueta).grid(
        row=0, column=0, columnspan=2, sticky="ew"
    )
    campo_polinomio = crear_campo(formulario)
    campo_polinomio.grid(
        row=1, column=0, columnspan=2, sticky="ew", ipady=7, pady=(5, 17)
    )
    campo_polinomio.insert(0, PLACEHOLDER)
    campo_polinomio.configure(fg=GRIS)

    def quitar_placeholder(event):
        if campo_polinomio.get() == PLACEHOLDER:
            campo_polinomio.delete(0, tk.END)
            campo_polinomio.configure(fg=AZUL_OSCURO)

    def restaurar_placeholder(event):
        if not campo_polinomio.get().strip():
            campo_polinomio.insert(0, PLACEHOLDER)
            campo_polinomio.configure(fg=GRIS)

    campo_polinomio.bind("<FocusIn>", quitar_placeholder)
    campo_polinomio.bind("<FocusOut>", restaurar_placeholder)

    tk.Label(formulario, text="Límite inferior Xi", **estilo_etiqueta).grid(
        row=2, column=0, sticky="ew", padx=(0, 8)
    )
    tk.Label(formulario, text="Límite superior Xs", **estilo_etiqueta).grid(
        row=2, column=1, sticky="ew", padx=(8, 0)
    )

    campo_xi = crear_campo(formulario)
    campo_xi.grid(row=3, column=0, sticky="ew", ipady=7, padx=(0, 8), pady=(5, 17))
    campo_xs = crear_campo(formulario)
    campo_xs.grid(row=3, column=1, sticky="ew", ipady=7, padx=(8, 0), pady=(5, 17))

    tk.Label(formulario, text="Error o tolerancia", **estilo_etiqueta).grid(
        row=4, column=0, columnspan=2, sticky="ew"
    )
    campo_tolerancia = crear_campo(formulario)
    campo_tolerancia.grid(
        row=5, column=0, columnspan=2, sticky="ew", ipady=7, pady=(5, 20)
    )

    def calcular():
        polinomio = campo_polinomio.get()
        if polinomio == PLACEHOLDER:
            polinomio = ""

        try:
            resultado = metodo_biseccion(
                polinomio,
                campo_xi.get(),
                campo_xs.get(),
                campo_tolerancia.get(),
            )
        except ValueError as error:
            messagebox.showerror("Datos no válidos", str(error), parent=ventana)
            return

        mostrar_ventana_resultados(
            ventana,
            polinomio,
            float(campo_xi.get()),
            float(campo_xs.get()),
            resultado,
        )

    boton_calcular = tk.Button(
        formulario,
        text="Calcular",
        command=calcular,
        bg=AZUL,
        fg="white",
        activebackground=AZUL_OSCURO,
        activeforeground="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        cursor="hand2",
        pady=9,
    )
    boton_calcular.grid(row=6, column=0, columnspan=2, sticky="ew")

    tk.Label(
        ventana,
        text="Ingrese un intervalo positivo que contenga un cambio de signo.",
        bg=FONDO,
        fg=GRIS,
        font=("Segoe UI", 9),
    ).pack(pady=(0, 18))

    ventana.bind("<Return>", lambda event: calcular())
    ventana.focus_set()
    return ventana


def iniciar_aplicacion():
    """Inicia la interfaz gráfica."""
    ventana = crear_ventana_entrada()
    ventana.mainloop()
