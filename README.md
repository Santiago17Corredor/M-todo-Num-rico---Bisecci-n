# Método de bisección

Aplicación académica en Python para aproximar una raíz positiva de un
polinomio mediante el método de bisección.

## Estado actual

**Versión 0.3 - Validaciones y tabla de iteraciones**

Esta versión incorpora validaciones básicas para los datos, conserva el paso a
paso completo del método y presenta los resultados en una tabla de consola.
La interfaz gráfica funcional se agregará en la versión 0.4.

## Archivos

- `main.py`: punto de entrada de la aplicación.
- `biseccion.py`: contiene la interpretación del polinomio, las validaciones,
  el método de bisección y la tabla de consola.
- `interfaz.py`: contiene la ventana inicial.
- `README.md`: documentación del proyecto.

## Ejecución

Se requiere Python 3 con Tkinter. Desde la carpeta del proyecto, ejecutar:

```bash
python main.py
```

Para probar el método desde la consola, ejecutar:

```bash
python biseccion.py
```

Un caso sencillo de prueba es:

- Polinomio: `x^3 - 4x + 1`
- Xi: `0.1`
- Xs: `1`
- Tolerancia: `0.001`
# Metodo Numerico Biseccion
Programa en Python con interfaz que aplica el metodo numérico bisección a una ecuación polinómica de grado n
