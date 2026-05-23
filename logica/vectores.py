import numpy as np


def proseso_ortogonal(conjunto_vectores):
    n = len(conjunto_vectores)
    for i in range(n):
        for j in range(i + 1, n):
            producto = np.dot(conjunto_vectores[i], conjunto_vectores[j])
            if not np.isclose(producto, 0):
                return False
    return True


def proseso_ortonormal(conjunto_vectores, ortogonal):
    if ortogonal:
        for v in conjunto_vectores:
            norma = np.linalg.norm(v)
            if not np.isclose(norma, 1):
                return False
        return True
    else:
        return False


def ortogonalizar(conjunto_vectores):
    dim = np.array(conjunto_vectores[0]).shape[0]
    ortogonales = []
    for v in conjunto_vectores:
        w = np.array(v, dtype=float)
        for u in ortogonales:
            norm_sq = np.dot(u, u)
            if not np.isclose(norm_sq, 0):
                w = w - (np.dot(w, u) / norm_sq) * u
        if not np.allclose(w, 0):
            ortogonales.append(w)
    if not ortogonales:
        return np.zeros((0, dim))
    return np.round(np.array(ortogonales), decimals=10)


def ortonormalizar(conjunto_vectores):
    ortogonales = ortogonalizar(conjunto_vectores)
    ortonormales = []
    for v in ortogonales:
        norma = np.linalg.norm(v)
        if not np.isclose(norma, 0):
            ortonormales.append(v / norma)
    if not ortonormales:
        return np.zeros((0, ortogonales.shape[1]))
    return np.round(np.array(ortonormales), decimals=10)


def diagnosticar_vectores(matriz):
    rango = np.linalg.matrix_rank(matriz)
    num = matriz.shape[0]
    dim = matriz.shape[1]
    li = rango == num
    gen = rango == dim
    base = li and gen
    ort = proseso_ortogonal(matriz)
    orton = proseso_ortonormal(matriz, ort)
    return {
        "rango": rango,
        "num": num,
        "dim": dim,
        "li": li,
        "gen": gen,
        "base": base,
        "ortogonal": ort,
        "ortonormal": orton,
    }
