#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
import requests
from bs4 import BeautifulSoup
import re
import etl
from etl import *

reload(sys)
sys.setdefaultencoding('utf-8')

def print_msg_in_message_box(msg):
    msg_box_value.set("Info: " + msg)

main_window = Tk()
application = Application(main_window)
main_window.title("ETL Movie Reviews")

msg_box_value = StringVar(main_window,value="Info: ")

frame_ETL_bar = Frame(main_window)
frame_ETL_bar.grid(row=2)

etl_bar_e = Label(frame_ETL_bar,text="E", font=("Helvetica", 24))
etl_bar_e.grid(row=2,column=0)

etl_bar_t = Label(frame_ETL_bar,text="T", font=("Helvetica", 24))
etl_bar_t.grid(row=2,column=1)

etl_bar_l = Label(frame_ETL_bar,text="L", font=("Helvetica", 24))
etl_bar_l.grid(row=2,column=2)

# title_bar = Label(main_window,text="movie Reviews", font=("Helvetica", 12))
# title_bar.grid(row=1)

input_movie_title = Entry(main_window)
input_movie_title.grid(row=3)

frame_ETL_buttons = Frame(main_window)
frame_ETL_buttons.grid(row=4)

button_ETL = Button(frame_ETL_buttons,text="ETL",command=etl.ETL)
button_ETL.grid(row=0,column=1)

button_extract = Button(frame_ETL_buttons,text="Extract",command=etl.extract)
button_extract.grid(row=1,column=0, padx=10, pady=5)

button_transform = Button(frame_ETL_buttons,text="Transform",state=DISABLED,command=etl.transform)
button_transform.grid(row=1,column=1, padx=10, pady=5)

button_load = Button(frame_ETL_buttons,text="Load",state=DISABLED,command=etl.load)
button_load.grid(row=1,column=2, padx=10, pady=5)

button_clean_data = Button(frame_ETL_buttons,text="Clean Data",command=etl.clean_data)
button_clean_data.grid(row=2,column=1)

message_box = Label(main_window,textvariable=msg_box_value,font=("Helvetica", 12))
message_box.grid(row=5,pady=10)

i = 0
while i < 10:
    main_window.rowconfigure(i, weight=2)
    main_window.columnconfigure(i,weight=2)
    i += 1

main_window.mainloop()