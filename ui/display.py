import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

main_win = tk.Tk()
main_win.title("PixelArt")
main_win.geometry("1100x700")
main_win.resizable(False, False)

gens_out = 10
pops_out = 10

def load_img():
    root = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=(("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif"), ("Todos los archivos", "*.*"))
    )
    if root:
        img = Image.open(root)  
        img_tk = ImageTk.PhotoImage(img)
        disp_in.config(image=img_tk)
        disp_in.image = img_tk

def gen():
    print("Generanding :3")

generations = tk.Label(main_win, text="Número de generaciones")
generations.place(x=50, y=10)

gen_out = tk.Label(main_win, text=f"Número de generaciones {gens_out}")
gen_out.place(x=750, y=10)

entry_gen = tk.Entry(main_win)
entry_gen.place(x=200, y=10)

population = tk.Label(main_win, text="Tamaño de población")
population.place(x=50, y=50)

pop_out = tk.Label(main_win, text=f"Tamaño de población {pops_out}")
pop_out.place(x=750, y=50)

entry_pop = tk.Entry(main_win)
entry_pop.place(x=200, y=50)

load_button = tk.Button(main_win, text="Cargar Imagen", command=load_img)
load_button.place(x=80, y=90)

play_button = tk.Button(main_win, text="Generar Imagen", command=gen)
play_button.place(x=190, y=90)

disp_in = tk.Label(main_win, width=500, height=500)
disp_in.place(x=20, y=130)

disp_out = tk.Label(main_win, width=500, height=500)
disp_out.place(x=570, y=130)


main_win.mainloop()
