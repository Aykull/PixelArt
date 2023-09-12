import os
import time
import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageSequence

main_win = tk.Tk()
main_win.title("PixelArt")
main_win.geometry("1100x700")
main_win.resizable(False, False)

gens_out = 10
pops_out = 10

out_img_gif = []

def load_in_img():
    root = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=(("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif"), ("Todos los archivos", "*.*"))
    )
    if root:
        img = Image.open(root)
        wid, leng = img.size
        if wid > 500 or leng > 500:
            img = img.resize((500, 500), Image.ANTIALIAS)
        img_sharp = img.filter(ImageFilter.SHARPEN)

        img_tk = ImageTk.PhotoImage(img_sharp)
        disp_in.config(image=img_tk)
        disp_in.image = img_tk

def gen():
    print("Generanding :3")

def load_out_img():
    out_img = Image.open("gif\link1.png")
    wid_out, leng_out = out_img.size
    if wid_out > 500 or leng_out > 500:
        out_img = out_img.resize((500, 500), Image.ANTIALIAS) 
    out_img_tk = ImageTk.PhotoImage(out_img)
    disp_out.config(image=out_img_tk)
    disp_out.image = out_img_tk

def update_out_img():
    while True:
        load_out_img()
        time.sleep(3)

def generate_gif():
    for out in os.listdir("gif"):
        if out.endswith((".jpg", ".jpeg", ".png", ".gif")):
            out_root = os.path.join("gif", out)
            out_img_gif.append(out_root)
    out_gif = []
    for out_img_root in out_img_gif:
        out_img = Image.open(out_img_root)
        resize_out = out_img.resize((500, 500), Image.ANTIALIAS) 
        out_gif.append(resize_out)

    out_gif[0].save("gif\image.gif", save_all=True, append_images=out_gif[1:], duration=500, loop=0)

def pop_up_gif():
    pop_up_gif = tk.Toplevel(main_win, width=500, height=500)
    pop_up_gif.title("Resultado como GIF")

    gif = Image.open("gif\image.gif")
    frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]  
    
    label = tk.Label(pop_up_gif)
    label.pack()
    
    def update_frame(frame_num):
        label.config(image=frames[frame_num])
        pop_up_gif.after(100, update_frame, (frame_num + 1) % len(frames))
    
    update_frame(0)

def pop_up_graf():
    pop_up_graf = tk.Toplevel(main_win, width=500, height=500)
    pop_up_graf.title("Gráfico")

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

load_button = tk.Button(main_win, text="Cargar Imagen", command=load_in_img)
load_button.place(x=80, y=90)

play_button = tk.Button(main_win, text="Generar Imagen", command=gen)
play_button.place(x=190, y=90)

disp_in = tk.Label(main_win, width=500, height=500)
disp_in.place(x=20, y=130)

disp_out = tk.Label(main_win, width=500, height=500)
disp_out.place(x=570, y=130)

update_out = threading.Thread(target=update_out_img)
update_out.daemon = True
update_out.start()

pop_up_gif()

main_win.mainloop()
