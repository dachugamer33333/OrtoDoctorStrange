import ast
import numpy as np
import customtkinter as ctk
from logica import vectores as vec
from interfaz.componentes import ACCENT, GREEN, RED, MUTED, seccion, prop_card, bind_scroll


def crear_tab_vectores(tabview):
    tab = tabview.add("R\u207f")

    # ── dimensión ───────────────────────────────────────────────────────────
    df = ctk.CTkFrame(tab, fg_color="transparent")
    df.pack(fill="x", padx=18, pady=(16, 0))
    ctk.CTkLabel(df, text="Dimensión del espacio  n =",
                 font=ctk.CTkFont(size=13)).pack(side="left")
    n_var = ctk.StringVar(value="3")
    ctk.CTkEntry(df, textvariable=n_var, width=64).pack(side="left", padx=10)

    # ── input ───────────────────────────────────────────────────────────────
    ctk.CTkLabel(tab, text="Vectores",
                 font=ctk.CTkFont(size=12), text_color=MUTED).pack(
        anchor="w", padx=18, pady=(12, 2))
    input_text = ctk.CTkTextbox(tab, height=74, corner_radius=8)
    input_text.pack(fill="x", padx=18)
    input_text.insert("1.0", "[1,3,0], [1,1,0], [2,0,1]")
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
            n = int(n_var.get())
            if n < 1:
                raise ValueError
        except ValueError:
            ctk.CTkLabel(results, text="⚠  n debe ser un entero positivo.",
                         text_color=RED).pack(anchor="w")
            return

        raw = input_text.get("1.0", "end-1c").strip()
        try:
            vectors = ast.literal_eval("[" + raw + "]")
            if not isinstance(vectors, list) or not vectors:
                raise ValueError
            if any(not isinstance(v, (list, tuple)) for v in vectors):
                raise ValueError
            matriz = np.array(vectors, dtype=float)
            if matriz.ndim != 2:
                raise ValueError
            if matriz.shape[1] != n:
                ctk.CTkLabel(results,
                             text=f"⚠  Cada vector debe tener {n} componentes (n={n}).",
                             text_color=RED).pack(anchor="w")
                return
        except (ValueError, SyntaxError):
            ctk.CTkLabel(results,
                         text="⚠  Formato inválido.  Ejemplo: [1,3,0], [1,1,0]",
                         text_color=RED).pack(anchor="w")
            return

        try:
            d = vec.diagnosticar_vectores(matriz)
        except Exception as e:
            ctk.CTkLabel(results, text=f"⚠  Error: {e}", text_color=RED).pack(anchor="w")
            return

        num = d["num"]
        rango, li, gen, base = d["rango"], d["li"], d["gen"], d["base"]
        ort, orton = d["ortogonal"], d["ortonormal"]

        ctk.CTkLabel(results,
                     text=f"  {num} vector{'es' if num != 1 else ''} en \u211d{n}",
                     font=ctk.CTkFont(size=11), text_color=MUTED).pack(
            anchor="w", pady=(4, 0))

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
                for i, v in enumerate(ortogonales):
                    ctk.CTkLabel(results, text=f"  q{i+1} = {np.round(v, 4)}",
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
                for i, v in enumerate(ortonormales):
                    ctk.CTkLabel(results, text=f"  e{i+1} = {np.round(v, 4)}",
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
