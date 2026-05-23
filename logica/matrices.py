import numpy as np


def producto_interno(A, B):
    return np.sum(A * B)


def proseso_ortogonal(conjunto_matrices):
    n = len(conjunto_matrices)
    for i in range(n):
        for j in range(i + 1, n):
            producto = producto_interno(conjunto_matrices[i], conjunto_matrices[j])
            if not np.isclose(producto, 0):
                return False
    return True


def proseso_ortonormal(conjunto_matrices, ortogonal):
    if ortogonal:
        for M in conjunto_matrices:
            norma = np.linalg.norm(M, 'fro')
            if not np.isclose(norma, 1):
                return False
        return True
    else:
        return False


def ortogonalizar(conjunto_matrices):
    shape = np.array(conjunto_matrices[0]).shape
    ortogonales = []
    for M in conjunto_matrices:
        W = np.array(M, dtype=float)
        for U in ortogonales:
            norm_sq = producto_interno(U, U)
            if not np.isclose(norm_sq, 0):
                W = W - (producto_interno(W, U) / norm_sq) * U
        if not np.allclose(W, 0):
            ortogonales.append(W)
    if not ortogonales:
        return np.zeros((0, *shape))
    return np.round(np.array(ortogonales), decimals=10)


def ortonormalizar(conjunto_matrices):
    ortogonales = ortogonalizar(conjunto_matrices)
    ortonormales = []
    for M in ortogonales:
        norma = np.linalg.norm(M, 'fro')
        if not np.isclose(norma, 0):
            ortonormales.append(M / norma)
    if not ortonormales:
        return np.zeros((0, *ortogonales.shape[1:]))
    return np.round(np.array(ortonormales), decimals=10)


def diagnosticar_matrices(arr, m, n_val):
    dim_espacio = m * n_val
    num = arr.shape[0]
    rango = np.linalg.matrix_rank(arr.reshape(num, dim_espacio))
    li = rango == num
    gen = rango == dim_espacio
    base = li and gen
    ort = proseso_ortogonal(arr)
    orton = proseso_ortonormal(arr, ort)
    return {
        "rango": rango,
        "num": num,
        "dim": dim_espacio,
        "m": m,
        "n": n_val,
        "li": li,
        "gen": gen,
        "base": base,
        "ortogonal": ort,
        "ortonormal": orton,
    }
