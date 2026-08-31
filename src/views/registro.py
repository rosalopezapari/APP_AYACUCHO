import tkinter as tk
from tkinter import messagebox, ttk
from src.models.ciudadano import Ciudadano
from src.models.historial import Historial
from src.views.login import VentanaLogin
from src.i18n import _


class VentanaRegistro:
    def __init__(self, root, volver_callback=None):
        self.root = root
        self.volver_callback = volver_callback
        self.root.title(_("Qory Ayacucho - Registro"))
        self.root.geometry("450x500")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Registro de Ciudadano"), style="Heading.TLabel").pack(pady=(0, 20))

        ttk.Label(frame, text=_("Nombre Completo:")).pack(anchor=tk.W)
        self.nombre_entry = ttk.Entry(frame, width=40)
        self.nombre_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame, text=_("Correo Electrónico:")).pack(anchor=tk.W)
        self.email_entry = ttk.Entry(frame, width=40)
        self.email_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame, text=_("Teléfono:")).pack(anchor=tk.W)
        self.telefono_entry = ttk.Entry(frame, width=40)
        self.telefono_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame, text=_("Contraseña (mín. 6 caracteres):")).pack(anchor=tk.W)
        self.contrasena_entry = ttk.Entry(frame, width=40, show="*")
        self.contrasena_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame, text=_("Confirmar Contraseña:")).pack(anchor=tk.W)
        self.confirmar_entry = ttk.Entry(frame, width=40, show="*")
        self.confirmar_entry.pack(fill=tk.X, pady=(0, 10))

        tk.Button(frame, text=_("CONFIRMAR REGISTRO"), command=self.registrar, font=("Arial", 11, "bold")).pack(pady=20)
        ttk.Button(frame, text=_("Ya tengo cuenta"), command=self.abrir_login, style="Secondary.TButton").pack()
        if volver_callback:
            ttk.Button(frame, text=_("Volver"), command=volver_callback, style="Secondary.TButton").pack(pady=(5, 0))

    def registrar(self):
        nombre = self.nombre_entry.get().strip()
        email = self.email_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        contrasena = self.contrasena_entry.get()
        confirmar = self.confirmar_entry.get()

        if not all([nombre, email, telefono, contrasena, confirmar]):
            messagebox.showerror(_("Error"), _("Todos los campos son obligatorios"))
            return

        if not Ciudadano.validar_email(email):
            messagebox.showerror(_("Error"), _("Correo electrónico inválido"))
            return

        if not Ciudadano.validar_telefono(telefono):
            messagebox.showerror(_("Error"), _("Teléfono inválido (solo números, 7-15 dígitos)"))
            return

        if not Ciudadano.validar_contrasena(contrasena):
            messagebox.showerror(_("Error"), _("La contraseña debe tener al menos 6 caracteres"))
            return

        if contrasena != confirmar:
            messagebox.showerror(_("Error"), _("Las contraseñas no coinciden"))
            return

        ciudadano = Ciudadano(nombre, email, telefono, contrasena)
        exito, mensaje = ciudadano.guardar()

        if exito:
            Historial.registrar(ciudadano.id_ciudadano, _("Registro"), _("Registro de %s (%s)") % (nombre, email))
            messagebox.showinfo(_("Éxito"), mensaje)
            self.limpiar_campos()
            if messagebox.askyesno(_("Inicio de Sesión"), _("¿Deseas iniciar sesión ahora?")):
                self.abrir_login()
        else:
            messagebox.showerror(_("Error"), mensaje)

    def abrir_login(self):
        self.root.withdraw()
        login_root = tk.Toplevel(self.root)
        login_root.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_hijo(login_root))
        VentanaLogin(login_root, volver_callback=lambda: self.cerrar_hijo(login_root))

    def cerrar_hijo(self, ventana):
        ventana.destroy()
        self.root.deiconify()

    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.contrasena_entry.delete(0, tk.END)
        self.confirmar_entry.delete(0, tk.END)
