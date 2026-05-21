import numpy as np
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

    

def diagnostico_vectores() -> None:
    
    conjunto_vectores=[[1,0,0], [1,1,0], [0,0,1]]
    matriz = np.array(conjunto_vectores)
    
    rango        = np.linalg.matrix_rank(matriz)
    

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
       
           
           

