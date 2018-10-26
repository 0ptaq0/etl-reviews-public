#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
import requests
from bs4 import BeautifulSoup
import re
import gui
from db_connection import *

if __name__ == '__main__':
    conn = connect_to_database_and_get_connection()
    #test get database version
    db_verion = select_database_version(conn)
    print(db_verion)

    #test get data from movies
    movies = select_all_movies(conn)
    print(movies)

    close_database_connection(conn)

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
    data_scrapping(get_filmweb_url_of(gui.input_movie_title.get()))
    gui.button_transform.config(state=NORMAL)
    gui.etl_bar_e.config(fg="red")
    gui.print_msg_in_message_box("Data Extracted")

def transform():
    gui.button_load.config(state=NORMAL)
    gui.etl_bar_t.config(fg="red")
    gui.print_msg_in_message_box("Data Transformed")

def load():
    gui.etl_bar_l.config(fg="red")
    gui.print_msg_in_message_box("Data Loaded")

def get_filmweb_url_of(movie_title):
    page = get_page(("https://www.filmweb.pl/search?q=" + movie_title))
    soup = BeautifulSoup(page.content, 'html.parser')
    movie_url_box = soup.find("a", attrs={"class": "filmPreview__link"})
    result = re.search('href=\"(.*)\"><h3 class', str(movie_url_box))
    return ("https://www.filmweb.pl" + result.group(1))


def data_scrapping(film_url):
    page = get_page(film_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    html = list(soup.children)[1]
    head = list(html.children)[0]
    body = list(html.children)[1]

    movie_title = list(head.children)[2].get_text().split("(",1)[0]
    print(movie_title)

    result = re.search('\((.*)\)', list(head.children)[2].get_text())
    movie_prod_year = result.group(1)
    print(movie_prod_year)

    movie_score_box = soup.find("span", attrs={"itemprop": "ratingValue"})
    movie_score = movie_score_box.text.strip()
    print(movie_score)
    

def get_page(url):
    page = requests.get(url)
    return page