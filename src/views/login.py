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

    def recuperar(self):
        DialogoRecuperarContrasena(self.root)


class DialogoRecuperarContrasena(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title(_("Recuperar Contraseña"))
        self.geometry("400x280")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Recuperar Contraseña"), style="Heading.TLabel").pack(pady=(0, 15))
        ttk.Label(frame, text=_("Ingresa tu correo electrónico para restablecer tu contraseña:")).pack(anchor=tk.W)

        ttk.Label(frame, text=_("Correo Electrónico:")).pack(anchor=tk.W, pady=(10, 0))
        self.email_entry = ttk.Entry(frame, width=40)
        self.email_entry.pack(fill=tk.X, pady=(0, 5))
        self.email_entry.focus()

        ttk.Button(frame, text=_("Buscar Cuenta"), command=self._buscar).pack(pady=(10, 5))

        self.frame_nueva = ttk.Frame(frame)
        self.nueva_label = None
        self.nueva_entry = None
        self.confirmar_label = None
        self.confirmar_entry = None
        self.btn_cambiar = None

    def _buscar(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showerror(_("Error"), _("Todos los campos son obligatorios"))
            return

        ciudadano = Ciudadano.obtener_por_email(email)
        if not ciudadano:
            messagebox.showerror(_("Error"), _("No se encontró una cuenta con ese correo electrónico"))
            return

        self.email_entry.config(state="disabled")
        self._ciudadano = ciudadano

        self.nueva_label = ttk.Label(self.frame_nueva, text=_("Contraseña (mín. 6 caracteres):"))
        self.nueva_label.pack(anchor=tk.W, pady=(10, 0))
        self.nueva_entry = ttk.Entry(self.frame_nueva, width=40, show="*")
        self.nueva_entry.pack(fill=tk.X, pady=(0, 5))

        self.confirmar_label = ttk.Label(self.frame_nueva, text=_("Confirmar Contraseña:"))
        self.confirmar_label.pack(anchor=tk.W)
        self.confirmar_entry = ttk.Entry(self.frame_nueva, width=40, show="*")
        self.confirmar_entry.pack(fill=tk.X, pady=(0, 5))

        self.btn_cambiar = ttk.Button(self.frame_nueva, text=_("Cambiar Contraseña"), command=self._cambiar)
        self.btn_cambiar.pack(pady=(10, 5))

        self.frame_nueva.pack(fill=tk.X)

    def _cambiar(self):
        nueva = self.nueva_entry.get()
        confirmar = self.confirmar_entry.get()

        if not nueva or not confirmar:
            messagebox.showerror(_("Error"), _("Todos los campos son obligatorios"))
            return

        if not Ciudadano.validar_contrasena(nueva):
            messagebox.showerror(_("Error"), _("La contraseña debe tener al menos 6 caracteres"))
            return

        if nueva != confirmar:
            messagebox.showerror(_("Error"), _("Las contraseñas no coinciden"))
            return

        exito, msg = Ciudadano.cambiar_contrasena(self._ciudadano["id_ciudadano"], nueva)
        if exito:
            messagebox.showinfo(_("Éxito"), msg)
            self.destroy()
        else:
            messagebox.showerror(_("Error"), msg)
