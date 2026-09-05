from heapq import heappush, heappop

MUROS = {12,16,21,25,30,34,39,40,41,42,43}
RUTA_REFERENCIA = [5,6,7,17,26,35,44,52,60,59]

def coordenadas(n):
    return divmod(n-1,9)

def vecinos(n):
    y,x = coordenadas(n)
    for dy,dx in ((0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)):
        a,b = y+dy,x+dx
        numero = a*9+b+1
        if 0 <= a < 7 and 0 <= b < 9 and numero not in MUROS:
            yield numero, 14 if dy and dx else 10

def heuristica(n, meta):
    y,x = coordenadas(n)
    a,b = coordenadas(meta)
    dy,dx = abs(y-a),abs(x-b)
    return 14*min(dy,dx)+10*abs(dy-dx)

def resolver(inicio=5, meta=59, usar_heuristica=True):
    if any(n < 1 or n > 63 or n in MUROS for n in (inicio,meta)):
        raise ValueError("Extremos inválidos")
    abiertos, costos, padres, cerrados = [(0,0,inicio)], {inicio:0}, {inicio:None}, []
    while abiertos:
        _,g,n = heappop(abiertos)
        if g != costos[n]:
            continue
        cerrados.append(n)
        if n == meta:
            ruta = []
            while n is not None:
                ruta.append(n)
                n = padres[n]
            return ruta[::-1],g,cerrados
        for v,paso in vecinos(n):
            nuevo = g+paso
            if nuevo < costos.get(v,float("inf")):
                costos[v],padres[v] = nuevo,n
                h = heuristica(v,meta) if usar_heuristica else 0
                heappush(abiertos,(nuevo+h,nuevo,v))
    return [],float("inf"),cerrados

if __name__ == "__main__":
    print(resolver())
