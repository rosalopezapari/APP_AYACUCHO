import tkinter as tk
from tkinter import messagebox, ttk
from src.models.reserva import Reserva
from src.i18n import _


class VentanaReserva:
    def __init__(self, root, ciudadano):
        self.root = root
        self.ciudadano = ciudadano
        self.root.title(_("Qory Ayacucho - Mis Reservas"))
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Gestión de Reservas"), style="Title.TLabel").pack(pady=(0, 10))

        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(toolbar, text=_("Filtrar:")).pack(side=tk.LEFT, padx=(0, 5))
        self.filtro_combo = ttk.Combobox(toolbar, state="readonly", width=15)
        self.filtro_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.filtro_combo.bind("<<ComboboxSelected>>", lambda e: self.cargar())

        ttk.Button(toolbar, text=_("Todas"), command=self.cargar).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar, text=_("Volver"), command=self.volver, style="Secondary.TButton").pack(side=tk.LEFT)
        ttk.Button(toolbar, text=_("Nueva Reserva"), command=self.nueva).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar, text=_("Eliminar"), command=self.eliminar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar, text=_("Cancelar"), command=self.cancelar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar, text=_("Confirmar"), command=self.confirmar).pack(side=tk.RIGHT)

        columns = ("id", "servicio", "tipo", "fecha", "estado")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        self.tree.heading("id", text=_("#"))
        self.tree.heading("servicio", text=_("Servicio"))
        self.tree.heading("tipo", text=_("Tipo"))
        self.tree.heading("fecha", text=_("Fecha Reserva"))
        self.tree.heading("estado", text=_("Estado"))
        self.tree.column("id", width=40)
        self.tree.column("servicio", width=280)
        self.tree.column("tipo", width=120)
        self.tree.column("fecha", width=120)
        self.tree.column("estado", width=120)

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

        estado = self.filtro_combo.get()
        if estado and estado != "Todas":
            datos = Reserva.listar_por_estado(self.ciudadano["id_ciudadano"], estado)
        else:
            datos = Reserva.listar_por_ciudadano(self.ciudadano["id_ciudadano"])

        for r in datos:
            self.tree.insert("", tk.END, iid=r["id_reserva"], values=(
                r["id_reserva"], r["nombre_servicio"], r["tipo_servicio"],
                r["fecha_reserva"], r["estado"],
            ))

        estados = [""] + Reserva.estados()
        self.filtro_combo["values"] = estados

    def _selected(self):
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    def nueva(self):
        DialogoReserva(self.root, self.ciudadano, guardar_callback=lambda: self.cargar())

    def confirmar(self):
        id_r = self._selected()
        if not id_r:
            messagebox.showerror(_("Error"), _("Selecciona una reserva"))
            return
        exito, msg = Reserva.cambiar_estado(id_r, "Confirmada")
        if exito:
            self.cargar()
        messagebox.showinfo(_("Éxito") if exito else _("Error"), msg)

    def cancelar(self):
        id_r = self._selected()
        if not id_r:
            messagebox.showerror(_("Error"), _("Selecciona una reserva"))
            return
        if messagebox.askyesno(_("Confirmar"), _("¿Cancelar esta reserva?")):
            exito, msg = Reserva.cambiar_estado(id_r, "Cancelada")
            if exito:
                self.cargar()
            messagebox.showinfo(_("Éxito") if exito else _("Error"), msg)

    def eliminar(self):
        id_r = self._selected()
        if not id_r:
            messagebox.showerror(_("Error"), _("Selecciona una reserva"))
            return
        if messagebox.askyesno(_("Confirmar"), _("¿Eliminar esta reserva permanentemente?")):
            exito, msg = Reserva.eliminar(id_r)
            if exito:
                self.cargar()
            messagebox.showinfo(_("Éxito") if exito else _("Error"), msg)


class DialogoReserva(tk.Toplevel):
    def __init__(self, parent, ciudadano, guardar_callback=None):
        super().__init__(parent)
        self.ciudadano = ciudadano
        self.guardar_callback = guardar_callback
        self.title(_("Nueva Reserva"))
        self.geometry("450x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Tipo de Servicio:")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.tipo_combo = ttk.Combobox(frame, values=Reserva.tipos_servicio(), state="readonly", width=35)
        self.tipo_combo.grid(row=0, column=1, pady=5)
        self.tipo_combo.bind("<<ComboboxSelected>>", lambda e: self._cargar_servicios())

        ttk.Label(frame, text=_("Servicio:")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.servicio_combo = ttk.Combobox(frame, state="readonly", width=35)
        self.servicio_combo.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text=_("Fecha de Reserva:")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.fecha_entry = ttk.Entry(frame, width=35)
        self.fecha_entry.grid(row=2, column=1, pady=5)
        self.fecha_entry.insert(0, "YYYY-MM-DD")

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(15, 0))
        ttk.Button(btn_frame, text=_("Guardar"), command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Cancelar"), command=self.destroy).pack(side=tk.LEFT, padx=5)

    def _cargar_servicios(self):
        tipo = self.tipo_combo.get()
        if not tipo:
            return
        servicios = Reserva.obtener_servicios_por_tipo(tipo)
        nombres = []
        self._servicios_map = {}
        for s in servicios:
            label = f"{s['nombre']} (S/ {s.get('precio', s.get('precio_min', 0)):.0f})"
            nombres.append(label)
            self._servicios_map[label] = s
        self.servicio_combo["values"] = nombres

    def guardar(self):
        tipo = self.tipo_combo.get()
        sel = self.servicio_combo.get()
        fecha = self.fecha_entry.get().strip()

        if not tipo or not sel or not fecha:
            messagebox.showerror(_("Error"), _("Todos los campos son obligatorios"))
            return

        srv = self._servicios_map.get(sel)
        if not srv:
            messagebox.showerror(_("Error"), _("Selecciona un servicio válido"))
            return

        id_key = {
            "Restaurante": "id_restaurante",
            "Hospedaje": "id_hospedaje",
            "Transporte": "id_transporte",
            "Destino": "id_destino",
        }
        id_srv = srv.get(id_key[tipo])

        exito, msg = Reserva.agregar(
            self.ciudadano["id_ciudadano"], tipo, id_srv, srv["nombre"], fecha,
        )
        if exito:
            messagebox.showinfo(_("Éxito"), msg)
            if self.guardar_callback:
                self.guardar_callback()
            self.destroy()
        else:
            messagebox.showerror(_("Error"), msg)
