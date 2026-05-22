import numpy as np
from logica.vectores import proseso_ortogonal, proseso_ortonormal, ortogonalizar, ortonormalizar

SUPER = {0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴",
         5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹"}

def _sup(n):
    if n == 0:
        return ""
    if n == 1:
        return ""
    if n <= 3:
        return {2: "²", 3: "³"}[n]
    return "".join(SUPER[int(d)] for d in str(n))

def _fmt(c):
    if c == int(c):
        return str(int(c))
    return f"{c:g}"

def vector_a_polinomio(coefs):
    coefs = np.array(coefs, dtype=float)
    terms = []
    for grado, c in enumerate(coefs):
        if np.isclose(c, 0):
            continue
        c = round(c, 10)
        if grado == 0:
            terms.append(_fmt(c))
        elif np.isclose(abs(c), 1):
            prefix = "-" if c < 0 else ""
            terms.append(f"{prefix}x{_sup(grado)}")
        else:
            prefix = "-" if c < 0 else ""
            terms.append(f"{prefix}{_fmt(abs(c))}x{_sup(grado)}")
    if not terms:
        return "0"
    terms.reverse()
    result = terms[0]
    for t in terms[1:]:
        if t.startswith("-"):
            result += " - " + t[1:]
        else:
            result += " + " + t
    return result

def diagnostico_polinomios():
    polinomios = [
        [1, 0, 0, 1],
        [0, 0, 1, 2],
        [1, 2, 3, 0],
    ]
    print("=== Diagnostico de Polinomios (P₃) ===")
    print("Polinomios dados:")
    for i, p in enumerate(polinomios):
        print(f"  p{i+1}(x) = {vector_a_polinomio(p)}")
    matriz = np.array(polinomios)
    rango = np.linalg.matrix_rank(matriz)
    num_polinomios = len(polinomios)
    dimension = len(polinomios[0])
    li = rango == num_polinomios
    gen = rango == dimension
    base = li and gen
    ortogonal = proseso_ortogonal(polinomios)
    ortonormal = proseso_ortonormal(polinomios, ortogonal)
    print(f"Rango: {rango}")
    print(f"Dimension del espacio (P₃): {dimension}")
    print(f"Lin. independiente: {li}")
    print(f"Generador: {gen}")
    print(f"Base: {base}")
    if base:
        print(f"Es Ortogonal: {ortogonal}")
        print(f"Es ortonormal: {ortonormal}")
        if not ortogonal:
            ortogonales = ortogonalizar(polinomios)
            ortogonal = proseso_ortogonal(ortogonales)
            print("Ortogonalizacion (Gram-Schmidt):")
            for i, p in enumerate(ortogonales):
                print(f"  q{i+1}(x) = {vector_a_polinomio(p)}")
            if ortogonal:
                print("Verificacion: Son ortogonales:", ortogonal)
                ortonormales = ortonormalizar(polinomios)
                print("Ortonormalizacion:")
                for i, p in enumerate(ortonormales):
                    print(f"  e{i+1}(x) = {vector_a_polinomio(p)}")
