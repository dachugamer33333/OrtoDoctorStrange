import ast
import numpy as np
import customtkinter as ctk
from logica import vectores as vec

GREEN = "#1a8a1a"
RED = "#cc3333"


def crear_tab_vectores(tabview):
    tab = tabview.add("R\u207f")

    ctk.CTkLabel(tab, text="Vectores (formato Python):",
                 font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=(10, 0))

    input_text = ctk.CTkTextbox(tab, height=70)
    input_text.pack(fill="x", padx=10, pady=5)
    input_text.insert("1.0", "[1,3,0], [1,1,0], [2,0,1]")

    ctk.CTkLabel(tab, text="Ctrl+Enter para diagnosticar",
                 font=ctk.CTkFont(size=11), text_color="gray").pack(anchor="e", padx=10)

    btn = ctk.CTkButton(tab, text="Diagnosticar")
    btn.pack(pady=5)

    results = ctk.CTkScrollableFrame(tab)
    results.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _bind_scroll(widget, canvas):
        widget.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        widget.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        widget.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        for child in widget.winfo_children():
            _bind_scroll(child, canvas)

    def prop_row(parent, row, col, label, value, ok):
        f = ctk.CTkFrame(parent)
        f.grid(row=row, column=col, padx=10, pady=2, sticky="w")
        ctk.CTkLabel(f, text=f"{label}:", width=90, anchor="w").pack(side="left")
        lbl = ctk.CTkLabel(f, text=value, font=ctk.CTkFont(size=12, weight="bold"))
        if ok is True:
            lbl.configure(text_color=GREEN)
        elif ok is False:
            lbl.configure(text_color=RED)
        lbl.pack(side="left")

    def diagnosticar():
        for w in results.winfo_children():
            w.destroy()

        raw = input_text.get("1.0", "end-1c").strip()
        try:
            vectors = ast.literal_eval("[" + raw + "]")
            if not isinstance(vectors, list) or len(vectors) == 0:
                raise ValueError
            if any(not isinstance(v, (list, tuple)) for v in vectors):
                raise ValueError
            matriz = np.array(vectors, dtype=float)
            if matriz.ndim != 2 or matriz.shape[0] < 1:
                raise ValueError
        except (ValueError, SyntaxError):
            ctk.CTkLabel(results, text="Error: formato invalido. Usa: [1,3,0], [1,1,0], [2,0,1]",
                         text_color=RED).pack(anchor="w")
            return

        try:
            d = vec.diagnosticar_vectores(matriz)
        except Exception as e:
            ctk.CTkLabel(results, text=f"Error inesperado: {e}", text_color=RED).pack(anchor="w")
            return

        num, dim = d["num"], d["dim"]
        rango, li, gen, base = d["rango"], d["li"], d["gen"], d["base"]
        ort, orton = d["ortogonal"], d["ortonormal"]

        ctk.CTkLabel(results,
                     text=f"Analizando {num} vector{'es' if num != 1 else ''} en \u211d{dim}",
                     font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(results, text="Propiedades:",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(5, 2))
        prop_frame = ctk.CTkFrame(results)
        prop_frame.pack(fill="x", pady=2)

        prop_row(prop_frame, 0, 0, "Rango", str(rango), None)
        prop_row(prop_frame, 0, 1, "L.I.", "\u2714" if li else "\u2718", li)
        prop_row(prop_frame, 1, 0, "Generador", "\u2714" if gen else "\u2718", gen)
        prop_row(prop_frame, 1, 1, "Base", "\u2714" if base else "\u2718", base)
        prop_row(prop_frame, 2, 0, "Ortogonal", "\u2714" if ort else "\u2718", ort)
        prop_row(prop_frame, 2, 1, "Ortonormal", "\u2714" if orton else "\u2718", orton)

        if base:
            ctk.CTkLabel(results, text="").pack()
            ctk.CTkLabel(results, text="Ortogonalizacion (Gram-Schmidt):",
                         font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(5, 2))

            if ort:
                ctk.CTkLabel(results, text="  \u2714 El conjunto ya es ortogonal",
                             text_color=GREEN).pack(anchor="w")
            else:
                ortogonales = vec.ortogonalizar(matriz)
                for i, v in enumerate(ortogonales):
                    ctk.CTkLabel(results, text=f"  q{i + 1} = {np.round(v, 4)}",
                                 font=ctk.CTkFont(family="Courier")).pack(anchor="w")
                verif = vec.proseso_ortogonal(ortogonales)
                ctk.CTkLabel(results,
                             text="  \u2714 Son ortogonales" if verif else "  \u2718 No son ortogonales",
                             text_color=GREEN if verif else RED).pack(anchor="w")

            ctk.CTkLabel(results, text="Ortonormalizacion:",
                         font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(5, 2))

            if orton:
                ctk.CTkLabel(results, text="  \u2714 El conjunto ya es ortonormal",
                             text_color=GREEN).pack(anchor="w")
            else:
                ortonormales = vec.ortonormalizar(matriz)
                for i, v in enumerate(ortonormales):
                    ctk.CTkLabel(results, text=f"  e{i + 1} = {np.round(v, 4)}",
                                 font=ctk.CTkFont(family="Courier")).pack(anchor="w")
                verif2 = vec.proseso_ortonormal(ortonormales, True)
                ctk.CTkLabel(results,
                             text="  \u2714 Son ortonormales" if verif2 else "  \u2718 No son ortonormales",
                             text_color=GREEN if verif2 else RED).pack(anchor="w")

        _bind_scroll(results, results._parent_canvas)

    input_text.bind("<Control-Return>", lambda e: diagnosticar())
    btn.configure(command=diagnosticar)
    return tab
