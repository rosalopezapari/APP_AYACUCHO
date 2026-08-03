import tkinter as tk
from tkinter import messagebox, ttk
from src.models.transporte import Transporte
from src.i18n import _


class VentanaTransporte:
    def __init__(self, root):
        self.root = root
        self.root.title(_("Qory Ayacucho - Transporte"))
        self.root.geometry("800x520")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(toolbar, text=_("Filtrar:")).pack(side=tk.LEFT, padx=(0, 5))
        self.filtro_combo = ttk.Combobox(toolbar, state="readonly", width=18)
        self.filtro_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.filtro_combo.bind("<<ComboboxSelected>>", lambda e: self.cargar())
        ttk.Button(toolbar, text=_("Mostrar Todos"), command=self.cargar).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar, text=_("Volver"), command=self.volver, style="Secondary.TButton").pack(side=tk.LEFT)
        ttk.Button(toolbar, text=_("Agregar"), command=self.agregar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar, text=_("Editar"), command=self.editar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar, text=_("Eliminar"), command=self.eliminar).pack(side=tk.RIGHT)

        columns = ("nombre", "tipo", "empresa", "origen", "destino", "precio", "duracion")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        self.tree.heading("nombre", text=_("Servicio"))
        self.tree.heading("tipo", text=_("Tipo"))
        self.tree.heading("empresa", text=_("Empresa"))
        self.tree.heading("origen", text=_("Origen"))
        self.tree.heading("destino", text=_("Destino"))
        self.tree.heading("precio", text=_("Precio (S/)"))
        self.tree.heading("duracion", text=_("Duración"))
        self.tree.column("nombre", width=180)
        self.tree.column("tipo", width=80)
        self.tree.column("empresa", width=130)
        self.tree.column("origen", width=110)
        self.tree.column("destino", width=110)
        self.tree.column("precio", width=80)
        self.tree.column("duracion", width=80)
        self.tree.bind("<Double-1>", lambda e: self.editar())

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.cargar_filtros()
        self.cargar()

    def volver(self):
        self.root.destroy()

    def cargar_filtros(self):
        opciones = [_("Todos")] + Transporte.tipos()
        self.filtro_combo["values"] = opciones
        self.filtro_combo.current(0)

    def cargar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        filtro = self.filtro_combo.get()
        datos = Transporte.listar_por_tipo(filtro) if filtro and filtro != _("Todos") else Transporte.listar_todos()

        for r in datos:
            self.tree.insert("", tk.END, iid=r["id_transporte"], values=(
                r["nombre"], r["tipo"], r["empresa"], r["origen"], r["destino"],
                f"S/ {r['precio']:.2f}", r["duracion"] or "-",
            ))

    def _selected(self):
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    def agregar(self):
        DialogoTransporte(self.root, guardar_callback=lambda: self.cargar())

    def editar(self):
        id_t = self._selected()
        if not id_t:
            messagebox.showerror(_("Error"), _("Selecciona un transporte"))
            return
        t = Transporte.obtener(id_t)
        if t:
            DialogoTransporte(self.root, transporte=t, guardar_callback=lambda: self.cargar())

    def eliminar(self):
        id_t = self._selected()
        if not id_t:
            messagebox.showerror(_("Error"), _("Selecciona un transporte"))
            return
        t = Transporte.obtener(id_t)
        if not t:
            return
        if messagebox.askyesno(_("Confirmar"), _("¿Eliminar %s?") % t['nombre']):
            exito, msg = Transporte.eliminar(id_t)
            if exito:
                self.cargar()
            messagebox.showinfo(_("Éxito") if exito else _("Error"), msg)


class DialogoTransporte(tk.Toplevel):
    def __init__(self, parent, transporte=None, guardar_callback=None):
        super().__init__(parent)
        self.transporte = transporte
        self.guardar_callback = guardar_callback
        titulo = _("Editar Transporte") if transporte else _("Agregar Transporte")
        self.title(titulo)
        self.geometry("450x320")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Nombre:")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nombre_entry = ttk.Entry(frame, width=40)
        self.nombre_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text=_("Tipo:")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.tipo_combo = ttk.Combobox(frame, values=Transporte.tipos(), state="readonly", width=37)
        self.tipo_combo.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text=_("Empresa:")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.empresa_combo = ttk.Combobox(frame, values=Transporte.empresas(), state="normal", width=37)
        self.empresa_combo.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text=_("Origen:")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.origen_entry = ttk.Entry(frame, width=40)
        self.origen_entry.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text=_("Destino:")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.destino_entry = ttk.Entry(frame, width=40)
        self.destino_entry.grid(row=4, column=1, pady=5)

        ttk.Label(frame, text=_("Precio (S/):")).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.precio_entry = ttk.Entry(frame, width=40)
        self.precio_entry.grid(row=5, column=1, pady=5)

        ttk.Label(frame, text=_("Duración:")).grid(row=6, column=0, sticky=tk.W, pady=5)
        self.duracion_entry = ttk.Entry(frame, width=40)
        self.duracion_entry.grid(row=6, column=1, pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btn_frame, text=_("Guardar"), command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Cancelar"), command=self.destroy).pack(side=tk.LEFT, padx=5)

        if transporte:
            self.cargar_datos()

    def cargar_datos(self):
        t = self.transporte
        self.nombre_entry.insert(0, t["nombre"])
        self.tipo_combo.set(t["tipo"])
        self.empresa_combo.set(t["empresa"])
        self.origen_entry.insert(0, t["origen"])
        self.destino_entry.insert(0, t["destino"])
        self.precio_entry.insert(0, str(t["precio"]))
        self.duracion_entry.insert(0, t["duracion"] or "")

    def guardar(self):
        nombre = self.nombre_entry.get().strip()
        tipo = self.tipo_combo.get()
        empresa = self.empresa_combo.get().strip()
        origen = self.origen_entry.get().strip()
        destino = self.destino_entry.get().strip()
        duracion = self.duracion_entry.get().strip() or None
        try:
            precio = float(self.precio_entry.get().strip())
        except ValueError:
            messagebox.showerror(_("Error"), _("El precio debe ser numérico"))
            return

        if not all([nombre, tipo, empresa, origen, destino]):
            messagebox.showerror(_("Error"), _("Todos los campos excepto duración son obligatorios"))
            return
        if precio < 0:
            messagebox.showerror(_("Error"), _("El precio debe ser positivo"))
            return

        if self.transporte:
            exito, msg = Transporte.actualizar(
                self.transporte["id_transporte"], tipo, empresa, nombre, origen, destino, precio, duracion,
            )
        else:
            exito, msg = Transporte.agregar(tipo, empresa, nombre, origen, destino, precio, duracion)

        if exito:
            messagebox.showinfo(_("Éxito"), msg)
            if self.guardar_callback:
                self.guardar_callback()
            self.destroy()
        else:
            messagebox.showerror(_("Error"), msg)
