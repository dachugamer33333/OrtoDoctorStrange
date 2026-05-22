import numpy as np
import scipy as sp
from scipy.linalg import qr
def proseso_ortogonal(conjunto_vectores):
    n = len(conjunto_vectores)
    for i in range(n):
        for j in range(i + 1, n): 
            producto = np.dot(conjunto_vectores[i], conjunto_vectores[j])
           
            if not np.isclose(producto, 0):  # isclose porque floats
                return False
    return True
def proseso_ortonormal(conjunto_vectores,ortogonal):
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
       
    ortogonales=np.array(ortogonales)
    return np.round(ortogonales,decimals=10)

def ortonormalizar(conjunto_vectores):
    # primero ortogonalizar con gram-schmidt
    ortogonales = ortogonalizar(conjunto_vectores)
    # luego dividir cada vector entre su norma
    ortonormales = []
    for v in ortogonales:
        norma = np.linalg.norm(v)
        ortonormales.append(v / norma)
    return np.round(np.array(ortonormales), decimals=10)

def diagnostico_vectores() -> None:
    
    conjunto_vectores=[[1,3,0], [1,1,0], [2,0,1]]
    print(f"Matriz dada:{conjunto_vectores}")
    matriz = np.array(conjunto_vectores)
    
    rango= np.linalg.matrix_rank(matriz)
    

    num_vectores = len(conjunto_vectores)       
    dimension    = len(conjunto_vectores[0])    

    li  = rango == num_vectores        
    gen = rango == dimension           
    base = li and gen                  
    ortogonal=proseso_ortogonal(conjunto_vectores)
    ortonormal=proseso_ortonormal(conjunto_vectores,ortogonal)
    
    
    print(f"Rango: {rango}")
    print(f"Lin. independiente: {li}")
    print(f"Generador: {gen}")
    print(f"Base: {base}")
    if base:
       print(f"Es Ortogonal: {ortogonal}")
       print(f"Es ortonormal:{ortonormal}")
       if not ortogonal:
           conjunto_vectores_ortogonal=ortogonalizar(conjunto_vectores)
           ortogonal=proseso_ortogonal(conjunto_vectores_ortogonal)
           if ortogonal:
               conjunto_vectores_ortonormal=ortonormalizar(conjunto_vectores)
               ortonormal=proseso_ortonormal(conjunto_vectores_ortonormal,ortogonal)
               print("ortogonal")
               print(proseso_ortogonal(conjunto_vectores_ortogonal))
               print(conjunto_vectores_ortogonal)
               print("ortonormal")
               print(ortonormal)
               print(conjunto_vectores_ortonormal)

                
           


       
           
           

