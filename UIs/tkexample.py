import tkinter as tk
import sys

window = tk.Tk()
window.grid_columnconfigure(0, weight=1)
window.title("Lambda")
window.geometry("300x100")
label = tk.Label(window, text="Lambda Calculus")
label.grid(column=0, row=0)
button = tk.Button(
  window,
  text="Reverse",
  command=lambda: label.configure(text=''.join(reversed(label.cget("text")))),
)
button.grid(column=0, row=1)
window.mainloop()

