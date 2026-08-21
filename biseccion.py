"""Lógica matemática del método de bisección."""

import ast
import re


def interpretar_polinomio(texto):
    """Convierte un texto como ``x^3 - 4x + 1`` en una función evaluable."""
    expresion = texto.lower().replace(" ", "").replace("^", "**")

    # Agrega la multiplicación que normalmente se omite al escribir polinomios.
    expresion = re.sub(r"(?<=\d)(?=[x(])", "*", expresion)
    expresion = re.sub(r"(?<=[x)])(?=\()", "*", expresion)
    expresion = re.sub(r"(?<=\))(?=[x\d])", "*", expresion)

    arbol = ast.parse(expresion, mode="eval")
    nodos_permitidos = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Pow,
        ast.UAdd,
        ast.USub,
        ast.Name,
        ast.Load,
        ast.Constant,
    )

    for nodo in ast.walk(arbol):
        if not isinstance(nodo, nodos_permitidos):
            raise ValueError("La expresión contiene una operación no permitida.")
        if isinstance(nodo, ast.Name) and nodo.id != "x":
            raise ValueError("La única variable permitida es x.")
        if isinstance(nodo, ast.Constant) and not isinstance(nodo.value, (int, float)):
            raise ValueError("El polinomio solo puede contener números.")
        if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, ast.Pow):
            exponente = nodo.right
            if not (
                isinstance(exponente, ast.Constant)
                and isinstance(exponente.value, int)
                and exponente.value >= 0
            ):
                raise ValueError("Los exponentes deben ser enteros no negativos.")

    codigo = compile(arbol, "<polinomio>", "eval")

    def evaluar(x):
        return eval(codigo, {"__builtins__": {}}, {"x": x})

    return evaluar


def metodo_biseccion(polinomio, xi, xs, tolerancia):
    """Aproxima una raíz y devuelve el resultado junto con sus iteraciones.

    En esta versión se supone que el intervalo y la tolerancia son adecuados.
    Las validaciones completas se agregarán en la versión 0.3.
    """
    funcion = interpretar_polinomio(polinomio)
    f_xi = funcion(xi)
    f_xs = funcion(xs)

    if f_xi == 0:
        return {"raiz": xi, "iteraciones": [], "error_final": 0.0}
    if f_xs == 0:
        return {"raiz": xs, "iteraciones": [], "error_final": 0.0}

    iteraciones = []
    xr_anterior = None

    while True:
        xr = (xi + xs) / 2
        f_xr = funcion(xr)
        error = None

        if xr_anterior is not None:
            error = abs((xr - xr_anterior) / xr)

        iteraciones.append(
            {
                "iteracion": len(iteraciones) + 1,
                "xi": xi,
                "xs": xs,
                "xr": xr,
                "f_xi": f_xi,
                "f_xs": f_xs,
                "f_xr": f_xr,
                "error": error,
            }
        )

        if f_xr == 0 or (error is not None and error <= tolerancia):
            return {
                "raiz": xr,
                "iteraciones": iteraciones,
                "error_final": 0.0 if f_xr == 0 else error,
            }

        if f_xi * f_xr < 0:
            xs = xr
            f_xs = f_xr
        else:
            xi = xr
            f_xi = f_xr

        xr_anterior = xr


def ejecutar_prueba_consola():
    """Solicita un caso sencillo y muestra las iteraciones en la consola."""
    print("Prueba del método de bisección - versión 0.2")
    polinomio = input("Polinomio f(x): ")
    xi = float(input("Límite inferior Xi: "))
    xs = float(input("Límite superior Xs: "))
    tolerancia = float(input("Tolerancia: "))

    resultado = metodo_biseccion(polinomio, xi, xs, tolerancia)

    print("\nIteraciones realizadas:")
    if not resultado["iteraciones"]:
        print("No se necesitaron iteraciones: un extremo es una raíz.")

    for paso in resultado["iteraciones"]:
        error = "---" if paso["error"] is None else f'{paso["error"]:.6f}'
        print(
            f'{paso["iteracion"]:>3}: '
            f'Xi={paso["xi"]:.6f}, '
            f'Xs={paso["xs"]:.6f}, '
            f'Xr={paso["xr"]:.6f}, '
            f'f(Xr)={paso["f_xr"]:.6f}, '
            f'Error={error}'
        )

    print(f'\nRaíz aproximada: {resultado["raiz"]:.6f}')


if __name__ == "__main__":
    ejecutar_prueba_consola()
