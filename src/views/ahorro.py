import tkinter as tk
from tkinter import messagebox, ttk
from src.models.ahorro import Ahorro
from src.models.historial import Historial
from src.i18n import _


class VentanaAhorro:
    def __init__(self, root, ciudadano):
        self.root = root
        self.ciudadano = ciudadano
        self.root.title(_("Qory Ayacucho - Metas de Ahorro"))
        self.root.geometry("750x520")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Metas de Ahorro - %s") % ciudadano['nombre'], style="Heading.TLabel").pack(pady=(0, 10))

        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(toolbar, text=_("Filtrar:")).pack(side=tk.LEFT, padx=(0, 5))
        self.filtro_combo = ttk.Combobox(toolbar, state="readonly", width=15)
        self.filtro_combo["values"] = (_("Todas"), _("En progreso"), _("Completada"), _("Cancelada"))
        self.filtro_combo.current(0)
        self.filtro_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.filtro_combo.bind("<<ComboboxSelected>>", lambda e: self.cargar())
        ttk.Button(toolbar, text=_("Volver"), command=self.volver, style="Secondary.TButton").pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar, text=_("Nueva Meta"), command=self.agregar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar, text=_("Aportar"), command=self.aportar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar, text=_("Editar"), command=self.editar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar, text=_("Eliminar"), command=self.eliminar).pack(side=tk.RIGHT)

        columns = ("meta", "monto_objetivo", "monto_actual", "progreso", "fecha_inicio", "fecha_limite", "estado")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=14)
        self.tree.heading("meta", text=_("Meta"))
        self.tree.heading("monto_objetivo", text=_("Objetivo (S/)"))
        self.tree.heading("monto_actual", text=_("Ahorrado (S/)"))
        self.tree.heading("progreso", text=_("Progreso"))
        self.tree.heading("fecha_inicio", text=_("Inicio"))
        self.tree.heading("fecha_limite", text=_("Límite"))
        self.tree.heading("estado", text=_("Estado"))
        self.tree.column("meta", width=160)
        self.tree.column("monto_objetivo", width=100)
        self.tree.column("monto_actual", width=100)
        self.tree.column("progreso", width=80)
        self.tree.column("fecha_inicio", width=90)
        self.tree.column("fecha_limite", width=90)
        self.tree.column("estado", width=100)
        self.tree.bind("<Double-1>", lambda e: self.aportar())

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.cargar()

    def volver(self):
        self.root.destroy()

    def cargar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        filtro = self.filtro_combo.get()
        datos = Ahorro.listar_por_ciudadano(self.ciudadano["id_ciudadano"])

        for r in datos:
            if filtro != _("Todas") and r["estado"] != filtro:
                continue
            pct = (r["monto_actual"] / r["monto_objetivo"] * 100) if r["monto_objetivo"] > 0 else 0
            self.tree.insert("", tk.END, iid=r["id_ahorro"], values=(
                r["meta"],
                f"S/ {r['monto_objetivo']:.2f}",
                f"S/ {r['monto_actual']:.2f}",
                f"{pct:.0f}%",
                r["fecha_inicio"],
                r["fecha_limite"] or "-",
                r["estado"],
            ))

    def _selected(self):
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    def agregar(self):
        DialogoAhorro(self.root, self.ciudadano, guardar_callback=lambda: self._on_guardar("creada"))

    def _on_guardar(self, accion, desc=None):
        Historial.registrar(
            self.ciudadano["id_ciudadano"], _("Meta %s") % accion,
            desc or _("Meta de ahorro %s por %s") % (accion, self.ciudadano['nombre']),
        )
        self.cargar()

    def aportar(self):
        id_a = self._selected()
        if not id_a:
            messagebox.showerror(_("Error"), _("Selecciona una meta"))
            return
        a = Ahorro.obtener(id_a)
        if a:
            DialogoAportar(self.root, a, guardar_callback=lambda: self._on_guardar("aportada", _("Aporte a meta '%s'") % a['meta']))

    def editar(self):
        id_a = self._selected()
        if not id_a:
            messagebox.showerror(_("Error"), _("Selecciona una meta"))
            return
        a = Ahorro.obtener(id_a)
        if a:
            DialogoAhorro(self.root, self.ciudadano, ahorro=a, guardar_callback=lambda: self._on_guardar("actualizada"))

    def eliminar(self):
        id_a = self._selected()
        if not id_a:
            messagebox.showerror("Error", "Selecciona una meta")
            return
        a = Ahorro.obtener(id_a)
        if not a:
            return
        if messagebox.askyesno(_("Confirmar"), _("¿Eliminar meta '%s'?") % a['meta']):
            exito, msg = Ahorro.eliminar(id_a)
            if exito:
                self._on_guardar("eliminada", _("Meta '%s' eliminada") % a['meta'])
            else:
                messagebox.showerror(_("Error"), msg)


class DialogoAhorro(tk.Toplevel):
    def __init__(self, parent, ciudadano, ahorro=None, guardar_callback=None):
        super().__init__(parent)
        self.ciudadano = ciudadano
        self.ahorro = ahorro
        self.guardar_callback = guardar_callback
        titulo = _("Editar Meta") if ahorro else _("Nueva Meta de Ahorro")
        self.title(titulo)
        self.geometry("400x250")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Meta:")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.meta_entry = ttk.Entry(frame, width=40)
        self.meta_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text=_("Monto Objetivo (S/):")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.monto_entry = ttk.Entry(frame, width=40)
        self.monto_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text=_("Fecha Límite:")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.fecha_entry = ttk.Entry(frame, width=40)
        self.fecha_entry.grid(row=2, column=1, pady=5)
        ttk.Label(frame, text=_("(YYYY-MM-DD, opcional)"), font=("Arial", 8)).grid(row=3, column=1, sticky=tk.W)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(15, 0))
        ttk.Button(btn_frame, text=_("Guardar"), command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Cancelar"), command=self.destroy).pack(side=tk.LEFT, padx=5)

        if ahorro:
            self.cargar_datos()

    def cargar_datos(self):
        a = self.ahorro
        self.meta_entry.insert(0, a["meta"])
        self.monto_entry.insert(0, str(a["monto_objetivo"]))
        self.fecha_entry.insert(0, a["fecha_limite"] or "")

    def guardar(self):
        meta = self.meta_entry.get().strip()
        try:
            monto = float(self.monto_entry.get().strip())
        except ValueError:
            messagebox.showerror(_("Error"), _("El monto debe ser numérico"))
            return
        fecha_limite = self.fecha_entry.get().strip() or None

        if not meta or monto <= 0:
            messagebox.showerror(_("Error"), _("Meta y monto positivo son obligatorios"))
            return

        if self.ahorro:
            exito, msg = Ahorro.actualizar(self.ahorro["id_ahorro"], meta, monto, fecha_limite)
        else:
            exito, msg = Ahorro.agregar(self.ciudadano["id_ciudadano"], meta, monto, fecha_limite)

        if exito:
            messagebox.showinfo("Éxito", msg)
            if self.guardar_callback:
                self.guardar_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", msg)


class DialogoAportar(tk.Toplevel):
    def __init__(self, parent, ahorro, guardar_callback=None):
        super().__init__(parent)
        self.ahorro = ahorro
        self.guardar_callback = guardar_callback
        self.title(_("Aportar a Meta"))
        self.geometry("350x180")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Meta: %s") % ahorro['meta'], font=("Arial", 10, "bold")).pack(anchor=tk.W)
        pct = (ahorro["monto_actual"] / ahorro["monto_objetivo"] * 100) if ahorro["monto_objetivo"] > 0 else 0
        ttk.Label(frame, text=_("Progreso: S/ %s / S/ %s (%d%%)") % (f"{ahorro['monto_actual']:.2f}", f"{ahorro['monto_objetivo']:.2f}", pct)).pack(anchor=tk.W, pady=5)
        self.progress = ttk.Progressbar(frame, length=300, value=pct)
        self.progress.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame, text=_("Monto a aportar (S/):")).pack(anchor=tk.W)
        self.monto_entry = ttk.Entry(frame, width=30)
        self.monto_entry.pack(fill=tk.X, pady=5)
        self.monto_entry.focus()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=(10, 0))
        ttk.Button(btn_frame, text=_("Aportar"), command=self.aportar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Cancelar"), command=self.destroy).pack(side=tk.LEFT, padx=5)

    def aportar(self):
        try:
            monto = float(self.monto_entry.get().strip())
        except ValueError:
            messagebox.showerror(_("Error"), _("Monto debe ser numérico"))
            return
        if monto <= 0:
            messagebox.showerror(_("Error"), _("El monto debe ser positivo"))
            return

        exito, msg = Ahorro.aportar(self.ahorro["id_ahorro"], monto)
        if exito:
            messagebox.showinfo("Éxito", msg)
            if self.guardar_callback:
                self.guardar_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", msg)
