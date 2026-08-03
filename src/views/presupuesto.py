import tkinter as tk
from tkinter import messagebox, ttk
from src.models.presupuesto import Presupuesto
from src.models.historial import Historial
from src.models.destino import Destino
from src.models.restaurante import Restaurante
from src.models.transporte import Transporte
from src.models.hospedaje import Hospedaje
from src.i18n import _


class VentanaPresupuesto:
    def __init__(self, root, ciudadano):
        self.root = root
        self.ciudadano = ciudadano
        self.root.title(_("Qory Ayacucho - Planificador de Viaje"))
        self.root.geometry("550x650")
        self.root.resizable(False, False)

        main = ttk.Frame(root, padding="15")
        main.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main, text=_("Planificador de Viaje Integrado"), style="Heading.TLabel").pack(pady=(0, 15))

        input_frame = ttk.LabelFrame(main, text=_("Datos del Viaje"), padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text=_("Presupuesto Total (S/):")).grid(row=0, column=0, sticky=tk.W, pady=3)
        self.total_entry = ttk.Entry(input_frame, width=30)
        self.total_entry.grid(row=0, column=1, pady=3, padx=(10, 0))

        ttk.Label(input_frame, text=_("Días de Viaje:")).grid(row=1, column=0, sticky=tk.W, pady=3)
        self.dias_entry = ttk.Entry(input_frame, width=30)
        self.dias_entry.grid(row=1, column=1, pady=3, padx=(10, 0))

        ttk.Label(input_frame, text=_("Fecha (AAAA-MM-DD):")).grid(row=2, column=0, sticky=tk.W, pady=3)
        self.fecha_entry = ttk.Entry(input_frame, width=30)
        self.fecha_entry.grid(row=2, column=1, pady=3, padx=(10, 0))

        seleccion = ttk.LabelFrame(main, text=_("Selecciona tus Opciones"), padding="10")
        seleccion.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(seleccion, text=_("Destino Turístico:")).grid(row=0, column=0, sticky=tk.W, pady=3)
        self.destino_combo = ttk.Combobox(seleccion, state="readonly", width=35)
        self.destino_combo.grid(row=0, column=1, pady=3, padx=(10, 0))

        ttk.Label(seleccion, text=_("Restaurante:")).grid(row=1, column=0, sticky=tk.W, pady=3)
        self.restaurante_combo = ttk.Combobox(seleccion, state="readonly", width=35)
        self.restaurante_combo.grid(row=1, column=1, pady=3, padx=(10, 0))

        ttk.Label(seleccion, text=_("Transporte:")).grid(row=2, column=0, sticky=tk.W, pady=3)
        self.transporte_combo = ttk.Combobox(seleccion, state="readonly", width=35)
        self.transporte_combo.grid(row=2, column=1, pady=3, padx=(10, 0))

        ttk.Label(seleccion, text=_("Hospedaje:")).grid(row=3, column=0, sticky=tk.W, pady=3)
        self.hospedaje_combo = ttk.Combobox(seleccion, state="readonly", width=35)
        self.hospedaje_combo.grid(row=3, column=1, pady=3, padx=(10, 0))

        self._cargar_opciones()

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(btn_frame, text=_("Calcular Costo Real"), command=self.calcular).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Guardar Presupuesto"), command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Limpiar"), command=self.limpiar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Volver"), command=self.volver, style="Secondary.TButton").pack(side=tk.RIGHT, padx=5)

        self.resultado_frame = ttk.LabelFrame(main, text=_("Resultado"), padding="10")
        self.resultado_frame.pack(fill=tk.BOTH, expand=True)

        self.resultado_text = tk.StringVar()
        ttk.Label(self.resultado_frame, textvariable=self.resultado_text, justify=tk.LEFT).pack(anchor=tk.W)

    def _cargar_opciones(self):
        destinos = Destino.listar_todos()
        self.destinos_map = {f"{d['nombre']} ({d['provincia']})": d["id_destino"] for d in destinos}
        self.destino_combo["values"] = list(self.destinos_map.keys())
        if self.destinos_map:
            self.destino_combo.current(0)

        restaurantes = Restaurante.listar_todos()
        self.restaurantes_map = {f"{r['nombre']} - S/ {r['precio_max']:.0f}/día": r["id_restaurante"] for r in restaurantes}
        self.restaurante_combo["values"] = list(self.restaurantes_map.keys())
        if self.restaurantes_map:
            self.restaurante_combo.current(0)

        transportes = Transporte.listar_todos()
        self.transportes_map = {f"{t['nombre']} - S/ {t['precio']:.0f}": t["id_transporte"] for t in transportes}
        self.transporte_combo["values"] = list(self.transportes_map.keys())
        if self.transportes_map:
            self.transporte_combo.current(0)

        hospedajes = Hospedaje.listar_todos()
        self.hospedajes_map = {f"{h['nombre']} - S/ {h['precio_max']:.0f}/noche": h["id_hospedaje"] for h in hospedajes}
        self.hospedaje_combo["values"] = list(self.hospedajes_map.keys())
        if self.hospedajes_map:
            self.hospedaje_combo.current(0)

    def calcular(self):
        try:
            total = float(self.total_entry.get().strip())
            dias = int(self.dias_entry.get().strip())
        except ValueError:
            messagebox.showerror(_("Error"), _("Presupuesto y días deben ser valores numéricos"))
            return

        if total <= 0 or dias <= 0:
            messagebox.showerror(_("Error"), _("Los valores deben ser mayores a cero"))
            return

        sel_destino = self.destino_combo.get()
        sel_restaurante = self.restaurante_combo.get()
        sel_transporte = self.transporte_combo.get()
        sel_hospedaje = self.hospedaje_combo.get()

        if not all([sel_destino, sel_restaurante, sel_transporte, sel_hospedaje]):
            messagebox.showerror(_("Error"), _("Selecciona un destino, restaurante, transporte y hospedaje"))
            return

        id_destino = self.destinos_map[sel_destino]
        id_restaurante = self.restaurantes_map[sel_restaurante]
        id_transporte = self.transportes_map[sel_transporte]
        id_hospedaje = self.hospedajes_map[sel_hospedaje]

        r = Presupuesto.calcular_integrado(total, dias, id_destino, id_restaurante, id_transporte, id_hospedaje)
        if not r:
            messagebox.showerror(_("Error"), _("No se pudieron obtener los datos seleccionados"))
            return

        estado = _("✅ DENTRO DEL PRESUPUESTO") if r["dentro_presupuesto"] else _("❌ EXCEDE EL PRESUPUESTO")
        texto = (
            f"Presupuesto: S/ {r['presupuesto']:.2f}\n"
            f"Costo Real Estimado: S/ {r['costo_total']:.2f}\n"
            f"Diferencia: S/ {r['diferencia']:.2f}  —  {estado}\n\n"
            f"━━━ Desglose ━━━\n"
            f"  Destino ({r['destino']}): S/ {r['costo_destino']:.2f}\n"
            f"  Comida × {dias} días ({r['restaurante']}): S/ {r['costo_comida']:.2f}\n"
            f"  Transporte ({r['transporte']}): S/ {r['costo_transporte']:.2f}\n"
            f"  Alojamiento × {dias} noches ({r['hospedaje']}): S/ {r['costo_alojamiento']:.2f}\n"
        )
        self.resultado_text.set(texto)

    def guardar(self):
        try:
            total = float(self.total_entry.get().strip())
            dias = int(self.dias_entry.get().strip())
        except ValueError:
            messagebox.showerror(_("Error"), _("Presupuesto y días deben ser valores numéricos"))
            return

        destino = self.destino_combo.get().split(" (")[0] if self.destino_combo.get() else ""
        fecha = self.fecha_entry.get().strip()

        p = Presupuesto(self.ciudadano["id_ciudadano"], total, dias, destino, fecha)
        exito, mensaje = p.guardar()
        if exito:
            Historial.registrar(
                self.ciudadano["id_ciudadano"], _("Presupuesto"),
                _("Presupuesto creado: S/ %s para %d días en %s") % (total, dias, destino or _("sin destino")),
            )
            messagebox.showinfo(_("Éxito"), mensaje)
        else:
            messagebox.showerror(_("Error"), mensaje)

    def limpiar(self):
        self.total_entry.delete(0, tk.END)
        self.dias_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.resultado_text.set("")
        if self.destinos_map:
            self.destino_combo.current(0)
        if self.restaurantes_map:
            self.restaurante_combo.current(0)
        if self.transportes_map:
            self.transporte_combo.current(0)
        if self.hospedajes_map:
            self.hospedaje_combo.current(0)

    def volver(self):
        self.root.destroy()
