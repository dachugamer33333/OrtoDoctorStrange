import tkinter as tk


class SplashScreen(tk.Toplevel):
    """
    Pantalla de inicio animada.
    Fases: fade_in → linea → typewriter → glow → subtitulo → progress → fade_out
    """

    BG     = "#0d0d1e"
    ACCENT = "#4a9eff"
    WHITE  = "#e8e8ff"
    MUTED  = "#555577"
    W, H   = 540, 300

    def __init__(self, parent, on_done):
        super().__init__(parent)
        self._on_done = on_done

        self.overrideredirect(True)
        self.configure(bg=self.BG)

        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{self.W}x{self.H}+{(sw-self.W)//2}+{(sh-self.H)//2}")
        self.lift()

        # Detecta si el WM soporta transparencia (necesita compositing)
        self._alpha_ok = self._test_alpha()
        self._alpha    = 0.0 if self._alpha_ok else 1.0

        self._cv = tk.Canvas(self, width=self.W, height=self.H,
                              bg=self.BG, highlightthickness=0)
        self._cv.pack()

        self._char_idx = 0
        self._line_t   = 0.0
        self._sub_t    = 0.0
        self._glow_t   = 0.0
        self._prog     = 0.0
        # Sin alpha: salta fades y arranca directo en la animación de contenido
        self._fase     = "fade_in" if self._alpha_ok else "linea"

        self._build_canvas()
        self._tick()

    # ── construcción del canvas ──────────────────────────────────────────────

    def _build_canvas(self):
        cv, cx, W, H = self._cv, self.W // 2, self.W, self.H

        # Borde sutil
        cv.create_rectangle(0, 0, W-1, H-1, outline="#1e1e3e", width=1)

        # Línea accent superior (empieza vacía, se anima)
        cv.create_line(cx, 62, cx, 62, fill=self.ACCENT, width=1, tags="linea")

        # Título (typewriter)
        cv.create_text(cx, 118, text="", anchor="center",
                        font=("Helvetica", 32, "bold"),
                        fill=self.WHITE, tags="titulo")

        # Subtítulo (fade in)
        cv.create_text(cx, 160, text="",
                        font=("Helvetica", 13),
                        fill=self.BG, tags="subtitulo")

        # Línea inferior (aparece con subtítulo)
        cv.create_line(cx, 186, cx, 186, fill=self.BG, tags="linea2")

        # Barra de progreso — fondo
        cv.create_rectangle(cx-110, 214, cx+110, 222,
                              fill="#1a1a30", outline="", tags="pbg")
        # Barra de progreso — relleno
        cv.create_rectangle(cx-110, 214, cx-110, 222,
                              fill=self.ACCENT, outline="", tags="pfill")

        # Etiqueta bajo la barra
        cv.create_text(cx, 238, text="",
                        font=("Helvetica", 9),
                        fill=self.MUTED, tags="loading")

    # ── utilidad: detecta soporte de alpha ──────────────────────────────────

    def _test_alpha(self):
        try:
            self.attributes("-alpha", 0.0)
            return True
        except Exception:
            return False

    # ── loop principal ───────────────────────────────────────────────────────

    def _tick(self):
        fase = self._fase

        if fase == "fade_in":
            self._alpha = min(1.0, self._alpha + 0.07)
            self.attributes("-alpha", self._alpha)
            if self._alpha >= 1.0:
                self._fase = "linea"
            self.after(16, self._tick)

        elif fase == "linea":
            self._line_t = min(1.0, self._line_t + 0.055)
            cx, span = self.W // 2, int(130 * self._line_t)
            self._cv.coords("linea", cx - span, 62, cx + span, 62)
            if self._line_t >= 1.0:
                self._fase = "typewriter"
            self.after(16, self._tick)

        elif fase == "typewriter":
            TITULO = "DOCTOR STRANGE"
            self._cv.itemconfig("titulo", text=TITULO[:self._char_idx])
            self._char_idx += 1
            if self._char_idx > len(TITULO):
                self._fase = "glow"
                self._glow_t = 0.0
                self.after(80, self._tick)
            else:
                self.after(52, self._tick)

        elif fase == "glow":
            # Pulso: blanco → accent → blanco (triángulo)
            self._glow_t = min(1.0, self._glow_t + 0.055)
            ping = 1 - abs(2 * self._glow_t - 1)
            self._cv.itemconfig("titulo",
                                 fill=self._lerp(self.WHITE, self.ACCENT, ping))
            if self._glow_t >= 1.0:
                self._cv.itemconfig("titulo", fill=self.WHITE)
                self._fase = "subtitulo"
            self.after(16, self._tick)

        elif fase == "subtitulo":
            self._sub_t = min(1.0, self._sub_t + 0.055)
            t = self._sub_t
            cx = self.W // 2

            # Subtítulo fade in
            self._cv.itemconfig("subtitulo",
                                  text="Álgebra Lineal",
                                  fill=self._lerp(self.BG, self.ACCENT, t))
            # Línea inferior expande igual
            span2 = int(110 * t)
            self._cv.coords("linea2", cx - span2, 186, cx + span2, 186)
            self._cv.itemconfig("linea2",
                                  fill=self._lerp(self.BG, "#1e1e3e", t))
            if t >= 1.0:
                self._fase = "progress"
                self._cv.itemconfig("loading", text="Iniciando...")
            self.after(16, self._tick)

        elif fase == "progress":
            _labels = [
                (0.00, "Iniciando..."),
                (0.33, "Cargando módulos..."),
                (0.66, "Preparando interfaz..."),
                (0.95, "Listo  ✔"),
            ]
            self._prog = min(100.0, self._prog + 1.4)
            p = self._prog / 100.0
            cx = self.W // 2
            self._cv.coords("pfill", cx-110, 214, cx-110 + int(220*p), 222)

            label = _labels[0][1]
            for thresh, txt in _labels:
                if p >= thresh:
                    label = txt
            self._cv.itemconfig("loading", text=label)

            if self._prog >= 100.0:
                self._fase = "pause"
                self.after(500, self._tick)
            else:
                self.after(14, self._tick)

        elif fase == "pause":
            self._fase = "fade_out"
            self._tick()

        elif fase == "fade_out":
            if self._alpha_ok:
                self._alpha = max(0.0, self._alpha - 0.07)
                self.attributes("-alpha", self._alpha)
                if self._alpha <= 0.0:
                    self.destroy()
                    self._on_done()
                else:
                    self.after(16, self._tick)
            else:
                self.destroy()
                self._on_done()

    # ── utilidades ───────────────────────────────────────────────────────────

    def _lerp(self, c1, c2, t):
        """Interpola linealmente entre dos colores hex."""
        t = max(0.0, min(1.0, t))
        r1, g1, b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
        r2, g2, b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
        r = int(r1 + (r2-r1)*t)
        g = int(g1 + (g2-g1)*t)
        b = int(b1 + (b2-b1)*t)
        return f"#{r:02x}{g:02x}{b:02x}"
