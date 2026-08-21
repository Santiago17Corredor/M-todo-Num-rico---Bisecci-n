# Método de bisección

Aplicación académica en Python para aproximar una raíz positiva de un
polinomio mediante el método de bisección.

## Estado actual

**Versión 0.2 - Método de bisección en consola**

Esta versión incorpora la interpretación de polinomios, el algoritmo de
bisección, el cálculo del error aproximado y el almacenamiento de cada
iteración. Por ahora, el método se prueba desde la consola.

## Archivos

- `main.py`: punto de entrada de la aplicación.
- `biseccion.py`: contiene la interpretación del polinomio y el método de
  bisección.
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
