from collections import deque

def josephus(n, inicio=1):
    if n < 1 or not 1 <= inicio <= n:
        raise ValueError("n e inicio fuera de rango")
    potencia = 1 << (n.bit_length() - 1)
    return (2 * (n - potencia) + inicio - 1) % n + 1

def camino(mapa, inicio, meta):
    if not mapa or not mapa[0] or any(len(f) != len(mapa[0]) for f in mapa):
        raise ValueError("Matriz rectangular no vacía requerida")
    filas, columnas = len(mapa), len(mapa[0])
    for f,c in (inicio, meta):
        if not (0 <= f < filas and 0 <= c < columnas) or mapa[f][c] == "x":
            raise ValueError("Extremo inválido")
    padres, cola = {inicio: None}, deque([inicio])
    while cola:
        actual = cola.popleft()
        if actual == meta:
            ruta = []
            while actual is not None:
                ruta.append(actual)
                actual = padres[actual]
            return ruta[::-1]
        f,c = actual
        for vecino in ((f-1,c),(f+1,c),(f,c-1),(f,c+1)):
            y,x = vecino
            if 0 <= y < filas and 0 <= x < columnas and mapa[y][x] != "x" and vecino not in padres:
                padres[vecino] = actual
                cola.append(vecino)
    return []

def islas(mapa):
    if not mapa:
        return 0
    if any(len(f) != len(mapa[0]) for f in mapa):
        raise ValueError("Matriz irregular")
    vistos, total = set(), 0
    for f,fila in enumerate(mapa):
        for c,valor in enumerate(fila):
            if valor != 1 or (f,c) in vistos:
                continue
            total += 1
            pila = [(f,c)]
            vistos.add((f,c))
            while pila:
                y,x = pila.pop()
                for a,b in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
                    if 0 <= a < len(mapa) and 0 <= b < len(fila) and mapa[a][b] == 1 and (a,b) not in vistos:
                        vistos.add((a,b))
                        pila.append((a,b))
    return total
