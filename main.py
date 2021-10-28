# Importamos las librerias necesarias para el proyecto
import random
import tkinter
from tkinter import messagebox

# Constantes
BACKGROUND_COLOR = "#B1DDC6"
VENTANA_TITLE = "Flash Cards"
VENTANA_WIDTH = 400
VENTANA_HEIGHT = 300
VENTANA_PAD_X = 20
VENTANA_PAD_Y = 20
CARD_W = 400
CARD_H = 263
BUTTON_SIZE = 50
IMAGEN_FRONT = "images/card_front.png"
IMAGEN_BACK = "images/card_back.png"
IMAGEN_RIGHT = "images/right.png"
IMAGEN_WRONG = "images/wrong.png"

# variables necesarias
img_front = None
img_back = None
img_right = None
img_wrong = None
id_card_front = None
id_card_back = None


# ---------------------------- Flip card ------------------------------ #
def flip_card(canvas, id_card, flip):
    # Para ocultar o mostrar un canvas usaremos
    # canvas.itemconfigure(id, state='hidden'/'normal')
    if flip:
        canvas.itemconfigure(id_card, state='hidden')
    else:
        canvas.itemconfigure(id_card, state='normal')


# ---------------------------- click OK  ------------------------------ #
def click_on_cavas_wrong(event):
    print("Oh no!")


# ---------------------------- click OK  ------------------------------ #
def click_on_cavas_right(event):
    print("Yeah")


# ---------------------------- UI SETUP ------------------------------- #
ventana = tkinter.Tk()
ventana.title(VENTANA_TITLE)
ventana.minsize(width=VENTANA_WIDTH, height=VENTANA_WIDTH)
# La configuramos para que no sea resizable
ventana.resizable(width=False, height=False)
ventana.config(padx=VENTANA_PAD_X, pady=VENTANA_PAD_Y)
# Creamos la estructura de imágenes. Primero cargamos las imágenes desde data.
carga_imgs_correcta = True
try:
    img_front = tkinter.PhotoImage(file=IMAGEN_FRONT)
    img_back = tkinter.PhotoImage(file=IMAGEN_BACK)
    img_right = tkinter.PhotoImage(file=IMAGEN_RIGHT)
    img_wrong = tkinter.PhotoImage(file=IMAGEN_WRONG)
except FileNotFoundError:
    # Si alguna no se puede cargar, no ejecutamos el software.
    messagebox.showinfo(title="Error", message="Error cargando las imágenes")
    carga_imgs_correcta = False
except NameError:
    # Si alguna no se puede cargar, no ejecutamos el software.
    messagebox.showinfo(title="Error", message="Error cargando las imágenes")
    carga_imgs_correcta = False
else:
    # Creo el canvas del tamaña del minsize
    canvas_card = tkinter.Canvas(width=CARD_W, heigh=CARD_H)
    # Creamos e insertamos las imágenes en la ventana
    id_card_front = canvas_card.create_image(CARD_W/2, CARD_H/2, image=img_front)
    canvas_card.grid(row=0, column=0, columnspan=2)
    id_card_back = canvas_card.create_image(CARD_W/2, CARD_H/2, image=img_back)
    canvas_card.grid(row=0, column=0, columnspan=2)
    canvas_right = tkinter.Canvas(width=BUTTON_SIZE, heigh=BUTTON_SIZE)
    canvas_right.create_image(BUTTON_SIZE/2, BUTTON_SIZE/2, image=img_right)
    canvas_right.grid(row=1, column=1)
    canvas_wrong = tkinter.Canvas(width=BUTTON_SIZE, heigh=BUTTON_SIZE)
    canvas_wrong.create_image(BUTTON_SIZE/2, BUTTON_SIZE/2, image=img_wrong)
    canvas_wrong.grid(row=1, column=0)

# Hacemos el binding de ratón para detectar los clicks en lo canvas-botones.
canvas_right.bind("<Button-1>", click_on_cavas_right)
canvas_wrong.bind("<Button-1>", click_on_cavas_wrong)
# Bucle del main
ventana.mainloop()

