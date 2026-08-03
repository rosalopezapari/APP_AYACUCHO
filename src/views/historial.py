import tkinter as tk
from tkinter import ttk
from src.models.historial import Historial
from src.i18n import _


class VentanaHistorial:
    def __init__(self, root, ciudadano):
        self.root = root
        self.ciudadano = ciudadano
        self.root.title(_("Qory Ayacucho - Historial de Actividades"))
        self.root.geometry("700x450")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Historial de Actividades"), style="Heading.TLabel").pack(pady=(0, 10))

        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(filter_frame, text=_("Filtrar por tipo:")).pack(side=tk.LEFT, padx=(0, 5))
        self.tipo_combo = ttk.Combobox(filter_frame, state="readonly", width=25)
        self.tipo_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.tipo_combo.bind("<<ComboboxSelected>>", lambda e: self.cargar())

        ttk.Button(filter_frame, text=_("Mostrar Todo"), command=self.cargar_sin_filtro).pack(side=tk.LEFT)

        columns = ("fecha", "tipo", "descripcion")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        self.tree.heading("fecha", text=_("Fecha"))
        self.tree.heading("tipo", text=_("Tipo de Actividad"))
        self.tree.heading("descripcion", text=_("Descripción"))
        self.tree.column("fecha", width=160)
        self.tree.column("tipo", width=140)
        self.tree.column("descripcion", width=370)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(frame, text=_("Volver"), command=self.volver, style="Secondary.TButton").pack(pady=(5, 0))
        self.cargar()

    def cargar(self):
        tipo = self.tipo_combo.get()
        tipo = None if tipo == "" or tipo == "Todas" else tipo
        registros = Historial.obtener_por_ciudadano(self.ciudadano["id_ciudadano"], tipo)
        self._poblar_tabla(registros)

    def cargar_sin_filtro(self):
        self.tipo_combo.set("")
        self.cargar()

    def _poblar_tabla(self, registros):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in registros:
            self.tree.insert("", tk.END, values=(r["fecha"], r["tipo_actividad"], r["descripcion"]))

        tipos = Historial.tipos_actividad()
        self.tipo_combo["values"] = [_("Todas")] + tipos

    def volver(self):
        self.root.destroy()
