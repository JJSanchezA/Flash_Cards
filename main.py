# Importamos las librerías necesarias para el proyecto
import csv
import tkinter
from tkinter import messagebox

# Constantes
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Courier"
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
RUTA_ARCHIVO_CSV = "data/french_words.csv"

# variables necesarias
img_front = None
img_back = None
img_right = None
img_wrong = None
id_card_front = None
id_card_back = None
id_text_card = None
lst_palabras = []
lst_descartadas = []
global_dupla = []
# Pasamos a los datos de la carga
# Lista con las configuraciones de cada escenario. Se pasan como lista de variables.
lista_conf = []
# Variable para ver hacia qué lado hay que hacer flip.
flip_carta = False
# Color del texto, según haya o no flip
text_colour_f = "grey"
text_colour_b = "blue"


# ---------------------------- Cargar datos palabras desde CSV--------- #
def cargar_archivo_palabras(ruta):
    # Intentamos cargar el archivo
    error = False
    try:
        archivo_csv = open(file=ruta, mode="r")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message=f"Error, Archivo {ruta} no encontrado.")
        error = True
    else:
        # Leemos el contenido del archivo
        listado_palabras = csv.reader(archivo_csv)
        for linea in listado_palabras:
            # Cada línea debería tener un par de palabras separadas por coma.
            # Guardamos una lista de duplas (palabra idioma a, palabra idioma b)
            try:
                lst_palabras.append([linea[0], linea[1]])
            except IndexError:
                messagebox.showerror(title="Error", message=f"Fallo de formato en el archivo {ruta}.")
                error = True
                break
    finally:
        return error


# ----- Iniciar una partida cargando el archivo y sacando una tupla  ---#
def iniciar_nueva_partida():
    global global_dupla
    # Cargamos las listas de palabras desde el archivo.
    error_en_carga = cargar_archivo_palabras(RUTA_ARCHIVO_CSV)
    # Si no hay fallos al cargar el archivo csv, seguimos la ejecución normal.
    if not error_en_carga:
        # Bucle del main
        # Si no hay click de ratón, seguimos y no esperamos en el mainloop
        # La primera iteración entrará ya que tiene el valor click = "init"
        # Sacamos la primera tarjeta, que debe ser el idioma
        global_dupla = sacar_nueva_dupla()


# ----------- Sacar otra dupla y actualizar listas  --------------------#
def sacar_nueva_dupla():
    global lista_conf
    nueva_dupla = []
    # Sacamos otra dupla y la mostramos
    if len(lst_palabras) > 0:
        nueva_dupla = lst_palabras[0]
        lista_conf = [canvas_card, id_card_front, id_card_back, id_text_card,
              nueva_dupla[0], nueva_dupla[1], text_colour_f, text_colour_b]
        # Volteamos la carta al lado front por si está en modo back.
        if flip_carta:
            flip_card(lista_conf)
        # Mostramos la palabra pregunta
        flip_card(lista_conf)
    return nueva_dupla


# --------------------------- Poner texto en card - ------------------- #
def poner_texto_en_card(canvas, id_canvas_texto, texto_insertar, color):
    # Le paso el canvas y el id del texto del cambias para poder cambiarlo
    canvas.itemconfig(id_canvas_texto, text=texto_insertar)
    # Le cambio el color
    canvas.itemconfig(id_canvas_texto, fill=color)


# ---------------------------- Flip card ------------------------------ #
def flip_card(lista_configuraciones):
    # Saco las configuraciones de la lista (Lo hago así por claridad)
    canvas = lista_configuraciones[0]
    id_card_f = lista_configuraciones[1]
    id_card_b = lista_configuraciones[2]
    id_text_c = lista_configuraciones[3]
    text_front = lista_configuraciones[4]
    text_back = lista_configuraciones[5]
    color_text_front = lista_configuraciones[6]
    color_text_back = lista_configuraciones[7]

    # Para ocultar o mostrar un canvas usaremos
    # canvas.itemconfigure(id, state='hidden'/'normal')
    # Así simulamos el giro de la carta.
    global flip_carta
    if flip_carta:
        canvas.itemconfigure(id_card_f, state='hidden')
        canvas.itemconfigure(id_card_b, state='normal')
        flip_carta = False
        poner_texto_en_card(canvas, id_text_c, text_back, color_text_back)

    else:
        canvas.itemconfigure(id_card_f, state='normal')
        canvas.itemconfigure(id_card_b, state='hidden')
        flip_carta = True
        poner_texto_en_card(canvas, id_text_c, text_front, color_text_front)


# ---------------------------- click canvas card ---------------------- #
def click_on_cavas_card(event):
    # Las configuraciones las tengo guardada ya en la lista
    # Solo llamo a la función
    flip_card(lista_conf)


# ---------------------------- click wrong ---------------------------- #
def click_on_cavas_wrong(event):
    global global_dupla
    if len(lst_palabras) > 1:
        # Saco la dupla
        lst_palabras.remove(global_dupla)
        # y la meto al final
        lst_palabras.append(global_dupla)
        global_dupla = sacar_nueva_dupla()


# ---------------------------- click OK  ------------------------------ #
def click_on_cavas_right(event):
    global global_dupla
    # ¿Hemos terminado?
    if len(lst_palabras) == 1:
        # Acabamos de acertar la última! :)
        res = messagebox.askyesno(title="Enhorabuena", message="Has finalizado correctamente todas las cartas!! \
                                                         ¿Desea repetir?")
        if res:
            # iniciamos una nueva partida
            iniciar_nueva_partida()
            # Quitamos la última tupla
            lst_palabras.remove(global_dupla)
            # Sacamos la primera tupla de la nueva partida. Ya estamos listos
            sacar_nueva_dupla()
        else:
            ventana.destroy()
    else:
        # Sacamos otra dupla
        # Sí la he acertado. Paso la dupla a descartadas
        # Sacamos esa dupla y la pasamos a la lista de descartadas
        lst_palabras.remove(global_dupla)
        lst_descartadas.append(global_dupla)
        global_dupla = sacar_nueva_dupla()


# ---------------------------- UI SETUP ------------------------------- #
ventana = tkinter.Tk()
ventana.title(VENTANA_TITLE)
ventana.minsize(width=VENTANA_WIDTH, height=VENTANA_WIDTH)
# La configuramos para que no sea resizable
ventana.resizable(width=False, height=False)
ventana.config(padx=VENTANA_PAD_X, pady=VENTANA_PAD_Y)
# Creamos la estructura de imágenes. Primero cargamos las imágenes desde data.
carga_imgs_correcta = True
# Creo variables fuera del try para no recibir error de variables "indefinidas" fuera del try
canvas_card = None
canvas_right = None
canvas_wrong = None
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
    # Creamos e insertamos las imágenes en la ventana (El orden es importante en el flip)
    id_card_back = canvas_card.create_image(CARD_W/2, CARD_H/2, image=img_back)
    canvas_card.grid(row=0, column=0, columnspan=2)
    id_card_front = canvas_card.create_image(CARD_W/2, CARD_H/2, image=img_front)
    # (Le pongo un ID (int) para más tarde poder cambiar el texto)
    id_text_card = canvas_card.create_text(CARD_W/2-1, CARD_H/2, text="",
                                           fill=text_colour_f, font=(FONT_NAME, 35, "bold"))
    canvas_card.grid(row=0, column=0, columnspan=2)
    # Seguimos con el posicionamiento de los botones_canvas
    canvas_right = tkinter.Canvas(width=BUTTON_SIZE, heigh=BUTTON_SIZE)
    canvas_right.create_image(BUTTON_SIZE/2, BUTTON_SIZE/2, image=img_right)
    canvas_right.grid(row=1, column=1)
    canvas_wrong = tkinter.Canvas(width=BUTTON_SIZE, heigh=BUTTON_SIZE)
    canvas_wrong.create_image(BUTTON_SIZE/2, BUTTON_SIZE/2, image=img_wrong)
    canvas_wrong.grid(row=1, column=0)
# Si la carga es correcta, seguimos
if carga_imgs_correcta:
    # Hacemos el binding de ratón para detectar los clicks en lo canvas-botones.
    canvas_right.bind("<Button-1>", click_on_cavas_right)
    canvas_wrong.bind("<Button-1>", click_on_cavas_wrong)
    canvas_card.bind("<Button-1>", click_on_cavas_card)
    # Iniciamos la partida cargando el archivo y sacando la primera tupla
    iniciar_nueva_partida()
else:
    messagebox.showinfo(title="Error", message="Error cargando el entorno gráfico.")
# Main loop
ventana.mainloop()
