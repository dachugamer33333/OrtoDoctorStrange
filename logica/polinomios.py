import numpy as np
from logica.vectores import proseso_ortogonal, proseso_ortonormal, ortogonalizar, ortonormalizar

SUPER = {0: "\u2070", 1: "\u00b9", 2: "\u00b2", 3: "\u00b3", 4: "\u2074",
         5: "\u2075", 6: "\u2076", 7: "\u2077", 8: "\u2078", 9: "\u2079"}


def _sup(n):
    if n <= 1:
        return ""
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


def diagnosticar_polinomios(matriz, n):
    dim_esperada = n + 1
    rango = np.linalg.matrix_rank(matriz)
    num = matriz.shape[0]
    li = rango == num
    gen = rango == dim_esperada
    base = li and gen
    ort = proseso_ortogonal(matriz)
    orton = proseso_ortonormal(matriz, ort)
    return {
        "rango": rango,
        "num": num,
        "dim": dim_esperada,
        "grado": n,
        "li": li,
        "gen": gen,
        "base": base,
        "ortogonal": ort,
        "ortonormal": orton,
    }
