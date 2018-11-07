#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
from Tkinter import *

import requests
from bs4 import BeautifulSoup

import gui
from db_connection import *
from movie import *
from review import*

if __name__ == '__main__':
    # code for testing below
    print("Program started")

    # conn = connect_to_database_and_get_connection()

    # create_table(conn)

    # #test get database version
    # db_verion = select_database_version(conn)
    # print(db_verion)

    # #test get data from movies
    # movies = select_all_movies(conn)
    # print(movies)

    # insert_movie(conn)

    # movie = make_movie("Film", 23, 24, 34)

    # print(movie.title + str(movie.filmweb_score))
    
    # close_database_connection(conn)

reload(sys)
sys.setdefaultencoding('utf-8')

movie_html_content = ""
movie = make_movie("", 0, 0, 0)
movie_site = "filmweb"
reviews_list_html = []
reviews_list_content = []
reviews_list = []
movie_main_url = ""

def ETL():
    extract()
    transform()
    load()

def clean_data():
    conn = connect_to_database_and_get_connection()
    delete_all_movies(conn)
    gui.print_msg_in_message_box("Data Erased")
    close_database_connection(conn)

def extract():
    global movie_main_url
    movie_main_url = get_filmweb_url_of(gui.input_movie_title.get())
    page = get_page(movie_main_url)

    soup = BeautifulSoup(page.content, 'html.parser')
    global movie_html_content
    movie_html_content = soup

    global reviews_list_html
    reviews_list_html = get_reviews_for_movie()

    gui.button_transform.config(state=NORMAL)
    gui.etl_bar_e.config(fg="red")
    gui.print_msg_in_message_box("Data Extracted")


def transform():
    soup = movie_html_content
    global movie
    moview = scrap_movie_from_filmweb(soup)

    scrap_reviews()
    global reviews_list
    for review_content in reviews_list_content:
        review = make_review(0, review_content)
        reviews_list.append(review)

    gui.button_load.config(state=NORMAL)
    gui.etl_bar_t.config(fg="red")
    gui.print_msg_in_message_box("Data Transformed")

def load():
    conn = connect_to_database_and_get_connection()
    insert_movie(conn, movie.title, movie.filmweb_score, movie.rotten_tomatoes_score, movie.imdb_score)
    close_database_connection(conn)

    gui.etl_bar_l.config(fg="red")
    gui.print_msg_in_message_box("Data Loaded")

def get_filmweb_url_of(movie_title):
    page = get_page(("https://www.filmweb.pl/search?q=" + movie_title))
    soup = BeautifulSoup(page.content, 'html.parser')
    movie_url_box = soup.find("a", attrs={"class": "filmPreview__link"})
    result = re.search('href=\"(.*)\"><h3 class', str(movie_url_box))
    return ("https://www.filmweb.pl" + result.group(1))


def scrap_movie_from_filmweb(soup):
    html = list(soup.children)[1]
    head = list(html.children)[0]
    body = list(html.children)[1]

    movie_title = list(head.children)[2].get_text().split("(",1)[0]

    result = re.search('\((.*)\)', list(head.children)[2].get_text())
    movie_prod_year = result.group(1)

    movie_score_box = soup.find("span", attrs={"itemprop": "ratingValue"})
    movie_score = int(float(movie_score_box.text.strip().replace(",","."))*10)

    movie = make_movie(movie_title, movie_score, 0, 0)
    return movie

def get_reviews_for_movie():
    page = get_page(movie_main_url + "/reviews")
    soup = BeautifulSoup(page.content, 'html.parser')

    reviews = soup.find("ul", {"class": "reviewsList"})
    return reviews.findAll("li", {"class": "hoverOpacity"})
    
def scrap_reviews():
    global reviews_list_content
    for review in reviews_list_html:
        a = review.find("a", {"class": "l"})
        result = re.search('href=\"(.*)\">', str(a))
        url = "https://www.filmweb.pl" + result.group(1)
        review_page = get_page(url)
        review_soup = BeautifulSoup(review_page.content, 'html.parser')
        review_content_html = review_soup.find("div", attrs={"itemprop": "reviewBody"}).text
        review_content = BeautifulSoup(review_content_html, "lxml").text
        reviews_list_content.append(review_content)
        
def get_page(url):
    page = requests.get(url)
    return page
