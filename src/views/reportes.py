import tkinter as tk
from tkinter import ttk
from src.database import get_connection
from src.i18n import _


class VentanaReportes:
    def __init__(self, root, ciudadano):
        self.root = root
        self.ciudadano = ciudadano
        self.root.title(_("Qory Ayacucho - Reportes y Estadísticas"))
        self.root.geometry("650x520")
        self.root.resizable(False, False)

        main = ttk.Frame(root, padding="10")
        main.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main, text=_("Reportes y Estadísticas"), style="Heading.TLabel").pack(pady=(0, 10))

        notebook = ttk.Notebook(main)
        notebook.pack(fill=tk.BOTH, expand=True)

        self._tab_resumen(notebook)
        self._tab_presupuestos(notebook)
        self._tab_actividades(notebook)
        self._tab_ahorro(notebook)

        ttk.Button(main, text=_("Volver"), command=self.volver, style="Secondary.TButton").pack(pady=(10, 0))

    def _conn(self):
        return get_connection()

    def _tab_resumen(self, notebook):
        frame = ttk.Frame(notebook, padding="15")
        notebook.add(frame, text=_("Resumen General"))

        conn = self._conn()
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM presupuesto WHERE id_ciudadano = ?", (self.ciudadano["id_ciudadano"],))
        total_pres = c.fetchone()[0]

        c.execute("SELECT COALESCE(SUM(total), 0) FROM presupuesto WHERE id_ciudadano = ?", (self.ciudadano["id_ciudadano"],))
        suma_pres = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM historial WHERE id_ciudadano = ?", (self.ciudadano["id_ciudadano"],))
        total_hist = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM ahorro WHERE id_ciudadano = ?", (self.ciudadano["id_ciudadano"],))
        total_ahorro = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM ahorro WHERE id_ciudadano = ? AND estado = 'Completada'", (self.ciudadano["id_ciudadano"],))
        completadas = c.fetchone()[0]

        c.execute("SELECT COALESCE(SUM(monto_actual), 0) FROM ahorro WHERE id_ciudadano = ?", (self.ciudadano["id_ciudadano"],))
        total_ahorrado = c.fetchone()[0]

        conn.close()

        datos = [
            (_("Ciudadano"), self.ciudadano["nombre"]),
            (_("Email"), self.ciudadano["email"]),
            ("", ""),
            (_("Presupuestos creados"), str(total_pres)),
            (_("Total presupuestado"), f"S/ {suma_pres:.2f}"),
            ("", ""),
            (_("Actividades registradas"), str(total_hist)),
            ("", ""),
            (_("Metas de ahorro"), str(total_ahorro)),
            (_("Metas completadas"), str(completadas)),
            (_("Total ahorrado"), f"S/ {total_ahorrado:.2f}"),
        ]

        for label, valor in datos:
            if label == "":
                ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
            else:
                row = ttk.Frame(frame)
                row.pack(fill=tk.X, pady=2)
                ttk.Label(row, text=label, width=25, anchor=tk.W, style="Bold.TLabel").pack(side=tk.LEFT)
                ttk.Label(row, text=valor, anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))

    def _tab_presupuestos(self, notebook):
        frame = ttk.Frame(notebook, padding="15")
        notebook.add(frame, text=_("Presupuestos"))

        conn = self._conn()
        c = conn.cursor()
        c.execute(
            "SELECT total, dias, destino_principal, created_at FROM presupuesto WHERE id_ciudadano = ? ORDER BY created_at DESC",
            (self.ciudadano["id_ciudadano"],),
        )
        presupuestos = [dict(r) for r in c.fetchall()]
        conn.close()

        if not presupuestos:
            ttk.Label(frame, text=_("Aún no has creado presupuestos."), style="Subtitle.TLabel").pack(expand=True)
            return

        totales = [p["total"] for p in presupuestos]
        dias_list = [p["dias"] for p in presupuestos]
        promedio = sum(totales) / len(totales)
        max_pres = max(totales)
        min_pres = min(totales)
        mayor_dias = max(dias_list)

        info = [
            (_("Total de presupuestos"), str(len(presupuestos))),
            (_("Promedio por viaje"), f"S/ {promedio:.2f}"),
            (_("Presupuesto más alto"), f"S/ {max_pres:.2f}"),
            (_("Presupuesto más bajo"), f"S/ {min_pres:.2f}"),
            (_("Mayor cantidad de días"), str(mayor_dias)),
        ]
        for label, valor in info:
            row = ttk.Frame(frame)
            row.pack(fill=tk.X, pady=3)
            ttk.Label(row, text=label, width=28, anchor=tk.W, style="Bold.TLabel").pack(side=tk.LEFT)
            ttk.Label(row, text=valor, anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=12)

        ttk.Label(frame, text=_("Distribución de presupuestos (S/)"), style="Bold.TLabel").pack(anchor=tk.W, pady=(0, 8))

        canvas = tk.Canvas(frame, height=150, bg="#FAF5EF", highlightthickness=0)
        canvas.pack(fill=tk.X)

        ancho_total = 550
        margen = 40
        max_val = max(totales) if totales else 1
        colores = ["#8B4513", "#A0522D", "#D4A574", "#2C3E50", "#27AE60", "#C0392B"]
        bar_w = min(40, (ancho_total - margen) // len(presupuestos))
        if bar_w > 60:
            bar_w = 60
        separacion = 8
        inicio_x = margen
        for i, p in enumerate(presupuestos[:10]):
            alto = (p["total"] / max_val) * 120
            x0 = inicio_x + i * (bar_w + separacion)
            y0 = 140 - alto
            color = colores[i % len(colores)]
            canvas.create_rectangle(x0, y0, x0 + bar_w, 140, fill=color, outline="")
            canvas.create_text(x0 + bar_w / 2, 145, text=f"{p['total']:.0f}", font=("Arial", 7), anchor=tk.N)

    def _tab_actividades(self, notebook):
        frame = ttk.Frame(notebook, padding="15")
        notebook.add(frame, text=_("Actividades"))

        conn = self._conn()
        c = conn.cursor()
        c.execute(
            "SELECT tipo_actividad, COUNT(*) as cnt FROM historial WHERE id_ciudadano = ? GROUP BY tipo_actividad ORDER BY cnt DESC",
            (self.ciudadano["id_ciudadano"],),
        )
        actividades = [dict(r) for r in c.fetchall()]
        conn.close()

        if not actividades:
            ttk.Label(frame, text=_("Aún no tienes actividades registradas."), style="Subtitle.TLabel").pack(expand=True)
            return

        max_cnt = max(a["cnt"] for a in actividades)
        max_bar = 300

        ttk.Label(frame, text=_("Actividades por tipo"), style="Bold.TLabel").pack(anchor=tk.W, pady=(0, 10))

        canvas = tk.Canvas(frame, height=len(actividades) * 40 + 20, bg="#FAF5EF", highlightthickness=0)
        canvas.pack(fill=tk.X)

        colores = ["#8B4513", "#2C3E50", "#D4A574", "#27AE60", "#C0392B"]
        for i, a in enumerate(actividades):
            y = 15 + i * 40
            ancho = int((a["cnt"] / max_cnt) * max_bar) if max_cnt else 0
            color = colores[i % len(colores)]
            canvas.create_rectangle(10, y, 10 + ancho, y + 25, fill=color, outline="")
            canvas.create_text(15 + ancho, y + 12, text=f"{a['tipo_actividad']} ({a['cnt']})", font=("Arial", 9), anchor=tk.W, fill="white" if ancho > 120 else "#2D3436")

    def _tab_ahorro(self, notebook):
        frame = ttk.Frame(notebook, padding="15")
        notebook.add(frame, text=_("Ahorro"))

        conn = self._conn()
        c = conn.cursor()
        c.execute(
            "SELECT meta, monto_objetivo, monto_actual, estado FROM ahorro WHERE id_ciudadano = ? ORDER BY fecha_inicio DESC",
            (self.ciudadano["id_ciudadano"],),
        )
        metas = [dict(r) for r in c.fetchall()]
        conn.close()

        if not metas:
            ttk.Label(frame, text=_("Aún no tienes metas de ahorro."), style="Subtitle.TLabel").pack(expand=True)
            return

        total_obj = sum(m["monto_objetivo"] for m in metas)
        total_act = sum(m["monto_actual"] for m in metas)
        completadas = sum(1 for m in metas if m["estado"] == "Completada")
        en_progreso = sum(1 for m in metas if m["estado"] == "En progreso")
        pct_global = (total_act / total_obj * 100) if total_obj > 0 else 0

        info = [
            (_("Total de metas"), str(len(metas))),
            (_("Completadas"), str(completadas)),
            (_("En progreso"), str(en_progreso)),
            (_("Objetivo total"), f"S/ {total_obj:.2f}"),
            (_("Ahorrado total"), f"S/ {total_act:.2f}"),
            (_("Progreso global"), f"{pct_global:.1f}%"),
        ]
        for label, valor in info:
            row = ttk.Frame(frame)
            row.pack(fill=tk.X, pady=3)
            ttk.Label(row, text=label, width=18, anchor=tk.W, style="Bold.TLabel").pack(side=tk.LEFT)
            ttk.Label(row, text=valor, anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=12)

        ttk.Label(frame, text=_("Progreso por meta"), style="Bold.TLabel").pack(anchor=tk.W, pady=(0, 8))

        canvas = tk.Canvas(frame, height=len(metas) * 40 + 20, bg="#FAF5EF", highlightthickness=0)
        canvas.pack(fill=tk.X)

        for i, m in enumerate(metas):
            y = 15 + i * 40
            pct = (m["monto_actual"] / m["monto_objetivo"] * 100) if m["monto_objetivo"] > 0 else 0
            ancho = int(pct / 100 * 300)
            color = "#27AE60" if m["estado"] == "Completada" else "#8B4513"
            canvas.create_rectangle(10, y, 10 + ancho, y + 25, fill=color, outline="")
            texto = f"{m['meta']}: S/ {m['monto_actual']:.0f} / S/ {m['monto_objetivo']:.0f} ({pct:.0f}%)"
            canvas.create_text(15 + ancho, y + 12, text=texto, font=("Arial", 9), anchor=tk.W, fill="white" if ancho > 150 else "#2D3436")

    def volver(self):
        self.root.destroy()
