import tkinter as tk
from tkinter import ttk

COLORS = {
    "bg": "#FAF5EF",
    "fg": "#2D3436",
    "primary": "#8B4513",
    "primary_light": "#A0522D",
    "secondary": "#2C3E50",
    "accent": "#D4A574",
    "accent_light": "#E8D5C0",
    "success": "#27AE60",
    "error": "#C0392B",
    "white": "#FFFFFF",
    "input_bg": "#FFFFFF",
    "disabled_bg": "#F0EDE8",
}

FONTS = {
    "title": ("Arial", 16, "bold"),
    "heading": ("Arial", 14, "bold"),
    "subtitle": ("Arial", 12),
    "body": ("Arial", 10),
    "small": ("Arial", 9),
    "bold": ("Arial", 10, "bold"),
}


def setup_theme():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(".", font=FONTS["body"], background=COLORS["bg"], foreground=COLORS["fg"])

    style.configure("TFrame", background=COLORS["bg"])
    style.configure("TLabelframe", background=COLORS["bg"])
    style.configure("TLabelframe.Label", background=COLORS["bg"], font=FONTS["bold"], foreground=COLORS["primary"])

    style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["fg"])
    style.configure("Title.TLabel", font=FONTS["title"], foreground=COLORS["secondary"])
    style.configure("Heading.TLabel", font=FONTS["heading"], foreground=COLORS["primary"])
    style.configure("Subtitle.TLabel", font=FONTS["subtitle"], foreground=COLORS["secondary"])
    style.configure("Bold.TLabel", font=FONTS["bold"])

    style.configure("TButton", font=FONTS["body"], padding=(12, 6), background=COLORS["primary"], foreground=COLORS["white"])
    style.map("TButton",
        background=[("active", COLORS["primary_light"]), ("!active", COLORS["primary"])],
        foreground=[("active", COLORS["white"]), ("!active", COLORS["white"])],
    )

    style.configure("Secondary.TButton", background=COLORS["secondary"], foreground=COLORS["white"])
    style.map("Secondary.TButton",
        background=[("active", "#34495E"), ("!active", COLORS["secondary"])],
        foreground=[("active", COLORS["white"]), ("!active", COLORS["white"])],
    )

    style.configure("TEntry", fieldbackground=COLORS["input_bg"], padding=5, foreground=COLORS["fg"])
    style.configure("TCombobox", fieldbackground=COLORS["input_bg"], padding=5, foreground=COLORS["fg"])
    style.map("TCombobox",
        fieldbackground=[("readonly", COLORS["input_bg"])],
    )

    style.configure("Treeview",
        background=COLORS["white"],
        fieldbackground=COLORS["white"],
        foreground=COLORS["fg"],
        rowheight=30,
        font=FONTS["body"],
    )
    style.map("Treeview",
        background=[("selected", COLORS["accent_light"])],
        foreground=[("selected", COLORS["fg"])],
    )
    style.configure("Treeview.Heading", font=FONTS["bold"], padding=6, background=COLORS["accent"], foreground=COLORS["secondary"])
    style.map("Treeview.Heading",
        background=[("active", COLORS["accent_light"])],
    )

    style.configure("TSeparator", background=COLORS["accent"])

    style.configure("TProgressbar", background=COLORS["primary"], troughcolor=COLORS["accent_light"])
