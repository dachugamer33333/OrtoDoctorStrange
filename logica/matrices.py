import numpy as np

def producto_interno(A, B):
    return np.vdot(A, B)

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
    ortogonales = []
    for M in conjunto_matrices:
        W = np.array(M, dtype=float)
        for U in ortogonales:
            W = W - (producto_interno(W, U) / producto_interno(U, U)) * U
        ortogonales.append(W)
    ortogonales = np.array(ortogonales)
    return np.round(ortogonales, decimals=10)

def ortonormalizar(conjunto_matrices):
    ortogonales = ortogonalizar(conjunto_matrices)
    ortonormales = []
    for M in ortogonales:
        norma = np.linalg.norm(M, 'fro')
        ortonormales.append(M / norma)
    return np.round(np.array(ortonormales), decimals=10)

def _fmt_matriz(M):
    lines = []
    for row in M:
        lines.append("  [" + " ".join(f"{x:>8.4f}" for x in row) + "]")
    return "[\n" + "\n".join(lines) + "\n]"

def diagnostico_matrices():
    matrices = [
        np.array([[1, 0], [0, 0]], dtype=float),
        np.array([[1, 1], [0, 0]], dtype=float),
        np.array([[1, 1], [1, 0]], dtype=float),
        np.array([[1, 1], [1, 1]], dtype=float),
    ]
    m, n = matrices[0].shape
    print(f"=== Diagnostico de Matrices (M_{{{m}\\times{n}}}) ===")
    print(f"Dimension del espacio: {m * n}")
    print("Matrices dadas:")
    for i, M in enumerate(matrices):
        print(f"  M{i+1} = {_fmt_matriz(M)}")
    flat = np.array([M.flatten() for M in matrices])
    rango = np.linalg.matrix_rank(flat)
    num_matrices = len(matrices)
    dimension = m * n
    li = rango == num_matrices
    gen = rango == dimension
    base = li and gen
    ortogonal = proseso_ortogonal(matrices)
    ortonormal = proseso_ortonormal(matrices, ortogonal)
    print(f"Rango: {rango}")
    print(f"Lin. independiente: {li}")
    print(f"Generador: {gen}")
    print(f"Base: {base}")
    if base:
        print(f"Es Ortogonal: {ortogonal}")
        print(f"Es ortonormal: {ortonormal}")
        if not ortogonal:
            ortogonales = ortogonalizar(matrices)
            ortogonal = proseso_ortogonal(ortogonales)
            print("Ortogonalizacion (Gram-Schmidt con producto de Frobenius):")
            for i, M in enumerate(ortogonales):
                print(f"  Q{i+1} = {_fmt_matriz(M)}")
            if ortogonal:
                print("Verificacion: Son ortogonales:", ortogonal)
                ortonormales = ortonormalizar(matrices)
                print("Ortonormalizacion:")
                for i, M in enumerate(ortonormales):
                    print(f"  E{i+1} = {_fmt_matriz(M)}")
