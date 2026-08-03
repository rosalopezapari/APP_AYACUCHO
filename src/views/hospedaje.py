import tkinter as tk
from tkinter import messagebox, ttk
from src.models.hospedaje import Hospedaje
from src.i18n import _


class VentanaHospedaje:
    def __init__(self, root):
        self.root = root
        self.root.title(_("Qory Ayacucho - Hospedajes"))
        self.root.geometry("800x520")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(toolbar, text=_("Filtrar:")).pack(side=tk.LEFT, padx=(0, 5))
        self.filtro_combo = ttk.Combobox(toolbar, state="readonly", width=20)
        self.filtro_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.filtro_combo.bind("<<ComboboxSelected>>", lambda e: self.cargar())
        ttk.Button(toolbar, text=_("Mostrar Todos"), command=self.cargar).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar, text=_("Volver"), command=self.volver, style="Secondary.TButton").pack(side=tk.LEFT)
        ttk.Button(toolbar, text=_("Agregar"), command=self.agregar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar, text=_("Editar"), command=self.editar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar, text=_("Eliminar"), command=self.eliminar).pack(side=tk.RIGHT)

        columns = ("nombre", "tipo", "provincia", "precio_min", "precio_max", "servicios", "telefono")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        self.tree.heading("nombre", text=_("Nombre"))
        self.tree.heading("tipo", text=_("Tipo"))
        self.tree.heading("provincia", text=_("Provincia"))
        self.tree.heading("precio_min", text=_("Mín (S/)"))
        self.tree.heading("precio_max", text=_("Máx (S/)"))
        self.tree.heading("servicios", text=_("Servicios"))
        self.tree.heading("telefono", text=_("Teléfono"))
        self.tree.column("nombre", width=180)
        self.tree.column("tipo", width=80)
        self.tree.column("provincia", width=100)
        self.tree.column("precio_min", width=70)
        self.tree.column("precio_max", width=70)
        self.tree.column("servicios", width=200)
        self.tree.column("telefono", width=90)
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
        opciones = [_("Todas")] + Hospedaje.tipos() + Hospedaje.provincias()
        self.filtro_combo["values"] = opciones
        self.filtro_combo.current(0)

    def _get_filtro(self):
        sel = self.filtro_combo.get()
        if not sel or sel == _("Todas"):
            return None, None
        if sel in Hospedaje.tipos():
            return "tipo", sel
        if sel in Hospedaje.provincias():
            return "provincia", sel
        return None, None

    def cargar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        tipo_f, valor = self._get_filtro()
        if tipo_f == "tipo":
            datos = Hospedaje.listar_por_tipo(valor)
        elif tipo_f == "provincia":
            datos = Hospedaje.listar_por_provincia(valor)
        else:
            datos = Hospedaje.listar_todos()

        for r in datos:
            self.tree.insert("", tk.END, iid=r["id_hospedaje"], values=(
                r["nombre"], r["tipo"], r["provincia"],
                f"S/ {r['precio_min']:.2f}", f"S/ {r['precio_max']:.2f}",
                r["servicios"] or "-", r["telefono"] or "-",
            ))

    def _selected(self):
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    def agregar(self):
        DialogoHospedaje(self.root, guardar_callback=lambda: self.cargar())

    def editar(self):
        id_h = self._selected()
        if not id_h:
            messagebox.showerror(_("Error"), _("Selecciona un hospedaje"))
            return
        h = Hospedaje.obtener(id_h)
        if h:
            DialogoHospedaje(self.root, hospedaje=h, guardar_callback=lambda: self.cargar())

    def eliminar(self):
        id_h = self._selected()
        if not id_h:
            messagebox.showerror(_("Error"), _("Selecciona un hospedaje"))
            return
        h = Hospedaje.obtener(id_h)
        if not h:
            return
        if messagebox.askyesno(_("Confirmar"), _("¿Eliminar %s?") % h['nombre']):
            exito, msg = Hospedaje.eliminar(id_h)
            if exito:
                self.cargar()
            messagebox.showinfo(_("Éxito") if exito else _("Error"), msg)


class DialogoHospedaje(tk.Toplevel):
    def __init__(self, parent, hospedaje=None, guardar_callback=None):
        super().__init__(parent)
        self.hospedaje = hospedaje
        self.guardar_callback = guardar_callback
        titulo = _("Editar Hospedaje") if hospedaje else _("Agregar Hospedaje")
        self.title(titulo)
        self.geometry("450x330")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Nombre:")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nombre_entry = ttk.Entry(frame, width=40)
        self.nombre_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text=_("Tipo:")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.tipo_combo = ttk.Combobox(frame, values=Hospedaje.tipos(), state="readonly", width=37)
        self.tipo_combo.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text=_("Provincia:")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.provincia_combo = ttk.Combobox(frame, values=Hospedaje.provincias(), state="readonly", width=37)
        self.provincia_combo.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text=_("Precio Mín (S/):")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.min_entry = ttk.Entry(frame, width=40)
        self.min_entry.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text=_("Precio Máx (S/):")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.max_entry = ttk.Entry(frame, width=40)
        self.max_entry.grid(row=4, column=1, pady=5)

        ttk.Label(frame, text=_("Servicios:")).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.servicios_entry = ttk.Entry(frame, width=40)
        self.servicios_entry.grid(row=5, column=1, pady=5)

        ttk.Label(frame, text=_("Teléfono:")).grid(row=6, column=0, sticky=tk.W, pady=5)
        self.telefono_entry = ttk.Entry(frame, width=40)
        self.telefono_entry.grid(row=6, column=1, pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btn_frame, text=_("Guardar"), command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Cancelar"), command=self.destroy).pack(side=tk.LEFT, padx=5)

        if hospedaje:
            self.cargar_datos()

    def cargar_datos(self):
        h = self.hospedaje
        self.nombre_entry.insert(0, h["nombre"])
        self.tipo_combo.set(h["tipo"])
        self.provincia_combo.set(h["provincia"])
        self.min_entry.insert(0, str(h["precio_min"]))
        self.max_entry.insert(0, str(h["precio_max"]))
        self.servicios_entry.insert(0, h["servicios"] or "")
        self.telefono_entry.insert(0, h["telefono"] or "")

    def guardar(self):
        nombre = self.nombre_entry.get().strip()
        tipo = self.tipo_combo.get()
        provincia = self.provincia_combo.get()
        servicios = self.servicios_entry.get().strip() or None
        telefono = self.telefono_entry.get().strip() or None
        try:
            precio_min = float(self.min_entry.get().strip())
            precio_max = float(self.max_entry.get().strip())
        except ValueError:
            messagebox.showerror(_("Error"), _("Precios deben ser numéricos"))
            return

        if not nombre or not tipo or not provincia:
            messagebox.showerror(_("Error"), _("Nombre, tipo y provincia son obligatorios"))
            return
        if precio_min < 0 or precio_max < 0:
            messagebox.showerror(_("Error"), _("Los precios deben ser positivos"))
            return

        if self.hospedaje:
            exito, msg = Hospedaje.actualizar(
                self.hospedaje["id_hospedaje"], provincia, tipo, nombre, precio_min, precio_max, servicios, telefono,
            )
        else:
            exito, msg = Hospedaje.agregar(provincia, tipo, nombre, precio_min, precio_max, servicios, telefono)

        if exito:
            messagebox.showinfo(_("Éxito"), msg)
            if self.guardar_callback:
                self.guardar_callback()
            self.destroy()
        else:
            messagebox.showerror(_("Error"), msg)
