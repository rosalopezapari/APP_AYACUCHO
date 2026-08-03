import tkinter as tk
from tkinter import ttk, messagebox
from src.models.recomendacion import Recomendacion
from src.models.historial import Historial
from src.i18n import _


class VentanaRecomendacion:
    def __init__(self, root, ciudadano):
        self.root = root
        self.ciudadano = ciudadano
        self.root.title(_("Qory Ayacucho - Recomendaciones de Viaje"))
        self.root.geometry("650x550")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Recomendaciones de Viaje"), style="Heading.TLabel").pack(pady=(0, 10))

        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text=_("Presupuesto Diario (S/):")).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.presupuesto_entry = ttk.Entry(input_frame, width=15)
        self.presupuesto_entry.grid(row=0, column=1, padx=(0, 10))

        ttk.Label(input_frame, text=_("Provincia:")).grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.provincia_combo = ttk.Combobox(input_frame, values=[_("Todas")] + Recomendacion.PROVINCIAS, state="readonly", width=20)
        self.provincia_combo.grid(row=0, column=3, padx=(0, 10))
        self.provincia_combo.current(0)

        ttk.Button(input_frame, text=_("Recomendar"), command=self.recomendar).grid(row=0, column=4)

        columns = ("nombre", "provincia", "categoria", "precio", "descripcion")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        self.tree.heading("nombre", text=_("Lugar"))
        self.tree.heading("provincia", text=_("Provincia"))
        self.tree.heading("categoria", text=_("Categoría"))
        self.tree.heading("precio", text=_("Precio (S/)"))
        self.tree.heading("descripcion", text=_("Descripción"))
        self.tree.column("nombre", width=180)
        self.tree.column("provincia", width=100)
        self.tree.column("categoria", width=90)
        self.tree.column("precio", width=80)
        self.tree.column("descripcion", width=180)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.info_label = ttk.Label(frame, text="", justify=tk.LEFT)
        self.info_label.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(frame, text=_("Volver"), command=self.volver, style="Secondary.TButton").pack(pady=(5, 0))

    def volver(self):
        self.root.destroy()

    def recomendar(self):
        try:
            presupuesto = float(self.presupuesto_entry.get().strip())
        except ValueError:
            messagebox.showerror(_("Error"), _("Ingresa un presupuesto diario válido"))
            return

        if presupuesto <= 0:
            messagebox.showerror(_("Error"), _("El presupuesto debe ser mayor a cero"))
            return

        provincia = self.provincia_combo.get()
        provincia = None if provincia == "Todas" else provincia

        rec = Recomendacion(presupuesto, 1)
        destinos = rec.recomendar(provincia)

        for row in self.tree.get_children():
            self.tree.delete(row)

        if not destinos:
            self.info_label.config(text=_("No hay destinos que se ajusten a tu presupuesto. Intenta con un presupuesto mayor."))
            return

        for d in destinos:
            self.tree.insert("", tk.END, values=(
                d["nombre"], d["provincia"], d["categoria"],
                f"S/ {d['precio']:.2f}", d["descripcion"],
            ))

        cant = len(destinos)
        precios = [d["precio"] for d in destinos]
        total = sum(precios)
        desc = f"Recomendación: {cant} lugares (S/ {total/cant:.2f} promedio) en {provincia or 'todas las provincias'}"
        Historial.registrar(self.ciudadano["id_ciudadano"], _("Recomendación"), desc)
        self.info_label.config(
            text=f"Encontrados {cant} lugares dentro de tu presupuesto.\n"
            f"Precio promedio: S/ {total/cant:.2f} | Rango: S/ {min(precios):.2f} - S/ {max(precios):.2f}"
        )
