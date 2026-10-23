"""Comprobaciones numéricas independientes de las ilustraciones."""
import csv
import json
import sys
from pathlib import Path
from statistics import mean

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ))
from ejercicios.soluciones import camino,islas,josephus
from kernel_convolucion.calculo import ENTRADA,convolucion
from evaluacion_a_aterisco.resolver import resolver,vecinos,RUTA_REFERENCIA,MUROS

reinas = [3,1,4,2]
assert len(set(reinas)) == len(set(i-c for i,c in enumerate(reinas))) == len(set(i+c for i,c in enumerate(reinas))) == 4
for n in range(1,31):
    personas = list(range(1,n+1))
    indice = 0
    while len(personas)>1:
        indice = (indice+1)%len(personas)
        personas.pop(indice)
    assert josephus(n) == personas[0]
assert josephus(7,3) == 2

estados = [(3,3),(3,1),(3,2),(3,0),(3,1),(1,1),(2,2),(0,2),(0,3),(0,1),(0,2),(0,0)]
for paso,(antes,despues) in enumerate(zip(estados,estados[1:])):
    cambios = [b-a for a,b in zip(antes,despues)]
    assert 1 <= sum(abs(d) for d in cambios) <= 2
    assert all(d <= 0 for d in cambios) if paso%2 == 0 else all(d >= 0 for d in cambios)
    for m,c in (despues,(3-despues[0],3-despues[1])):
        assert 0 <= m <= 3 and 0 <= c <= 3 and (m == 0 or m >= c)

laberinto = [list(" x   x  "),list(" x x   1"),list("   xxx x")]
ruta = camino(laberinto,(0,0),(1,7))
assert len(ruta)-1 == 12
assert camino([list(" x ")],(0,0),(0,2)) == []
mapa = [[1,1,0,0,0],[1,1,0,0,1],[0,0,0,1,1],[0,0,0,0,0],[1,0,1,0,1]]
assert islas(mapa) == 5 and islas([[1,0],[0,1]]) == 2 and islas([]) == 0
assert mapa[0][0] == 1

esperada = [[118,140,255,93,221],[205,255,255,255,255],[201,255,255,255,255],
            [255,255,255,255,255],[241,255,255,255,255]]
assert convolucion(ENTRADA) == esperada
assert convolucion([[7]]) == [[0]]
assert convolucion([[-1,-2],[-3,-4]]) == [[0,0],[0,0]]
assert convolucion(ENTRADA,False)[0][2] == 271

optima,costo,cerrados = resolver()
assert costo == resolver(usar_heuristica=False)[1] == 102
acumulados = [0]
for a,b in zip(RUTA_REFERENCIA,RUTA_REFERENCIA[1:]):
    assert a not in MUROS and b not in MUROS
    acumulados.append(acumulados[-1]+dict(vecinos(a))[b])
assert acumulados == [0,10,20,34,44,54,64,78,92,102]

with (RAIZ/"dataset_excel/dataset.csv").open() as archivo:
    datos = [[float(x) for x in fila] for fila in csv.reader(archivo) if fila]
assert len(datos) == 150 and all(len(f)==4 for f in datos)
iris = []
for inicio in (0,50,100):
    bloque = datos[inicio:inicio+50]
    iris.append({"filas":[inicio+1,inicio+50],
                 "medias":[round(mean(f[c] for f in bloque),3) for c in range(4)],
                 "rangos":[[min(f[c] for f in bloque),max(f[c] for f in bloque)] for c in range(4)]})
resultados = {"reinas":reinas,"josephus_7":josephus(7),"cruces":11,
              "laberinto_movimientos":len(ruta)-1,"islas":5,
              "convolucion":esperada,"ruta_referencia":RUTA_REFERENCIA,
              "costos_acumulados":acumulados,"costo_astar_y_dijkstra":costo,
              "ruta_algoritmo":optima,"cerrados_algoritmo":cerrados,"iris":iris}
(RAIZ/"verificacion/resultados.json").write_text(json.dumps(resultados,indent=2,ensure_ascii=False),encoding="utf-8")
print("OK: reinas, Josephus, cruces, laberinto, islas, convolución, A*/Dijkstra e Iris.")
