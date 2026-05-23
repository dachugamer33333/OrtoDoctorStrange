import ast
import numpy as np
import customtkinter as ctk
from logica import vectores as vec
from logica.polinomios import vector_a_polinomio, diagnosticar_polinomios
from interfaz.componentes import ACCENT, GREEN, RED, MUTED, seccion, prop_card, bind_scroll


def crear_tab_polinomios(tabview):
    tab = tabview.add("Polinomios")

    # ── grado ────────────────────────────────────────────────────────────────
    gf = ctk.CTkFrame(tab, fg_color="transparent")
    gf.pack(fill="x", padx=18, pady=(16, 0))
    ctk.CTkLabel(gf, text="Grado máximo del espacio  P\u2099  n =",
                 font=ctk.CTkFont(size=13)).pack(side="left")
    grado_var = ctk.StringVar(value="3")
    ctk.CTkEntry(gf, textvariable=grado_var, width=64).pack(side="left", padx=10)

    # ── input ────────────────────────────────────────────────────────────────
    ctk.CTkLabel(tab,
                 text="Polinomios  —  coeficientes orden descendente  [c\u2099, \u2026, c\u2081, c\u2080]",
                 font=ctk.CTkFont(size=12), text_color=MUTED).pack(
        anchor="w", padx=18, pady=(12, 2))
    input_text = ctk.CTkTextbox(tab, height=74, corner_radius=8)
    input_text.pack(fill="x", padx=18)
    input_text.insert("1.0", "[1,0,0,1], [2,1,0,0], [0,3,2,1]")
    ctk.CTkLabel(tab, text="Ctrl+Enter para diagnosticar",
                 font=ctk.CTkFont(size=10), text_color=MUTED).pack(
        anchor="e", padx=18, pady=(2, 0))

    btn = ctk.CTkButton(tab, text="Diagnosticar", height=40,
                        font=ctk.CTkFont(size=13, weight="bold"),
                        fg_color=ACCENT, hover_color="#2d7dd2")
    btn.pack(pady=10, padx=18, fill="x")

    results = ctk.CTkScrollableFrame(tab, fg_color="transparent", corner_radius=0)
    results.pack(fill="both", expand=True, padx=18, pady=(0, 12))

    def diagnosticar():
        for w in results.winfo_children():
            w.destroy()

        try:
            n = int(grado_var.get())
            if n < 0:
                raise ValueError
        except ValueError:
            ctk.CTkLabel(results, text="⚠  El grado debe ser un entero ≥ 0.",
                         text_color=RED).pack(anchor="w")
            return

        raw = input_text.get("1.0", "end-1c").strip()
        try:
            pols = ast.literal_eval("[" + raw + "]")
            if not isinstance(pols, list) or not pols:
                raise ValueError
            if any(not isinstance(p, (list, tuple)) for p in pols):
                raise ValueError
            matriz = np.array(pols, dtype=float)
            if matriz.ndim != 2:
                raise ValueError
            if matriz.shape[1] != n + 1:
                ctk.CTkLabel(results,
                             text=f"⚠  Cada polinomio debe tener {n+1} coeficientes para P{n}.",
                             text_color=RED).pack(anchor="w")
                return
            # usuario ingresa orden descendente; internamente se usa ascendente
            matriz = matriz[:, ::-1]
        except (ValueError, SyntaxError):
            ctk.CTkLabel(results,
                         text="⚠  Formato inválido.  Ejemplo: [1,0,0,1], [2,1,0,0]",
                         text_color=RED).pack(anchor="w")
            return

        try:
            d = diagnosticar_polinomios(matriz, n)
        except Exception as e:
            ctk.CTkLabel(results, text=f"⚠  Error: {e}", text_color=RED).pack(anchor="w")
            return

        num = d["num"]
        rango, li, gen, base = d["rango"], d["li"], d["gen"], d["base"]
        ort, orton = d["ortogonal"], d["ortonormal"]

        ctk.CTkLabel(results,
                     text=f"  {num} polinomio{'s' if num != 1 else ''} en P{n}",
                     font=ctk.CTkFont(size=11), text_color=MUTED).pack(
            anchor="w", pady=(4, 0))

        seccion(results, "POLINOMIOS DADOS")
        for i, p in enumerate(matriz):
            ctk.CTkLabel(results, text=f"  p{i+1}(x) = {vector_a_polinomio(p)}",
                         font=ctk.CTkFont(family="Courier", size=12)).pack(anchor="w")

        seccion(results, "PROPIEDADES")
        prop_card(results, [
            ("Rango",         str(rango),         None),
            ("Independiente", "✔" if li    else "✗", li),
            ("Generador",     "✔" if gen   else "✗", gen),
            ("Base",          "✔" if base  else "✗", base),
            ("Ortogonal",     "✔" if ort   else "✗", ort),
            ("Ortonormal",    "✔" if orton else "✗", orton),
        ])

        if li:
            seccion(results, "GRAM-SCHMIDT")
            if ort:
                ctk.CTkLabel(results, text="  ✔  El conjunto ya es ortogonal",
                             text_color=GREEN, font=ctk.CTkFont(size=12)).pack(anchor="w")
            else:
                ortogonales = vec.ortogonalizar(matriz)
                for i, p in enumerate(ortogonales):
                    ctk.CTkLabel(results, text=f"  q{i+1}(x) = {vector_a_polinomio(p)}",
                                 font=ctk.CTkFont(family="Courier", size=12)).pack(anchor="w")
                verif = vec.proseso_ortogonal(ortogonales)
                ctk.CTkLabel(results,
                             text="  ✔  Son ortogonales" if verif else "  ✗  No son ortogonales",
                             text_color=GREEN if verif else RED,
                             font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(6, 0))

            seccion(results, "ORTONORMALIZACIÓN")
            if orton:
                ctk.CTkLabel(results, text="  ✔  El conjunto ya es ortonormal",
                             text_color=GREEN, font=ctk.CTkFont(size=12)).pack(anchor="w")
            else:
                ortonormales = vec.ortonormalizar(matriz)
                for i, p in enumerate(ortonormales):
                    ctk.CTkLabel(results, text=f"  e{i+1}(x) = {vector_a_polinomio(p)}",
                                 font=ctk.CTkFont(family="Courier", size=12)).pack(anchor="w")
                verif2 = vec.proseso_ortonormal(ortonormales, True)
                ctk.CTkLabel(results,
                             text="  ✔  Son ortonormales" if verif2 else "  ✗  No son ortonormales",
                             text_color=GREEN if verif2 else RED,
                             font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(6, 0))

        bind_scroll(results, results._parent_canvas)

    input_text.bind("<Control-Return>", lambda e: diagnosticar())
    btn.configure(command=diagnosticar)
    return tab
