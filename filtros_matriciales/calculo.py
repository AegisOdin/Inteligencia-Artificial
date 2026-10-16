ENTRADA = [
    [6,18,21,180,18],
    [60,40,13,20,21],
    [70,71,68,41,15],
    [14,16,117,160,160],
    [21,211,216,217,150],
]
KERNEL = [[1,1,1],[1,0,1],[1,1,1]]

def convolucion(matriz, saturar=True):
    if not matriz or not matriz[0] or any(len(f) != len(matriz[0]) for f in matriz):
        raise ValueError("Matriz rectangular no vacía requerida")
    salida = []
    for y,fila in enumerate(matriz):
        nueva = []
        for x in range(len(fila)):
            valor = sum(matriz[a][b]
                        for a in range(y-1,y+2) for b in range(x-1,x+2)
                        if (a,b) != (y,x) and 0 <= a < len(matriz) and 0 <= b < len(fila))
            nueva.append(max(0,min(255,valor)) if saturar else valor)
        salida.append(nueva)
    return salida

if __name__ == "__main__":
    for fila in convolucion(ENTRADA):
        print(fila)
