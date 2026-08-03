import tkinter as tk
from tkinter import ttk
from src.i18n import _
from src.views.presupuesto import VentanaPresupuesto
from src.views.recomendacion import VentanaRecomendacion
from src.views.historial import VentanaHistorial
from src.views.restaurante import VentanaRestaurante
from src.views.tienda import VentanaTienda
from src.views.ahorro import VentanaAhorro
from src.views.transporte import VentanaTransporte
from src.views.hospedaje import VentanaHospedaje
from src.views.destino import VentanaDestino
from src.views.perfil import VentanaPerfil
from src.views.exportar import VentanaExportar
from src.views.reportes import VentanaReportes
from src.views.reserva import VentanaReserva


class VentanaMenu:
    def __init__(self, root, ciudadano):
        self.root = root
        self.ciudadano = ciudadano
        self.root.title("Qory Ayacucho - Menú Principal")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame,
            text=_("Bienvenido") + f", {ciudadano['nombre']}",
            style="Title.TLabel",
        ).pack(pady=(0, 5))

        info_frame = ttk.Frame(frame)
        info_frame.pack(pady=(0, 10))
        ttk.Label(
            info_frame,
            text=f"Email: {ciudadano['email']}",
            style="Subtitle.TLabel",
        ).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(
            info_frame,
            text=_("Editar Perfil"),
            command=self.abrir_perfil,
        ).pack(side=tk.LEFT)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        lang_frame = ttk.Frame(frame)
        lang_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(lang_frame, text=_("Idioma:")).pack(side=tk.LEFT, padx=(0, 5))
        self.lang_combo = ttk.Combobox(lang_frame, state="readonly", width=12)
        self.lang_combo.pack(side=tk.LEFT)
        self.lang_combo.bind("<<ComboboxSelected>>", lambda e: self._cambiar_idioma())

        ttk.Label(frame, text=_("Menú de Funcionalidades"), style="Subtitle.TLabel").pack(pady=(10, 5))

        ttk.Button(frame, text=_("Gestión de Presupuesto"), command=self.abrir_presupuesto).pack(fill=tk.X, pady=3)
        ttk.Button(frame, text=_("Recomendaciones de Viaje"), command=self.abrir_recomendacion).pack(fill=tk.X, pady=3)
        ttk.Button(frame, text=_("Destinos Turísticos"), command=self.abrir_destinos).pack(fill=tk.X, pady=3)
        ttk.Button(frame, text=_("Restaurantes"), command=self.abrir_restaurantes).pack(fill=tk.X, pady=3)
        ttk.Button(frame, text=_("Tiendas y Artesanías"), command=self.abrir_tiendas).pack(fill=tk.X, pady=3)
        ttk.Button(frame, text=_("Metas de Ahorro"), command=self.abrir_ahorro).pack(fill=tk.X, pady=3)
        ttk.Button(frame, text=_("Transporte"), command=self.abrir_transporte).pack(fill=tk.X, pady=3)
        ttk.Button(frame, text=_("Hospedajes"), command=self.abrir_hospedaje).pack(fill=tk.X, pady=3)
        ttk.Button(frame, text=_("Reservas"), command=self.abrir_reserva).pack(fill=tk.X, pady=3)
        ttk.Button(frame, text=_("Historial de Actividades"), command=self.abrir_historial).pack(fill=tk.X, pady=3)
        ttk.Button(frame, text=_("Exportar Datos"), command=self.abrir_exportar).pack(fill=tk.X, pady=3)
        ttk.Button(frame, text=_("Reportes y Estadísticas"), command=self.abrir_reportes).pack(fill=tk.X, pady=3)

        self._cargar_idiomas()

    def abrir_presupuesto(self):
        self.root.withdraw()
        presupuesto_root = tk.Toplevel(self.root)
        VentanaPresupuesto(presupuesto_root, self.ciudadano)
        presupuesto_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(presupuesto_root))

    def abrir_recomendacion(self):
        self.root.withdraw()
        recomendacion_root = tk.Toplevel(self.root)
        VentanaRecomendacion(recomendacion_root, self.ciudadano)
        recomendacion_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(recomendacion_root))

    def abrir_destinos(self):
        self.root.withdraw()
        destino_root = tk.Toplevel(self.root)
        VentanaDestino(destino_root)
        destino_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(destino_root))

    def abrir_restaurantes(self):
        self.root.withdraw()
        restaurante_root = tk.Toplevel(self.root)
        VentanaRestaurante(restaurante_root)
        restaurante_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(restaurante_root))

    def abrir_tiendas(self):
        self.root.withdraw()
        tienda_root = tk.Toplevel(self.root)
        VentanaTienda(tienda_root)
        tienda_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(tienda_root))

    def abrir_ahorro(self):
        self.root.withdraw()
        ahorro_root = tk.Toplevel(self.root)
        VentanaAhorro(ahorro_root, self.ciudadano)
        ahorro_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(ahorro_root))

    def abrir_transporte(self):
        self.root.withdraw()
        transporte_root = tk.Toplevel(self.root)
        VentanaTransporte(transporte_root)
        transporte_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(transporte_root))

    def abrir_hospedaje(self):
        self.root.withdraw()
        hospedaje_root = tk.Toplevel(self.root)
        VentanaHospedaje(hospedaje_root)
        hospedaje_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(hospedaje_root))

    def abrir_perfil(self):
        perfil_root = tk.Toplevel(self.root)
        perfil_root.transient(self.root)
        perfil_root.grab_set()
        VentanaPerfil(perfil_root, self.ciudadano)
        perfil_root.protocol("WM_DELETE_WINDOW", lambda: self._cerrar_perfil(perfil_root))

    def _cerrar_perfil(self, ventana):
        ventana.destroy()
        self._refrescar_cabecera()

    def _refrescar_cabecera(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.__init__(self.root, self.ciudadano)

    def abrir_exportar(self):
        exportar_root = tk.Toplevel(self.root)
        exportar_root.transient(self.root)
        exportar_root.grab_set()
        VentanaExportar(exportar_root, self.ciudadano)
        exportar_root.protocol("WM_DELETE_WINDOW", lambda: exportar_root.destroy())

    def abrir_reportes(self):
        self.root.withdraw()
        reportes_root = tk.Toplevel(self.root)
        VentanaReportes(reportes_root, self.ciudadano)
        reportes_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(reportes_root))

    def abrir_reserva(self):
        self.root.withdraw()
        reserva_root = tk.Toplevel(self.root)
        VentanaReserva(reserva_root, self.ciudadano)
        reserva_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(reserva_root))

    def abrir_historial(self):
        self.root.withdraw()
        historial_root = tk.Toplevel(self.root)
        VentanaHistorial(historial_root, self.ciudadano)
        historial_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(historial_root))

    def _cargar_idiomas(self):
        from src.i18n import available_languages, current_lang
        langs = available_languages()
        self.lang_codes = {name: code for code, name in langs}
        self.lang_combo["values"] = list(self.lang_codes.keys())
        current = current_lang()
        for code, name in langs:
            if code == current:
                self.lang_combo.set(name)
                break

    def _cambiar_idioma(self):
        from src.i18n import load_language
        name = self.lang_combo.get()
        code = self.lang_codes.get(name, "es")
        load_language(code)
        self._refrescar_cabecera()

    def cerrar_hijo(self, ventana):
        ventana.destroy()
        self.root.deiconify()
