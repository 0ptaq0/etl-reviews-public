from Tkinter import *
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

def ETL():
    extract()
    transform()
    load()

def clean_data():
    #todo
    return

def extract():
    data_scrapping(input_film_title.get())
    button_transform.config(state=NORMAL)
    etl_bar_e.config(fg="red")
    print_msg_in_message_box("Data Extracted")

def transform():
    button_load.config(state=NORMAL)
    etl_bar_t.config(fg="red")
    print_msg_in_message_box("Data Transformed")

def load():
    etl_bar_l.config(fg="red")
    print_msg_in_message_box("Data Loaded")

def data_scrapping(film_url):
    page = get_page(film_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    html = list(soup.children)[1]
    head = list(html.children)[0]
    body = list(html.children)[1]

    film_title = list(head.children)[0]
    print(film_title)

def get_page(film_url):
    page = requests.get(film_url)
    return page

def print_msg_in_message_box(msg):
    msg_box_value.set("Info: " + msg)

main_window = Tk()
main_window.title("ETL Film Reviews")

msg_box_value = StringVar(main_window,value="Info: ")

frame_ETL_bar = Frame(main_window)
frame_ETL_bar.grid(row=0)

etl_bar_e = Label(frame_ETL_bar,text="E", font=("Helvetica", 24))
etl_bar_e.grid(row=0,column=0)

etl_bar_t = Label(frame_ETL_bar,text="T", font=("Helvetica", 24))
etl_bar_t.grid(row=0,column=1)

etl_bar_l = Label(frame_ETL_bar,text="L", font=("Helvetica", 24))
etl_bar_l.grid(row=0,column=2)

title_bar = Label(main_window,text="Film Reviews", font=("Helvetica", 12))
title_bar.grid(row=1)

input_film_title = Entry(main_window)
input_film_title.grid(row=2)

frame_ETL_buttons = Frame(main_window)
frame_ETL_buttons.grid(row=3)

button_ETL = Button(frame_ETL_buttons,text="ETL",command=ETL)
button_ETL.grid(row=0,column=1)

button_extract = Button(frame_ETL_buttons,text="Extract",command=extract)
button_extract.grid(row=1,column=0)

button_transform = Button(frame_ETL_buttons,text="Transform",state=DISABLED,command=transform)
button_transform.grid(row=1,column=1)

button_load = Button(frame_ETL_buttons,text="Load",state=DISABLED,command=load)
button_load.grid(row=1,column=2)

button_clean_data = Button(frame_ETL_buttons,text="Clean Data")
button_clean_data.grid(row=2,column=1)

message_box = Label(main_window,textvariable=msg_box_value,font=("Helvetica", 12))
message_box.grid(row=4)

main_window.mainloop()