# Captura con Haar

Ejecutar `python captura_rostros/haarcascade.py dataset/persona_01`. Espacio guarda los rostros visibles y Escape cierra. Cambiar de carpeta al cambiar de persona; no mezclar identidades. La captura se inicia únicamente al ejecutar el programa.

Los recortes se guardan en gris a 100×100 con un identificador de sesión para evitar sobrescrituras. La cámara se libera incluso si falla una lectura. Haar detecta una región parecida a un rostro; no identifica a la persona.

El XML incluido se conserva como recurso de OpenCV con su licencia y procedencia; no se regenera un clasificador entrenado como si fuera una imagen. El programa carga el equivalente distribuido con OpenCV.
