import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import customtkinter as ctk
from interfaz.tab_vectores import crear_tab_vectores
from interfaz.tab_polinomios import crear_tab_polinomios
from interfaz.tab_matrices import crear_tab_matrices

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Algebra Lineal - DoctorStrange")
        self.geometry("850x650")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        crear_tab_vectores(self.tabview)
        crear_tab_polinomios(self.tabview)
        crear_tab_matrices(self.tabview)


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
