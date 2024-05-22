import tkinter as tk

root = tk.Tk()

e = tk.Entry(root)
e.pack()

# ****************
a = 4
b = 5
c = a + b
d = "Mi resultado es: " + str(c)
# ****************
var = tk.StringVar()  # IntVar es para enteros, pero StringVar es para textos
e.config(textvariable=var)
var.set(d)  # yo le seteo un valor


root.mainloop()
