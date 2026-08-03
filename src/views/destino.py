import tkinter as tk
from tkinter import messagebox, ttk
from src.models.destino import Destino
from src.i18n import _


class VentanaDestino:
    def __init__(self, root):
        self.root = root
        self.root.title(_("Qory Ayacucho - Destinos Turísticos"))
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

        columns = ("nombre", "provincia", "categoria", "precio", "descripcion")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        self.tree.heading("nombre", text=_("Nombre"))
        self.tree.heading("provincia", text=_("Provincia"))
        self.tree.heading("categoria", text=_("Categoría"))
        self.tree.heading("precio", text=_("Precio (S/)"))
        self.tree.heading("descripcion", text=_("Descripción"))
        self.tree.column("nombre", width=200)
        self.tree.column("provincia", width=110)
        self.tree.column("categoria", width=100)
        self.tree.column("precio", width=80)
        self.tree.column("descripcion", width=280)
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
        opciones = [_("Todas")] + Destino.CATEGORIAS + Destino.PROVINCIAS
        self.filtro_combo["values"] = opciones
        self.filtro_combo.current(0)

    def _get_filtro(self):
        sel = self.filtro_combo.get()
        if not sel or sel == _("Todas"):
            return None, None
        if sel in Destino.CATEGORIAS:
            return "categoria", sel
        if sel in Destino.PROVINCIAS:
            return "provincia", sel
        return None, None

    def cargar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        tipo_f, valor = self._get_filtro()
        if tipo_f == "categoria":
            datos = Destino.listar_por_categoria(valor)
        elif tipo_f == "provincia":
            datos = Destino.listar_por_provincia(valor)
        else:
            datos = Destino.listar_todos()

        for r in datos:
            self.tree.insert("", tk.END, iid=r["id_destino"], values=(
                r["nombre"], r["provincia"], r["categoria"],
                f"S/ {r['precio']:.2f}", r["descripcion"] or "-",
            ))

    def _selected(self):
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    def agregar(self):
        DialogoDestino(self.root, guardar_callback=lambda: self.cargar())

    def editar(self):
        id_d = self._selected()
        if not id_d:
            messagebox.showerror(_("Error"), _("Selecciona un destino"))
            return
        d = Destino.obtener(id_d)
        if d:
            DialogoDestino(self.root, destino=d, guardar_callback=lambda: self.cargar())

    def eliminar(self):
        id_d = self._selected()
        if not id_d:
            messagebox.showerror(_("Error"), _("Selecciona un destino"))
            return
        d = Destino.obtener(id_d)
        if not d:
            return
        if messagebox.askyesno(_("Confirmar"), _("¿Eliminar %s?") % d['nombre']):
            exito, msg = Destino.eliminar(id_d)
            if exito:
                self.cargar()
            messagebox.showinfo(_("Éxito") if exito else _("Error"), msg)


class DialogoDestino(tk.Toplevel):
    def __init__(self, parent, destino=None, guardar_callback=None):
        super().__init__(parent)
        self.destino = destino
        self.guardar_callback = guardar_callback
        titulo = _("Editar Destino") if destino else _("Agregar Destino")
        self.title(titulo)
        self.geometry("450x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Nombre:")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nombre_entry = ttk.Entry(frame, width=40)
        self.nombre_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text=_("Provincia:")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.provincia_combo = ttk.Combobox(frame, values=Destino.PROVINCIAS, state="readonly", width=37)
        self.provincia_combo.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text=_("Categoría:")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.categoria_combo = ttk.Combobox(frame, values=Destino.CATEGORIAS, state="readonly", width=37)
        self.categoria_combo.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text=_("Precio (S/):")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.precio_entry = ttk.Entry(frame, width=40)
        self.precio_entry.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text=_("Descripción:")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.descripcion_entry = ttk.Entry(frame, width=40)
        self.descripcion_entry.grid(row=4, column=1, pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(15, 0))
        ttk.Button(btn_frame, text=_("Guardar"), command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Cancelar"), command=self.destroy).pack(side=tk.LEFT, padx=5)

        if destino:
            self.cargar_datos()

    def cargar_datos(self):
        d = self.destino
        self.nombre_entry.insert(0, d["nombre"])
        self.provincia_combo.set(d["provincia"])
        self.categoria_combo.set(d["categoria"])
        self.precio_entry.insert(0, str(d["precio"]))
        self.descripcion_entry.insert(0, d["descripcion"] or "")

    def guardar(self):
        nombre = self.nombre_entry.get().strip()
        provincia = self.provincia_combo.get()
        categoria = self.categoria_combo.get()
        descripcion = self.descripcion_entry.get().strip() or None
        try:
            precio = float(self.precio_entry.get().strip())
        except ValueError:
            messagebox.showerror(_("Error"), _("El precio debe ser numérico"))
            return

        if not nombre or not provincia or not categoria:
            messagebox.showerror(_("Error"), _("Nombre, provincia y categoría son obligatorios"))
            return
        if precio < 0:
            messagebox.showerror(_("Error"), _("El precio debe ser positivo"))
            return

        if self.destino:
            exito, msg = Destino.actualizar(
                self.destino["id_destino"], provincia, categoria, nombre, precio, descripcion,
            )
        else:
            exito, msg = Destino.agregar(provincia, categoria, nombre, precio, descripcion)

        if exito:
            messagebox.showinfo(_("Éxito"), msg)
            if self.guardar_callback:
                self.guardar_callback()
            self.destroy()
        else:
            messagebox.showerror(_("Error"), msg)
