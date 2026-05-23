import re
import numpy as np
import customtkinter as ctk
from logica import matrices as mat
from interfaz.componentes import ACCENT, GREEN, RED, MUTED, seccion, prop_card, bind_scroll


def _fmt_matriz(M):
    filas = ["[" + "  ".join(f"{x:7.4f}" for x in fila) + "]" for fila in M]
    return "  " + "\n  ".join(filas)


def _parsear_matrices(raw):
    """Formato: [fila1; fila2]  una por línea o separadas por comas."""
    bloques = re.findall(r'\[([^\[\]]+)\]', raw)
    if not bloques:
        raise ValueError("sin matrices")
    matrices = []
    for bloque in bloques:
        filas_str = [f.strip() for f in bloque.split(';')]
        matriz = []
        for fila in filas_str:
            vals = [float(x) for x in re.split(r'[,\s]+', fila.strip()) if x]
            if not vals:
                raise ValueError
            matriz.append(vals)
        matrices.append(matriz)
    return matrices


def _ejemplo_formato(m, n):
    fila = " ".join(["0"] * n)
    return "[" + "; ".join([fila] * m) + "]"


def crear_tab_matrices(tabview):
    tab = tabview.add("Matrices")

    # ── dimensión ────────────────────────────────────────────────────────────
    df = ctk.CTkFrame(tab, fg_color="transparent")
    df.pack(fill="x", padx=18, pady=(16, 0))
    ctk.CTkLabel(df, text="Dimensión M\u2098\u2099  —  m =",
                 font=ctk.CTkFont(size=13)).pack(side="left")
    m_var = ctk.StringVar(value="2")
    ctk.CTkEntry(df, textvariable=m_var, width=60).pack(side="left", padx=8)
    ctk.CTkLabel(df, text="n =",
                 font=ctk.CTkFont(size=13)).pack(side="left", padx=(12, 0))
    n_var = ctk.StringVar(value="2")
    ctk.CTkEntry(df, textvariable=n_var, width=60).pack(side="left", padx=8)

    # ── input ────────────────────────────────────────────────────────────────
    ctk.CTkLabel(tab, text="Matrices  —  una por línea: [fila1; fila2; \u2026]",
                 font=ctk.CTkFont(size=12), text_color=MUTED).pack(
        anchor="w", padx=18, pady=(12, 2))
    input_text = ctk.CTkTextbox(tab, height=100, corner_radius=8)
    input_text.pack(fill="x", padx=18)
    input_text.insert("1.0", "[1 0; 0 0]\n[1 1; 0 0]\n[1 1; 1 0]\n[1 1; 1 1]")

    hint_label = ctk.CTkLabel(tab, text="",
                               font=ctk.CTkFont(size=10), text_color=MUTED)
    hint_label.pack(anchor="w", padx=18, pady=(2, 0))

    def actualizar_hint(*_):
        try:
            mv, nv = int(m_var.get()), int(n_var.get())
            if mv > 0 and nv > 0:
                hint_label.configure(
                    text=f"Formato: {_ejemplo_formato(mv, nv)}   "
                         f"  filas separadas por ';', valores por espacios o comas")
        except ValueError:
            pass

    m_var.trace_add("write", actualizar_hint)
    n_var.trace_add("write", actualizar_hint)
    actualizar_hint()

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
            m = int(m_var.get())
            nv = int(n_var.get())
            if m < 1 or nv < 1:
                raise ValueError
        except ValueError:
            ctk.CTkLabel(results, text="⚠  m y n deben ser enteros positivos.",
                         text_color=RED).pack(anchor="w")
            return

        raw = input_text.get("1.0", "end-1c").strip()
        try:
            matrices = _parsear_matrices(raw)
            arr = np.array(matrices, dtype=float)
            if arr.ndim != 3:
                raise ValueError
            if arr.shape[1] != m or arr.shape[2] != nv:
                ctk.CTkLabel(results,
                             text=f"⚠  Cada matriz debe ser {m}×{nv}.",
                             text_color=RED).pack(anchor="w")
                return
        except (ValueError, TypeError):
            ej = _ejemplo_formato(m, nv)
            ctk.CTkLabel(results,
                         text=f"⚠  Formato inválido.  Ejemplo: {ej}",
                         text_color=RED).pack(anchor="w")
            return

        try:
            d = mat.diagnosticar_matrices(arr, m, nv)
        except Exception as e:
            ctk.CTkLabel(results, text=f"⚠  Error: {e}", text_color=RED).pack(anchor="w")
            return

        num = d["num"]
        rango, li, gen, base = d["rango"], d["li"], d["gen"], d["base"]
        ort, orton = d["ortogonal"], d["ortonormal"]

        ctk.CTkLabel(results,
                     text=f"  {num} matri{'ces' if num != 1 else 'z'} en M{m}\u00d7{nv}",
                     font=ctk.CTkFont(size=11), text_color=MUTED).pack(
            anchor="w", pady=(4, 0))

        seccion(results, "MATRICES DADAS")
        for i, M in enumerate(arr):
            ctk.CTkLabel(results, text=f"  M{i+1} = {_fmt_matriz(M)}",
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
            seccion(results, "GRAM-SCHMIDT  (FROBENIUS)")
            if ort:
                ctk.CTkLabel(results, text="  ✔  El conjunto ya es ortogonal",
                             text_color=GREEN, font=ctk.CTkFont(size=12)).pack(anchor="w")
            else:
                ortogonales = mat.ortogonalizar(arr)
                for i, M in enumerate(ortogonales):
                    ctk.CTkLabel(results, text=f"  Q{i+1} = {_fmt_matriz(M)}",
                                 font=ctk.CTkFont(family="Courier", size=12)).pack(anchor="w")
                verif = mat.proseso_ortogonal(ortogonales)
                ctk.CTkLabel(results,
                             text="  ✔  Son ortogonales" if verif else "  ✗  No son ortogonales",
                             text_color=GREEN if verif else RED,
                             font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(6, 0))

            seccion(results, "ORTONORMALIZACIÓN")
            if orton:
                ctk.CTkLabel(results, text="  ✔  El conjunto ya es ortonormal",
                             text_color=GREEN, font=ctk.CTkFont(size=12)).pack(anchor="w")
            else:
                ortonormales = mat.ortonormalizar(arr)
                for i, M in enumerate(ortonormales):
                    ctk.CTkLabel(results, text=f"  E{i+1} = {_fmt_matriz(M)}",
                                 font=ctk.CTkFont(family="Courier", size=12)).pack(anchor="w")
                verif2 = mat.proseso_ortonormal(ortonormales, True)
                ctk.CTkLabel(results,
                             text="  ✔  Son ortonormales" if verif2 else "  ✗  No son ortonormales",
                             text_color=GREEN if verif2 else RED,
                             font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(6, 0))

        bind_scroll(results, results._parent_canvas)

    input_text.bind("<Control-Return>", lambda e: diagnosticar())
    btn.configure(command=diagnosticar)
    return tab
