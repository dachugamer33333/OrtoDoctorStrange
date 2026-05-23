import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import customtkinter as ctk
from interfaz.tab_vectores import crear_tab_vectores
from interfaz.tab_polinomios import crear_tab_polinomios
from interfaz.tab_matrices import crear_tab_matrices

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OrtoBasesDoctorStrange \u2014 \u00c1lgebra Lineal")
        self.geometry("940x700")
        self.minsize(800, 560)

        # Header
        header = ctk.CTkFrame(self, height=50, corner_radius=0,
                               fg_color=("#12122a", "#0d0d1e"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="\u00c1LGEBRA LINEAL",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color="#4a9eff").pack(side="left", padx=22, pady=14)
        ctk.CTkLabel(header, text="OrtoBaseDoctorStrange",
                     font=ctk.CTkFont(size=11),
                     text_color="#555577").pack(side="right", padx=22)

        self.tabview = ctk.CTkTabview(self, corner_radius=0)
        self.tabview.pack(fill="both", expand=True)

        crear_tab_vectores(self.tabview)
        crear_tab_polinomios(self.tabview)
        crear_tab_matrices(self.tabview)


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
