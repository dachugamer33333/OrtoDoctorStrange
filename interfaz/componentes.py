import customtkinter as ctk

ACCENT = "#4a9eff"
GREEN  = "#2ecc71"
RED    = "#e74c3c"
MUTED  = "#888888"
CARD   = ("#e8e8f2", "#252535")
SEP    = ("#c0c0d8", "#2d2d45")


def seccion(parent, titulo):
    """Cabecera de sección: TITULO ────────────"""
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(fill="x", pady=(14, 3))
    ctk.CTkLabel(f, text=titulo,
                 font=ctk.CTkFont(size=10, weight="bold"),
                 text_color=ACCENT).pack(side="left")
    ctk.CTkFrame(f, height=1, fg_color=SEP).pack(
        side="left", fill="x", expand=True, padx=(8, 0), pady=5)


def prop_card(parent, props):
    """
    Tarjeta de propiedades.
    props: list of (label, value_str, ok)  — ok=True/False/None
    """
    card = ctk.CTkFrame(parent, corner_radius=10, fg_color=CARD)
    card.pack(fill="x", pady=(2, 6), padx=2)
    n = len(props)
    for i, (label, value, ok) in enumerate(props):
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=18,
                 pady=(10 if i == 0 else 3, 10 if i == n - 1 else 3))
        ctk.CTkLabel(row, text=label,
                     font=ctk.CTkFont(size=12), anchor="w",
                     width=140).pack(side="left")
        color = None if ok is None else (GREEN if ok else RED)
        lbl = ctk.CTkLabel(row, text=value,
                            font=ctk.CTkFont(size=13, weight="bold"),
                            anchor="e")
        if color:
            lbl.configure(text_color=color)
        lbl.pack(side="right")
    return card


def bind_scroll(widget, canvas):
    widget.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    widget.bind("<Button-4>",   lambda e: canvas.yview_scroll(-1, "units"))
    widget.bind("<Button-5>",   lambda e: canvas.yview_scroll(1, "units"))
    for child in widget.winfo_children():
        bind_scroll(child, canvas)
