import logica.vectores as vec

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
            print()
        case 3:
            print()

if __name__ == "__main__":
    menu_consola()
    
