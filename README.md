# Método de bisección

Aplicación académica en Python para aproximar una raíz positiva de un
polinomio mediante el método de bisección.

## Estado actual

**Versión 0.6 - Integración completa**

Esta versión incorpora la ventana completa de resultados. Presenta la gráfica
del polinomio, la tabla desplazable con todas las iteraciones, el resumen del
procedimiento y una conclusión automática.

## Archivos

- `main.py`: punto de entrada de la aplicación.
- `biseccion.py`: contiene la interpretación del polinomio, las validaciones,
  el método de bisección y la tabla de consola.
- `interfaz.py`: contiene el formulario de entrada y la ventana completa de
  resultados con gráfica, tabla, resumen y conclusión.
- `README.md`: documentación del proyecto.

## Ejecución

Se requiere Python 3 con Tkinter y Matplotlib. Para instalar Matplotlib:

```bash
pip install matplotlib
```

Desde la carpeta del proyecto, ejecutar:

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
