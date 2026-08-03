import tkinter as tk
from src.database import init_db
from src.theme import setup_theme
from src.views.inicio import VentanaInicio


def main():
    init_db()
    root = tk.Tk()
    setup_theme()
    VentanaInicio(root)
    root.mainloop()


if __name__ == "__main__":
    main()
