# XOR: corregir la representación y el entrenamiento

La tabla es 00→0, 01→1, 10→1, 11→0. Una sola neurona con frontera lineal no puede separarla. La sigmoide correcta es 1/(1+exp(−z)), no 1/(1−z).

Esta versión conserva un experimento de **entrenamiento**, pero usa una red mínima de dos entradas, dos neuronas ocultas y una salida. Ajusta pesos y sesgos por retropropagación durante 30 000 épocas, con tasa 0.5 e inicialización fija para poder reproducir el resultado. Utiliza error cuadrático y sigmoide estable numéricamente.

Compilar: `gcc percep.c -o percep -lm`. El programa comprueba las cuatro clasificaciones, exige error absoluto menor de 0.1 en cada salida e imprime sus valores. No se presenta como un perceptrón lineal que aprendió XOR ni como una evaluación de generalización: se comprueba la tabla finita completa.
