import tkinter as tk
from tkinter import messagebox, ttk
from src.models.ciudadano import Ciudadano
from src.models.historial import Historial
from src.i18n import _


class VentanaPerfil:
    def __init__(self, root, ciudadano):
        self.root = root
        self.ciudadano = ciudadano
        self.root.title(_("Qory Ayacucho - Editar Perfil"))
        self.root.geometry("450x400")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=_("Editar Perfil"), style="Title.TLabel").pack(pady=(0, 20))

        ttk.Label(frame, text=_("Nombre Completo:")).pack(anchor=tk.W)
        self.nombre_entry = ttk.Entry(frame, width=45)
        self.nombre_entry.pack(fill=tk.X, pady=(0, 10))
        self.nombre_entry.insert(0, ciudadano["nombre"])

        ttk.Label(frame, text=_("Correo Electrónico:")).pack(anchor=tk.W)
        self.email_entry = ttk.Entry(frame, width=45)
        self.email_entry.pack(fill=tk.X, pady=(0, 10))
        self.email_entry.insert(0, ciudadano["email"])

        ttk.Label(frame, text=_("Teléfono:")).pack(anchor=tk.W)
        self.telefono_entry = ttk.Entry(frame, width=45)
        self.telefono_entry.pack(fill=tk.X, pady=(0, 10))
        self.telefono_entry.insert(0, ciudadano["telefono"])

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(frame, text=_("Cambiar Contraseña (dejar en blanco para mantener actual):"), font=("Arial", 9)).pack(anchor=tk.W)

        self.contrasena_entry = ttk.Entry(frame, width=45, show="*")
        self.contrasena_entry.pack(fill=tk.X, pady=(5, 5))

        self.confirmar_entry = ttk.Entry(frame, width=45, show="*")
        self.confirmar_entry.pack(fill=tk.X, pady=(0, 10))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=(10, 0))
        ttk.Button(btn_frame, text=_("Guardar Cambios"), command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_("Cancelar"), command=self.volver, style="Secondary.TButton").pack(side=tk.LEFT, padx=5)

    def guardar(self):
        nombre = self.nombre_entry.get().strip()
        email = self.email_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        contrasena = self.contrasena_entry.get()
        confirmar = self.confirmar_entry.get()

        if not all([nombre, email, telefono]):
            messagebox.showerror(_("Error"), _("Nombre, email y teléfono son obligatorios"))
            return

        if not Ciudadano.validar_email(email):
            messagebox.showerror(_("Error"), _("Correo electrónico inválido"))
            return

        if not Ciudadano.validar_telefono(telefono):
            messagebox.showerror(_("Error"), _("Teléfono inválido (solo números, 7-15 dígitos)"))
            return

        if contrasena or confirmar:
            if not Ciudadano.validar_contrasena(contrasena):
                messagebox.showerror(_("Error"), _("La contraseña debe tener al menos 6 caracteres"))
                return
            if contrasena != confirmar:
                messagebox.showerror(_("Error"), _("Las contraseñas no coinciden"))
                return

        contrasena_final = contrasena if contrasena else None
        exito, msg = Ciudadano.actualizar(
            self.ciudadano["id_ciudadano"], nombre, email, telefono, contrasena_final,
        )

        if exito:
            Historial.registrar(
                self.ciudadano["id_ciudadano"], _("Perfil"),
                _("Perfil actualizado: %s (%s)") % (nombre, email),
            )
            self.ciudadano["nombre"] = nombre
            self.ciudadano["email"] = email
            self.ciudadano["telefono"] = telefono
            messagebox.showinfo(_("Éxito"), msg)
            self.volver()
        else:
            messagebox.showerror(_("Error"), msg)

    def volver(self):
        self.root.destroy()
