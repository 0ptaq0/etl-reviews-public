#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import unicodecsv as csv
from ttk import *
from Tkinter import *

import requests
from bs4 import BeautifulSoup

import gui
from db_connection import *
from movie import *
from review import *


reload(sys)
sys.setdefaultencoding('utf-8')

movie_html_content = ""
movie = make_movie("", 0)
movie_site = "filmweb"
reviews_list_html = []
reviews_list_content = []
reviews_list = []
movie_main_url = ""
reviews_list_dict = []

def ETL():
    extract()
    transform()
    load()

def clean_data():
    conn = connect_to_database_and_get_connection()
    number_of_erased_movies_from_db = delete_all_movies(conn)
    number_of_erased_movie_reviews_from_db = delete_all_reviews(conn)
    gui.print_msg_in_message_box("Data Erased. \n " + number_of_erased_movies_from_db + " movie score records were erased. \n " 
        + number_of_erased_movie_reviews_from_db + " movie review records were erased.")
    close_database_connection(conn)

def extract():
    if gui.input_movie_title.get() == "":
        gui.print_msg_in_message_box("Please type a movie title in the input field above.")
        return

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
    gui.print_msg_in_message_box("Data Extracted. \n" + str(len(reviews_list_html)) + " reviews found. ")


def transform():
    soup = movie_html_content
    global movie
    movie = scrap_movie_from_filmweb(soup)

    scrap_reviews()

    gui.button_load.config(state=NORMAL)
    gui.etl_bar_t.config(fg="red")
    gui.print_msg_in_message_box("Data Transformed. \n " + movie.title + " - users rating: " + str(movie.filmweb_score)[:-1] + "." + str(movie.filmweb_score)[:1])

def load():
    conn = connect_to_database_and_get_connection()
    print(movie.title)
    movie_id = insert_movie(conn, movie)
    for review in reviews_list:
        insert_review(conn, review, movie_id)
    close_database_connection(conn)

    gui.etl_bar_l.config(fg="red")
    gui.print_msg_in_message_box("Data Loaded. \n " + str(len(reviews_list)) + " new movie review(s) uploaded into database.")
    del reviews_list[:]

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

    movie = make_movie(movie_title, movie_score)
    return movie

def get_reviews_for_movie():
    page = get_page(movie_main_url + "/reviews")
    soup = BeautifulSoup(page.content, 'html.parser')

    reviews = soup.find("div", {"class": "allReviews"})
    all_reviews = ""
    if reviews != None:
        top_reviews = reviews.findAll("a", {"class": "l"})
        rest_of_the_reviews = reviews.findAll("a", {"class": "normal"})
        all_reviews = top_reviews
        all_reviews.extend(rest_of_the_reviews)
    return all_reviews
    
def scrap_reviews():
    global reviews_list       
    for review in reviews_list_html:
        result = re.search('href=\"(.*)\">', str(review))
        url = "https://www.filmweb.pl" + result.group(1)
        review_page = get_page(url)
        review_soup = BeautifulSoup(review_page.content, 'html.parser')
        review_content_html = review_soup.find("div", attrs={"itemprop": "reviewBody"}).text
        review_content = BeautifulSoup(review_content_html, "lxml").text
        index = review_content.index('waitingModule')
        review_content = review_content[:index]

        rev_title = review_soup.find("h2", attrs={"itemprop": "name"}).text

        author = review_soup.find("div", attrs={"itemprop": "author"}).text

        review_rating = review_soup.find("span", {"class": "reviewRatingPercent"}).text[:-1]

        review = make_review(0, rev_title, review_content, author, review_rating)
        reviews_list.append(review)
        
def get_page(url):
    page = requests.get(url)
    return page

def extract_db_to_csv():
    conn = connect_to_database_and_get_connection()
    dict_with_data = select_all_reviews(conn)
    close_database_connection(conn)
    keys = dict_with_data[0].keys()
    if not os.path.exists('temp'):
        os.makedirs('temp')
    with open('temp/movie_reviews_output.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dict_with_data)
    gui.print_msg_in_message_box("Data saved in CSV.")

class Application():
    def __init__(self,master):
        self.master = master
        self.tree = Treeview(self.master, selectmode='browse')
        self.tree.place(x=0, y=0)
        self.vsb = Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        self.vsb.grid(row=1, column=1, sticky='ns')

        self.searchfield = Treeview(self.master)
        self.searchfield.grid(row=0, column=0, sticky='n')
        self.search_var = StringVar()
        self.entry = Entry(self.searchfield, textvariable=self.search_var, width=45)
        self.entry.grid(row=0, column=0)

        self.searchbtn = Button(self.searchfield, text='Search', command=self.search) 
        self.searchbtn.grid(row=0, column=1)
        # self.treeFrame = Listbox(self.searchfield, width=45, height=45)
        # self.treeFrame.grid(row=1, column=0, padx=10, pady=3)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.tree.grid(row=1,column=0,sticky='nsew')
        self.tree["columns"] = ("id", "movie", "rev_title", "author", "rev_rating")
        self.tree['show'] = 'headings'
        self.tree.column("id",  anchor='c', stretch=YES)
        self.tree.column("movie", anchor='c', stretch=YES)
        self.tree.column("rev_title",  anchor='c', stretch=YES)
        self.tree.column("author",  anchor='c', stretch=YES)
        self.tree.column("rev_rating", anchor='c', stretch=YES)

        self.tree.heading("id", text="ID")
        self.tree.heading("movie", text="Movie")
        self.tree.heading("rev_title", text="Review title")
        self.tree.heading("author", text="Author")
        self.tree.heading("rev_rating", text="Review rating")

        self.tree.bind('<ButtonRelease-1>', self.selectItem)
    
    def create_data_table(self, search_for):
        conn = connect_to_database_and_get_connection()
        global reviews_list_dict
        reviews_list_dict = select_reviews_fiter_by_movie(conn, search_for)
        close_database_connection(conn)
        counter=0
        for i in self.tree.get_children():
            self.tree.delete(i)
        for review_dict in reviews_list_dict:
            counter+=1
            self.tree.insert("",'end',text="ID_" + str(counter),values=(counter, review_dict["title"], 
                review_dict["rev_title"], review_dict["author"], 
                review_dict["review_rating"]))
    
    def search(self):
        search_for = self.search_var.get()
        self.create_data_table(search_for)

    def selectItem(self, a):
        curItem = self.tree.focus()
        id = (self.tree.item(curItem)["text"])[3:]

        review = reviews_list_dict[(int(id)-1)]
        review_window = Tk()
        review_window.title("Review")
        review_window.minsize(width=440, height=220)

        label_review_title = Label(review_window,text=review["rev_title"], font=("Helvetica", 24))
        label_review_title.pack()

        label_review_author = Label(review_window,text="Author: " + review["author"], font=("Helvetica", 12))
        label_review_author.pack()

        label_review_movie = Label(review_window,text="Moview: " + review["title"], font=("Helvetica", 12))
        label_review_movie.pack()

        str_rev_rating = "This review was helpful for " + str(review["review_rating"]) + "% of users."
        label_review_rev_reting = Label(review_window,text=str_rev_rating, font=("Helvetica", 10))
        label_review_rev_reting.pack()

        label_review_content = Label(review_window,text=review["content"], font=("Helvetica", 12), wraplength=1200, justify=LEFT)
        label_review_content.pack()

if __name__ == '__main__':
    # code for testing below
    print("main")
    
    # conn = connect_to_database_and_get_connection()

    # create_tables(conn)

    # #test get database version
    # db_verion = select_database_version(conn)
    # print(db_verion)

    # #test get data from movies
    # movies = select_all_movies(conn)
    # print(movies)

    # dict_res = select_all_reviews(conn)
    # print dict_res
    # print(dict_res[0].get("author"))

    # movie = make_movie("AAA", 33)
    # review = make_review(2, "tes", "sdfsdfsdfsdfsdg", "Ja", 43)

    # print(insert_review(conn, review))

    # print(insert_movie(conn, movie))

    # print(movie.title + str(movie.filmweb_score))
    
    # close_database_connection(conn)
    # root = Tk()
    # Application(root)
    # root.mainloop()    
 
