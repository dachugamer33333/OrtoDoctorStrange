import numpy as np

def diagnostico_vectores():
    vectores=[[1,90,1,2], [0,2,0,9], [0,0,1,0], [0,0,1,0]]
    matriz = np.array(vectores)
    print(matriz)
    rango        = np.linalg.matrix_rank(matriz)
    num_vectores = len(vectores)       # 3
    dimension    = len(vectores[0])    # 4 ← aquí estaba el bug

    li  = rango == num_vectores        # 3 == 3 → True  ✓
    gen = rango == dimension           # 3 == 4 → False ✓
    base = li and gen                  # False  ✓

    print(f"Rango: {rango}")
    print(f"Lin. independiente: {li}")
    print(f"Generador: {gen}")
    print(f"Base: {base}")