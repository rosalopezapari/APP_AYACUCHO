import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from src.models.exportador import Exportador
from src.models.historial import Historial
from src.i18n import _


class VentanaExportar:
    def __init__(self, root, ciudadano):
        self.root = root
        self.ciudadano = ciudadano
        self.root.title(_("Qory Ayacucho - Exportar Datos"))
        self.root.geometry("400x320")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Exportar Datos"), style="Title.TLabel").pack(pady=(0, 15))

        ttk.Label(frame, text=_("Selecciona los datos a exportar:"), style="Bold.TLabel").pack(anchor=tk.W)

        self.historial_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text=_("Historial de Actividades"), variable=self.historial_var).pack(anchor=tk.W, pady=3)

        self.presupuesto_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text=_("Presupuestos"), variable=self.presupuesto_var).pack(anchor=tk.W, pady=3)

        self.ahorro_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text=_("Metas de Ahorro"), variable=self.ahorro_var).pack(anchor=tk.W, pady=3)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        ttk.Label(frame, text=_("Formato de exportación:"), style="Bold.TLabel").pack(anchor=tk.W)

        self.formato_var = tk.StringVar(value="csv")
        ttk.Radiobutton(frame, text=_("CSV (Excel, hoja de cálculo)"), variable=self.formato_var, value="csv").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(frame, text=_("TXT (reporte formateado)"), variable=self.formato_var, value="txt").pack(anchor=tk.W, pady=2)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack()
        ttk.Button(btn_frame, text=_("Exportar"), command=self.exportar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Volver"), command=self.volver, style="Secondary.TButton").pack(side=tk.LEFT, padx=5)

    def exportar(self):
        seleccion = []
        if self.historial_var.get():
            seleccion.append("historial")
        if self.presupuesto_var.get():
            seleccion.append("presupuesto")
        if self.ahorro_var.get():
            seleccion.append("ahorro")

        if not seleccion:
            messagebox.showerror(_("Error"), _("Selecciona al menos un tipo de datos"))
            return

        formato = self.formato_var.get()
        ext = ".csv" if formato == "csv" else ".txt"
        desc = f"Archivo {formato.upper()}" if formato == "csv" else "Archivo de texto"

        if len(seleccion) == 1 and formato == "csv":
            nombres = {"historial": "historial", "presupuesto": "presupuestos", "ahorro": "metas_ahorro"}
            sugerido = f"{nombres[seleccion[0]]}{ext}"
        else:
            sugerido = f"reporte_qory_ayacucho{ext}"

        ruta = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[(desc, f"*{ext}")],
            initialfile=sugerido,
            title="Guardar archivo como",
        )
        if not ruta:
            return

        id_c = self.ciudadano["id_ciudadano"]
        exito_total = True
        mensajes = []

        if formato == "csv":
            if "historial" in seleccion:
                ok, msg = Exportador.exportar_historial_csv(id_c, ruta)
                exito_total &= ok
                mensajes.append(msg)
            if "presupuesto" in seleccion:
                if len(seleccion) > 1:
                    base, _ = os.path.splitext(ruta)
                    ruta = base + "_presupuestos.csv"
                ok, msg = Exportador.exportar_presupuestos_csv(id_c, ruta)
                exito_total &= ok
                mensajes.append(msg)
            if "ahorro" in seleccion:
                if len(seleccion) > 1:
                    base, _ = os.path.splitext(ruta)
                    ruta = base + "_metas_ahorro.csv"
                ok, msg = Exportador.exportar_ahorros_csv(id_c, ruta)
                exito_total &= ok
                mensajes.append(msg)
        else:
            ok, msg = Exportador.exportar_reporte_txt(id_c, ruta, self.ciudadano["nombre"])
            exito_total &= ok
            mensajes.append(msg)

        Historial.registrar(id_c, _("Exportación"), _("Datos exportados: %s en formato %s") % (', '.join(seleccion), formato.upper()))
        if exito_total:
            messagebox.showinfo(_("Éxito"), "\n".join(mensajes))
        else:
            messagebox.showerror(_("Error"), "\n".join(mensajes))

    def volver(self):
        self.root.destroy()
