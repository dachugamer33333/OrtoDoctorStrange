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
    ortogonales = []
    for v in conjunto_vectores:
        w = np.array(v, dtype=float)
        for u in ortogonales:
            w = w - (np.dot(w, u) / np.dot(u, u)) * u
        ortogonales.append(w)
    ortogonales = np.array(ortogonales)
    return np.round(ortogonales, decimals=10)


def ortonormalizar(conjunto_vectores):
    ortogonales = ortogonalizar(conjunto_vectores)
    ortonormales = []
    for v in ortogonales:
        norma = np.linalg.norm(v)
        ortonormales.append(v / norma)
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
