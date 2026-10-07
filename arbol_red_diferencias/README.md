# Árboles de decisión y redes multicapa

| Aspecto | Árbol | MLP |
|---|---|---|
| Representación | Reglas y particiones | Capas con pesos, sesgos y activaciones |
| Aprendizaje | Divisiones que reducen impureza | Gradientes de una función de pérdida |
| Predicción | Ruta de raíz a hoja | Propagación por capas |
| Escalado | Normalmente innecesario | Habitualmente importante |
| Explicación | Clara en árboles pequeños | Interacciones difíciles de resumir |
| Riesgos | Sobreajuste, varianza, decisiones voraces | Sobreajuste, ajuste de hiperparámetros |

El árbol aprende umbrales como `distancia <= t`; la MLP compone transformaciones `h = activación(Wx+b)`. Ambos representan relaciones no lineales. Ninguno gana siempre. Un árbol enorme deja de ser legible y una salida probabilística no garantiza calibración.

## Láminas
1. [Capacidades MLP](1.png)
2. [Límites MLP y definición del árbol](2.png)
3. [Ventajas y límites del árbol](3.png)
4. [Diferencia matemática](4.png)
5. [Entrada y predicción](5.png)
6. [Entrenamiento](6.png)
7. [Características y resultado](7.png)

Para el juego, un árbol pequeño permite inspeccionar decisiones con pocas entradas. Evaluar cualquier alternativa sobre los mismos datos reservados y considerar el costo de cada error.

## Detalles del ajuste

La MLP puede ampliar capas y neuronas, pero aumenta su costo de c?mputo y memoria. La optimizaci?n suele ser no convexa; tasa de aprendizaje, activaci?n, lotes, ?pocas y regularizaci?n afectan al resultado. Un ?rbol selecciona caracter?sticas impl?citamente al dividir; su entrenamiento suele ser r?pido en problemas peque?os, pero las decisiones locales voraces no garantizan el mejor ?rbol global. La profundidad insuficiente tambi?n puede causar subajuste.

Fuentes: [?rboles en scikit-learn](https://sklearn.org/stable/modules/tree.html) y [redes multicapa](https://github.com/scikit-learn/scikit-learn/blob/main/doc/modules/neural_networks_supervised.rst).
