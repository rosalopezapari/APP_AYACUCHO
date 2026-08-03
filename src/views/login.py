import tkinter as tk
from tkinter import messagebox, ttk
from src.models.ciudadano import Ciudadano
from src.models.historial import Historial
from src.views.menu_principal import VentanaMenu
from src.i18n import _


class VentanaLogin:
    def __init__(self, root, volver_callback=None):
        self.root = root
        self.volver_callback = volver_callback
        self.root.title(_("Qory Ayacucho - Inicio de Sesión"))
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Inicio de Sesión"), style="Heading.TLabel").pack(pady=(0, 20))

        ttk.Label(frame, text=_("Correo Electrónico:")).pack(anchor=tk.W)
        self.email_entry = ttk.Entry(frame, width=40)
        self.email_entry.pack(fill=tk.X, pady=(0, 10))
        self.email_entry.focus()

        ttk.Label(frame, text=_("Contraseña:")).pack(anchor=tk.W)
        self.contrasena_entry = ttk.Entry(frame, width=40, show="*")
        self.contrasena_entry.pack(fill=tk.X, pady=(0, 10))
        self.contrasena_entry.bind("<Return>", lambda e: self.iniciar_sesion())

        ttk.Button(frame, text=_("Iniciar Sesión"), command=self.iniciar_sesion).pack(pady=(10, 5))
        ttk.Button(frame, text=_("¿Olvidaste tu contraseña?"), command=self.recuperar, style="Secondary.TButton").pack(pady=(2, 5))
        if volver_callback:
            ttk.Button(frame, text=_("Volver"), command=volver_callback, style="Secondary.TButton").pack()

    def iniciar_sesion(self):
        email = self.email_entry.get().strip()
        contrasena = self.contrasena_entry.get()

        if not email or not contrasena:
            messagebox.showerror("Error", _("Todos los campos son obligatorios"))
            return

        exito, resultado = Ciudadano.iniciar_sesion(email, contrasena)
        if exito:
            Historial.registrar(resultado["id_ciudadano"], _("Inicio de Sesión"), _("Inicio de sesión de %s") % resultado['nombre'])
            messagebox.showinfo(_("Bienvenido"), _("Inicio de sesión exitoso. ¡Bienvenido %s!") % resultado['nombre'])
            top = self.root.winfo_toplevel()
            master = top.master
            top.destroy()
            master.destroy()
            root = tk.Tk()
            VentanaMenu(root, resultado)
            root.mainloop()
        else:
            messagebox.showerror(_("Error"), resultado)
