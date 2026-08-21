import ast
import math
import re


def interpretar_polinomio(texto):
    expresion = texto.lower().replace(" ", "").replace("^", "**")

    # Acepta formas comunes como 4x y x^2.
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
        if isinstance(nodo, ast.Constant) and type(nodo.value) not in (int, float):
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


def validar_datos(polinomio, xi, xs, tolerancia):
    campos = (polinomio, xi, xs, tolerancia)
    if any(valor is None or str(valor).strip() == "" for valor in campos):
        raise ValueError("Todos los campos son obligatorios.")

    try:
        xi = float(xi)
        xs = float(xs)
        tolerancia = float(tolerancia)
    except (TypeError, ValueError):
        raise ValueError("Xi, Xs y la tolerancia deben ser números.") from None

    if not all(math.isfinite(valor) for valor in (xi, xs, tolerancia)):
        raise ValueError("Xi, Xs y la tolerancia deben ser números finitos.")
    if xi < 0 or xs < 0:
        raise ValueError("El intervalo debe corresponder a valores no negativos.")
    if xi >= xs:
        raise ValueError("El límite inferior Xi debe ser menor que Xs.")
    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser un número positivo.")

    try:
        funcion = interpretar_polinomio(str(polinomio).strip())
        f_xi = funcion(xi)
        f_xs = funcion(xs)
    except (ArithmeticError, SyntaxError, TypeError, ValueError):
        raise ValueError("El polinomio ingresado no es válido.") from None

    if not all(math.isfinite(valor) for valor in (f_xi, f_xs)):
        raise ValueError("El polinomio no produce valores numéricos válidos.")

    if f_xi != 0 and f_xs != 0 and f_xi * f_xs >= 0:
        raise ValueError(
            "El intervalo ingresado no cumple las condiciones necesarias "
            "para aplicar el método de bisección."
        )

    return funcion, xi, xs, tolerancia, f_xi, f_xs


def metodo_biseccion(polinomio, xi, xs, tolerancia):
    funcion, xi, xs, tolerancia, f_xi, f_xs = validar_datos(
        polinomio, xi, xs, tolerancia
    )

    if f_xi == 0:
        return {
            "raiz": xi,
            "iteraciones": [],
            "error_final": 0.0,
            "extremo_raiz": "inferior",
        }
    if f_xs == 0:
        return {
            "raiz": xs,
            "iteraciones": [],
            "error_final": 0.0,
            "extremo_raiz": "superior",
        }

    iteraciones = []
    xr_anterior = None

    # Repite hasta alcanzar la tolerancia.
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
                "extremo_raiz": None,
            }

        if f_xi * f_xr < 0:
            xs = xr
            f_xs = f_xr
        else:
            xi = xr
            f_xi = f_xr

        xr_anterior = xr


def mostrar_resultado(resultado):
    iteraciones = resultado["iteraciones"]

    if not iteraciones:
        extremo = resultado["extremo_raiz"]
        print(f"\nEl límite {extremo} corresponde exactamente a una raíz.")
    else:
        encabezado = (
            f'{"Iteración":^10} | {"Xi":^12} | {"Xs":^12} | {"Xr":^12} | '
            f'{"f(Xi)":^13} | {"f(Xs)":^13} | {"f(Xr)":^13} | {"Error":^12}'
        )
        print("\n" + encabezado)
        print("-" * len(encabezado))

        for paso in iteraciones:
            error = "---" if paso["error"] is None else f'{paso["error"]:.6f}'
            print(
                f'{paso["iteracion"]:^10} | '
                f'{paso["xi"]:^12.6f} | '
                f'{paso["xs"]:^12.6f} | '
                f'{paso["xr"]:^12.6f} | '
                f'{paso["f_xi"]:^13.6f} | '
                f'{paso["f_xs"]:^13.6f} | '
                f'{paso["f_xr"]:^13.6f} | '
                f'{error:^12}'
            )

    print(f'\nRaíz aproximada: {resultado["raiz"]:.6f}')
    print(f'Total de iteraciones: {len(iteraciones)}')
    print(f'Error final: {resultado["error_final"]:.6f}')


def ejecutar_prueba_consola():
    print("Prueba del método de bisección - versión 0.3")
    polinomio = input("Polinomio f(x): ")
    xi = input("Límite inferior Xi: ")
    xs = input("Límite superior Xs: ")
    tolerancia = input("Tolerancia: ")

    try:
        resultado = metodo_biseccion(polinomio, xi, xs, tolerancia)
        mostrar_resultado(resultado)
    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    ejecutar_prueba_consola()
