from tkinter import *
from tkinter import messagebox
from classroom import mostrarClassroom
from classroom import otorgarPermisos

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class ClassroomExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Classroom Explorer")

        # Button to trigger file exploration
        self.explore_button = ttk.Button(
            self.root, text="Explore Classroom", command=self.explore_classroom
        )
        self.explore_button.pack(pady=10)

        # Text widget to display the selected file
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.pack(padx=10, pady=10)

    def explore_classroom(self):
        creds= otorgarPermisos()
        classroom_info= mostrarClassroom(creds)

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, classroom_info)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClassroomExplorerApp(root)
    root.mainloop()
