import tkinter as tk
from tkinter import ttk
from src.i18n import _
from src.views.login import VentanaLogin
from src.views.registro import VentanaRegistro


class VentanaInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Qory Ayacucho")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding="30")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Qory Ayacucho"), style="Title.TLabel").pack(pady=(0, 5))
        ttk.Label(frame, text=_("Tu guía turística para la región Ayacucho"), style="Subtitle.TLabel").pack(pady=(0, 30))

        ttk.Button(frame, text=_("Inicio de Sesión"), command=self.abrir_login, width=25).pack(pady=5)
        ttk.Button(frame, text=_("Registro"), command=self.abrir_registro, width=25).pack(pady=5)
        ttk.Button(frame, text=_("Salir"), command=root.destroy, width=25, style="Secondary.TButton").pack(pady=(20, 5))

    def abrir_login(self):
        self.root.withdraw()
        login_root = tk.Toplevel(self.root)
        login_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(login_root))
        VentanaLogin(login_root, volver_callback=lambda: self.cerrar_hijo(login_root))

    def abrir_registro(self):
        self.root.withdraw()
        registro_root = tk.Toplevel(self.root)
        registro_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(registro_root))
        VentanaRegistro(registro_root, volver_callback=lambda: self.cerrar_hijo(registro_root))

    def cerrar_hijo(self, ventana):
        ventana.destroy()
        self.root.deiconify()
