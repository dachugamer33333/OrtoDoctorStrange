import ast
import numpy as np
import customtkinter as ctk
from logica import vectores as vec
from logica.polinomios import vector_a_polinomio, diagnosticar_polinomios


def crear_tab_polinomios(tabview):
    tab = tabview.add("Polinomios")

    grado_frame = ctk.CTkFrame(tab)
    grado_frame.pack(fill="x", padx=10, pady=(10, 0))
    ctk.CTkLabel(grado_frame, text="Grado maximo del espacio (P\u2099):",
                 font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
    grado_var = ctk.StringVar(value="3")
    grado_menu = ctk.CTkOptionMenu(grado_frame, variable=grado_var,
                                   values=["1", "2", "3", "4"], width=60)
    grado_menu.pack(side="left")

    ctk.CTkLabel(tab, text="Polinomios (coeficientes orden ascendente [c\u2080, c\u2081, ...]):",
                 font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=(10, 0))

    input_text = ctk.CTkTextbox(tab, height=70)
    input_text.pack(fill="x", padx=10, pady=5)
    input_text.insert("1.0", "[1,0,0,1], [0,0,1,2], [1,2,3,0]")

    btn = ctk.CTkButton(tab, text="Diagnosticar")
    btn.pack(pady=5)

    results = ctk.CTkScrollableFrame(tab)
    results.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def diagnosticar():
        for w in results.winfo_children():
            w.destroy()

        n = int(grado_var.get())

        raw = input_text.get("1.0", "end-1c").strip()
        try:
            pols = ast.literal_eval("[" + raw + "]")
            if not isinstance(pols, list):
                raise ValueError
            if len(pols) == 0:
                raise ValueError("lista vacia")
            if any(not isinstance(p, (list, tuple)) for p in pols):
                raise ValueError
            matriz = np.array(pols, dtype=float)
            if matriz.ndim != 2 or matriz.shape[0] < 1:
                raise ValueError
            if matriz.shape[1] != n + 1:
                ctk.CTkLabel(results,
                             text=f"Error: los coeficientes deben tener {n + 1} componentes para P\u2099 con n={n}",
                             text_color="red").pack(anchor="w")
                return
            d = diagnosticar_polinomios(matriz, n)
        except Exception:
            ctk.CTkLabel(results, text="Error: formato invalido.",
                         text_color="red").pack(anchor="w")
            return

        rango, li, gen, base = d["rango"], d["li"], d["gen"], d["base"]
        ort, orton = d["ortogonal"], d["ortonormal"]

        ctk.CTkLabel(results, text="Polinomios dados:",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(5, 2))
        for i, p in enumerate(matriz):
            ctk.CTkLabel(results, text=f"  p{i + 1}(x) = {vector_a_polinomio(p)}",
                         font=ctk.CTkFont(family="Courier")).pack(anchor="w")

        ctk.CTkLabel(results, text="").pack()
        ctk.CTkLabel(results, text="Propiedades:",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(5, 2))
        prop_frame = ctk.CTkFrame(results)
        prop_frame.pack(fill="x", pady=2)

        def prop_row(parent, row, col, label, value, ok):
            f = ctk.CTkFrame(parent)
            f.grid(row=row, column=col, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(f, text=f"{label}:", width=90, anchor="w").pack(side="left")
            c = "#1a8a1a" if ok else "#cc3333"
            ctk.CTkLabel(f, text=value, text_color=c,
                         font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")

        prop_row(prop_frame, 0, 0, "Rango", str(rango), True)
        prop_row(prop_frame, 0, 1, "L.I.", "\u2714" if li else "\u2718", li)
        prop_row(prop_frame, 1, 0, "Generador", "\u2714" if gen else "\u2718", gen)
        prop_row(prop_frame, 1, 1, "Base", "\u2714" if base else "\u2718", base)
        prop_row(prop_frame, 2, 0, "Ortogonal", "\u2714" if ort else "\u2718", ort)
        prop_row(prop_frame, 2, 1, "Ortonormal", "\u2714" if orton else "\u2718", orton)

        if not base:
            return

        if not ort:
            ctk.CTkLabel(results, text="").pack()
            ctk.CTkLabel(results, text="Ortogonalizacion (Gram-Schmidt):",
                         font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(5, 2))
            ortogonales = vec.ortogonalizar(matriz)
            for i, p in enumerate(ortogonales):
                ctk.CTkLabel(results, text=f"  q{i + 1}(x) = {vector_a_polinomio(p)}",
                             font=ctk.CTkFont(family="Courier")).pack(anchor="w")

            verif = vec.proseso_ortogonal(ortogonales)
            c_color = "#1a8a1a" if verif else "#cc3333"
            ctk.CTkLabel(results, text=f"  \u2714 Son ortogonales" if verif else f"  \u2718 No son ortogonales",
                         text_color=c_color).pack(anchor="w")

            ctk.CTkLabel(results, text="Ortonormalizacion:",
                         font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(5, 2))
            ortonormales = vec.ortonormalizar(matriz)
            for i, p in enumerate(ortonormales):
                ctk.CTkLabel(results, text=f"  e{i + 1}(x) = {vector_a_polinomio(p)}",
                             font=ctk.CTkFont(family="Courier")).pack(anchor="w")

            verif2 = vec.proseso_ortonormal(ortonormales, True)
            c_color2 = "#1a8a1a" if verif2 else "#cc3333"
            ctk.CTkLabel(results, text=f"  \u2714 Son ortonormales" if verif2 else f"  \u2718 No son ortonormales",
                         text_color=c_color2).pack(anchor="w")

    btn.configure(command=diagnosticar)
    return tab
