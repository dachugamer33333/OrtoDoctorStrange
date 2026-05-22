import logica.vectores as vec
import logica.polinomios as pol
import logica.matrices as mat

def menu_consola():
    print("||Menu Consola||")
    print("""
    ===Alebra Lineal==
    1.Rⁿ
    2.Polinomios
    3.Matrices
""")
    op=int(input("Elige una opcion"))

    match op:
        case 1:
            vec.diagnostico_vectores()
        case 2:
            pol.diagnostico_polinomios()
        case 3:
            mat.diagnostico_matrices()

if __name__ == "__main__":
    menu_consola()
    
