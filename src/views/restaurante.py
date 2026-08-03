import tkinter as tk
from tkinter import messagebox, ttk
from src.models.restaurante import Restaurante
from src.i18n import _


class VentanaRestaurante:
    def __init__(self, root):
        self.root = root
        self.root.title(_("Qory Ayacucho - Restaurantes"))
        self.root.geometry("750x500")
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

        columns = ("nombre", "provincia", "tipo_comida", "precio_min", "precio_max", "especialidad")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        self.tree.heading("nombre", text=_("Nombre"))
        self.tree.heading("provincia", text=_("Provincia"))
        self.tree.heading("tipo_comida", text=_("Tipo"))
        self.tree.heading("precio_min", text=_("Precio Mín (S/)"))
        self.tree.heading("precio_max", text=_("Precio Máx (S/)"))
        self.tree.heading("especialidad", text=_("Especialidad"))
        self.tree.column("nombre", width=180)
        self.tree.column("provincia", width=100)
        self.tree.column("tipo_comida", width=80)
        self.tree.column("precio_min", width=90)
        self.tree.column("precio_max", width=90)
        self.tree.column("especialidad", width=180)
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
        opciones = [_("Todas")] + Restaurante.tipos_comida() + Restaurante.provincias()
        self.filtro_combo["values"] = opciones
        self.filtro_combo.current(0)

    def _get_filtro(self):
        sel = self.filtro_combo.get()
        if not sel or sel == _("Todas"):
            return None, None
        if sel in Restaurante.tipos_comida():
            return "tipo", sel
        if sel in Restaurante.provincias():
            return "provincia", sel
        return None, None

    def cargar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        tipo, valor = self._get_filtro()
        if tipo == "tipo":
            datos = Restaurante.listar_por_tipo(valor)
        elif tipo == "provincia":
            datos = Restaurante.listar_por_provincia(valor)
        else:
            datos = Restaurante.listar_todos()

        for r in datos:
            self.tree.insert("", tk.END, iid=r["id_restaurante"], values=(
                r["nombre"], r["provincia"], r["tipo_comida"],
                f"S/ {r['precio_min']:.2f}", f"S/ {r['precio_max']:.2f}",
                r["especialidad"],
            ))

    def _selected(self):
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    def agregar(self):
        DialogoRestaurante(self.root, guardar_callback=lambda: self.cargar())

    def editar(self):
        id_r = self._selected()
        if not id_r:
            messagebox.showerror(_("Error"), _("Selecciona un restaurante"))
            return
        r = Restaurante.obtener(id_r)
        if r:
            DialogoRestaurante(self.root, restaurante=r, guardar_callback=lambda: self.cargar())

    def eliminar(self):
        id_r = self._selected()
        if not id_r:
            messagebox.showerror(_("Error"), _("Selecciona un restaurante"))
            return
        r = Restaurante.obtener(id_r)
        if not r:
            return
        if messagebox.askyesno(_("Confirmar"), _("¿Eliminar %s?") % r['nombre']):
            exito, msg = Restaurante.eliminar(id_r)
            if exito:
                self.cargar()
            messagebox.showinfo(_("Éxito") if exito else _("Error"), msg)


class DialogoRestaurante(tk.Toplevel):
    def __init__(self, parent, restaurante=None, guardar_callback=None):
        super().__init__(parent)
        self.restaurante = restaurante
        self.guardar_callback = guardar_callback
        titulo = _("Editar Restaurante") if restaurante else _("Agregar Restaurante")
        self.title(titulo)
        self.geometry("450x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Nombre:")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nombre_entry = ttk.Entry(frame, width=40)
        self.nombre_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text=_("Provincia:")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.provincia_combo = ttk.Combobox(frame, values=Restaurante.provincias(), state="readonly", width=37)
        self.provincia_combo.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text=_("Tipo de Comida:")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.tipo_combo = ttk.Combobox(frame, values=Restaurante.tipos_comida(), state="readonly", width=37)
        self.tipo_combo.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text=_("Precio Mín (S/):")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.min_entry = ttk.Entry(frame, width=40)
        self.min_entry.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text=_("Precio Máx (S/):")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.max_entry = ttk.Entry(frame, width=40)
        self.max_entry.grid(row=4, column=1, pady=5)

        ttk.Label(frame, text=_("Especialidad:")).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.especialidad_entry = ttk.Entry(frame, width=40)
        self.especialidad_entry.grid(row=5, column=1, pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(15, 0))
        ttk.Button(btn_frame, text=_("Guardar"), command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Cancelar"), command=self.destroy).pack(side=tk.LEFT, padx=5)

        if restaurante:
            self.cargar_datos()

    def cargar_datos(self):
        r = self.restaurante
        self.nombre_entry.insert(0, r["nombre"])
        self.provincia_combo.set(r["provincia"])
        self.tipo_combo.set(r["tipo_comida"])
        self.min_entry.insert(0, str(r["precio_min"]))
        self.max_entry.insert(0, str(r["precio_max"]))
        self.especialidad_entry.insert(0, r["especialidad"] or "")

    def guardar(self):
        nombre = self.nombre_entry.get().strip()
        provincia = self.provincia_combo.get()
        tipo = self.tipo_combo.get()
        try:
            precio_min = float(self.min_entry.get().strip())
            precio_max = float(self.max_entry.get().strip())
        except ValueError:
            messagebox.showerror(_("Error"), _("Precios deben ser numéricos"))
            return
        especialidad = self.especialidad_entry.get().strip()

        if not nombre or not provincia or not tipo:
            messagebox.showerror(_("Error"), _("Nombre, provincia y tipo son obligatorios"))
            return
        if precio_min < 0 or precio_max < 0:
            messagebox.showerror(_("Error"), _("Los precios deben ser positivos"))
            return

        if self.restaurante:
            exito, msg = Restaurante.actualizar(
                self.restaurante["id_restaurante"], provincia, tipo, nombre, precio_min, precio_max, especialidad,
            )
        else:
            exito, msg = Restaurante.agregar(provincia, tipo, nombre, precio_min, precio_max, especialidad)

        if exito:
            messagebox.showinfo(_("Éxito"), msg)
            if self.guardar_callback:
                self.guardar_callback()
            self.destroy()
        else:
            messagebox.showerror(_("Error"), msg)
