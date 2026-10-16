# Entrenar Eigenfaces

Ejecutar `python modelo_eigenfaces/eigenfacerecognizer.py ruta/al/dataset --salida modelos/eigenfaces.xml`. Debe haber una subcarpeta por identidad con recortes de rostros. El mismo cargador se comparte con la comparación de tres métodos para mantener el preprocesamiento.

Convierte a escala de grises y 100×100, descarta archivos no legibles y conserva un JSON con el orden de etiquetas. No hay datos de rostros reales incluidos ni se presume una tasa de reconocimiento.
