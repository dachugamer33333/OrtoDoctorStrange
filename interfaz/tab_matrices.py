import ast
import numpy as np
import customtkinter as ctk
from logica import matrices as mat

GREEN = "#1a8a1a"
RED = "#cc3333"


def _fmt_matriz_compacto(M):
    rows = []
    for row in M:
        rows.append("[" + " ".join(f"{x:7.4f}" for x in row) + "]")
    return "  " + "\n  ".join(rows)


def crear_tab_matrices(tabview):
    tab = tabview.add("Matrices")

    dim_frame = ctk.CTkFrame(tab)
    dim_frame.pack(fill="x", padx=10, pady=(10, 0))
    ctk.CTkLabel(dim_frame, text="Dimension M\u2098\u2099:  m =",
                 font=ctk.CTkFont(size=14)).pack(side="left")
    m_var = ctk.StringVar(value="2")
    m_entry = ctk.CTkEntry(dim_frame, textvariable=m_var, width=60)
    m_entry.pack(side="left", padx=5)
    ctk.CTkLabel(dim_frame, text="n =",
                 font=ctk.CTkFont(size=14)).pack(side="left", padx=(10, 0))
    n_var = ctk.StringVar(value="2")
    n_entry = ctk.CTkEntry(dim_frame, textvariable=n_var, width=60)
    n_entry.pack(side="left", padx=5)

    ctk.CTkLabel(tab, text="Matrices (formato Python):",
                 font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=(10, 0))
    input_text = ctk.CTkTextbox(tab, height=70)
    input_text.pack(fill="x", padx=10, pady=5)
    input_text.insert("1.0", "[[1,0],[0,0]], [[1,1],[0,0]], [[1,1],[1,0]], [[1,1],[1,1]]")

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

        try:
            m = int(m_var.get())
            n_val = int(n_var.get())
            if m < 1 or n_val < 1:
                ctk.CTkLabel(results, text="Error: m y n deben ser enteros positivos.",
                             text_color=RED).pack(anchor="w")
                return
        except ValueError:
            ctk.CTkLabel(results, text="Error: m y n deben ser numeros enteros.",
                         text_color=RED).pack(anchor="w")
            return

        raw = input_text.get("1.0", "end-1c").strip()
        try:
            matrices = ast.literal_eval("[" + raw + "]")
            if not isinstance(matrices, list) or len(matrices) == 0:
                raise ValueError
            if any(not isinstance(M, (list, tuple)) for M in matrices):
                raise ValueError
            arr = np.array(matrices, dtype=float)
            if arr.ndim != 3 or arr.shape[0] < 1:
                raise ValueError
            if arr.shape[1] != m or arr.shape[2] != n_val:
                ctk.CTkLabel(results,
                             text=f"Error: cada matriz debe ser {m}x{n_val}",
                             text_color=RED).pack(anchor="w")
                return
        except (ValueError, SyntaxError):
            ctk.CTkLabel(results, text="Error: formato invalido.",
                         text_color=RED).pack(anchor="w")
            return

        try:
            d = mat.diagnosticar_matrices(arr, m, n_val)
        except Exception as e:
            ctk.CTkLabel(results, text=f"Error inesperado: {e}", text_color=RED).pack(anchor="w")
            return

        num = d["num"]
        rango, li, gen, base = d["rango"], d["li"], d["gen"], d["base"]
        ort, orton = d["ortogonal"], d["ortonormal"]

        ctk.CTkLabel(results,
                     text=f"Analizando {num} matri{'ces' if num != 1 else 'z'} en M{m}x{n_val}",
                     font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(results, text="Matrices dadas:",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(5, 2))
        for i, M in enumerate(arr):
            ctk.CTkLabel(results, text=f"  M{i + 1} = {_fmt_matriz_compacto(M)}",
                         font=ctk.CTkFont(family="Courier", size=12)).pack(anchor="w")

        ctk.CTkLabel(results, text="").pack()
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

        if li:
            ctk.CTkLabel(results, text="").pack()
            ctk.CTkLabel(results, text="Ortogonalizacion (Gram-Schmidt con producto de Frobenius):",
                         font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(5, 2))

            if ort:
                ctk.CTkLabel(results, text="  \u2714 El conjunto ya es ortogonal",
                             text_color=GREEN).pack(anchor="w")
            else:
                ortogonales = mat.ortogonalizar(arr)
                for i, M in enumerate(ortogonales):
                    ctk.CTkLabel(results, text=f"  Q{i + 1} = {_fmt_matriz_compacto(M)}",
                                 font=ctk.CTkFont(family="Courier", size=12)).pack(anchor="w")
                verif = mat.proseso_ortogonal(ortogonales)
                ctk.CTkLabel(results,
                             text="  \u2714 Son ortogonales" if verif else "  \u2718 No son ortogonales",
                             text_color=GREEN if verif else RED).pack(anchor="w")

            ctk.CTkLabel(results, text="Ortonormalizacion:",
                         font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(5, 2))

            if orton:
                ctk.CTkLabel(results, text="  \u2714 El conjunto ya es ortonormal",
                             text_color=GREEN).pack(anchor="w")
            else:
                ortonormales = mat.ortonormalizar(arr)
                for i, M in enumerate(ortonormales):
                    ctk.CTkLabel(results, text=f"  E{i + 1} = {_fmt_matriz_compacto(M)}",
                                 font=ctk.CTkFont(family="Courier", size=12)).pack(anchor="w")
                verif2 = mat.proseso_ortonormal(ortonormales, True)
                ctk.CTkLabel(results,
                             text="  \u2714 Son ortonormales" if verif2 else "  \u2718 No son ortonormales",
                             text_color=GREEN if verif2 else RED).pack(anchor="w")

        _bind_scroll(results, results._parent_canvas)

    input_text.bind("<Control-Return>", lambda e: diagnosticar())
    btn.configure(command=diagnosticar)
    return tab
