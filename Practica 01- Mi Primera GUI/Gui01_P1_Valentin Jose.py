import tkinter as tk

root = tk.Tk()
root.title("Mi primera GUI")
root.geometry("360x200")

lbl = tk.Label(root, text="¡Hola, GUI!")
lbl.pack(pady=10)

root.mainloop()
