import tkinter as tk
from tkinter import messagebox, ttk
from src.models.evento_cultural import EventoCultural
from src.i18n import _


class VentanaEventoCultural:
    def __init__(self, root):
        self.root = root
        self.root.title(_("Qory Ayacucho - Eventos Culturales y Peñas"))
        self.root.geometry("850x550")
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

        columns = ("nombre", "tipo", "provincia", "fecha", "lugar", "precio")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        self.tree.heading("nombre", text=_("Nombre"))
        self.tree.heading("tipo", text=_("Tipo"))
        self.tree.heading("provincia", text=_("Provincia"))
        self.tree.heading("fecha", text=_("Fecha"))
        self.tree.heading("lugar", text=_("Lugar"))
        self.tree.heading("precio", text=_("Precio (S/)"))
        self.tree.column("nombre", width=200)
        self.tree.column("tipo", width=100)
        self.tree.column("provincia", width=100)
        self.tree.column("fecha", width=90)
        self.tree.column("lugar", width=200)
        self.tree.column("precio", width=80)
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
        opciones = [_("Todas")] + list(EventoCultural.TIPOS) + list(EventoCultural.PROVINCIAS)
        self.filtro_combo["values"] = opciones
        self.filtro_combo.current(0)

    def _get_filtro(self):
        sel = self.filtro_combo.get()
        if not sel or sel == _("Todas"):
            return None, None
        if sel in EventoCultural.TIPOS:
            return "tipo", sel
        if sel in EventoCultural.PROVINCIAS:
            return "provincia", sel
        return None, None

    def cargar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        tipo_f, valor = self._get_filtro()
        if tipo_f == "tipo":
            datos = EventoCultural.listar_por_tipo(valor)
        elif tipo_f == "provincia":
            datos = EventoCultural.listar_por_provincia(valor)
        else:
            datos = EventoCultural.listar_todos()

        for r in datos:
            precio_texto = _("Gratis") if r["precio_entrada"] == 0 else f"S/ {r['precio_entrada']:.2f}"
            self.tree.insert("", tk.END, iid=r["id_evento"], values=(
                r["nombre"], r["tipo"], r["provincia"],
                r["fecha"], r["lugar"], precio_texto,
            ))

    def _selected(self):
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    def agregar(self):
        DialogoEventoCultural(self.root, guardar_callback=lambda: self.cargar())

    def editar(self):
        id_e = self._selected()
        if not id_e:
            messagebox.showerror(_("Error"), _("Selecciona un evento"))
            return
        e = EventoCultural.obtener(id_e)
        if e:
            DialogoEventoCultural(self.root, evento=e, guardar_callback=lambda: self.cargar())

    def eliminar(self):
        id_e = self._selected()
        if not id_e:
            messagebox.showerror(_("Error"), _("Selecciona un evento"))
            return
        e = EventoCultural.obtener(id_e)
        if not e:
            return
        if messagebox.askyesno(_("Confirmar"), _("¿Eliminar evento '%s'?") % e['nombre']):
            exito, msg = EventoCultural.eliminar(id_e)
            if exito:
                self.cargar()
            messagebox.showinfo(_("Éxito") if exito else _("Error"), msg)


class DialogoEventoCultural(tk.Toplevel):
    def __init__(self, parent, evento=None, guardar_callback=None):
        super().__init__(parent)
        self.evento = evento
        self.guardar_callback = guardar_callback
        titulo = _("Editar Evento") if evento else _("Agregar Evento")
        self.title(titulo)
        self.geometry("500x420")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Nombre:")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nombre_entry = ttk.Entry(frame, width=40)
        self.nombre_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text=_("Tipo:")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.tipo_combo = ttk.Combobox(frame, values=list(EventoCultural.TIPOS), state="readonly", width=37)
        self.tipo_combo.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text=_("Provincia:")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.provincia_combo = ttk.Combobox(frame, values=list(EventoCultural.PROVINCIAS), state="readonly", width=37)
        self.provincia_combo.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text=_("Fecha (AAAA-MM-DD):")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.fecha_entry = ttk.Entry(frame, width=40)
        self.fecha_entry.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text=_("Lugar:")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.lugar_entry = ttk.Entry(frame, width=40)
        self.lugar_entry.grid(row=4, column=1, pady=5)

        ttk.Label(frame, text=_("Descripción:")).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.descripcion_entry = ttk.Entry(frame, width=40)
        self.descripcion_entry.grid(row=5, column=1, pady=5)

        ttk.Label(frame, text=_("Precio Entrada (S/):")).grid(row=6, column=0, sticky=tk.W, pady=5)
        self.precio_entry = ttk.Entry(frame, width=40)
        self.precio_entry.grid(row=6, column=1, pady=5)

        ttk.Label(frame, text=_("Organizador:")).grid(row=7, column=0, sticky=tk.W, pady=5)
        self.organizador_entry = ttk.Entry(frame, width=40)
        self.organizador_entry.grid(row=7, column=1, pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=(15, 0))
        ttk.Button(btn_frame, text=_("Guardar"), command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Cancelar"), command=self.destroy).pack(side=tk.LEFT, padx=5)

        if evento:
            self.cargar_datos()

    def cargar_datos(self):
        e = self.evento
        self.nombre_entry.insert(0, e["nombre"])
        self.tipo_combo.set(e["tipo"])
        self.provincia_combo.set(e["provincia"])
        self.fecha_entry.insert(0, e["fecha"])
        self.lugar_entry.insert(0, e["lugar"])
        self.descripcion_entry.insert(0, e["descripcion"] or "")
        self.precio_entry.insert(0, str(e["precio_entrada"]))
        self.organizador_entry.insert(0, e["organizador"] or "")

    def guardar(self):
        nombre = self.nombre_entry.get().strip()
        tipo = self.tipo_combo.get()
        provincia = self.provincia_combo.get()
        fecha = self.fecha_entry.get().strip()
        lugar = self.lugar_entry.get().strip()
        descripcion = self.descripcion_entry.get().strip() or None
        organizador = self.organizador_entry.get().strip() or None
        try:
            precio = float(self.precio_entry.get().strip())
        except ValueError:
            messagebox.showerror(_("Error"), _("El precio debe ser numérico"))
            return

        if not nombre or not tipo or not provincia or not fecha or not lugar:
            messagebox.showerror(_("Error"), _("Nombre, tipo, provincia, fecha y lugar son obligatorios"))
            return
        if precio < 0:
            messagebox.showerror(_("Error"), _("El precio debe ser positivo"))
            return

        if self.evento:
            exito, msg = EventoCultural.actualizar(
                self.evento["id_evento"], nombre, tipo, provincia, fecha, lugar, descripcion, precio, organizador,
            )
        else:
            exito, msg = EventoCultural.agregar(nombre, tipo, provincia, fecha, lugar, descripcion, precio, organizador)

        if exito:
            messagebox.showinfo(_("Éxito"), msg)
            if self.guardar_callback:
                self.guardar_callback()
            self.destroy()
        else:
            messagebox.showerror(_("Error"), msg)
