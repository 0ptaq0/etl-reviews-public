#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Movie(object):
    title = ""
    filmweb_score = 0
    prod_year = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, title, prod_year, filmweb_score):
        self.title = title
        self.filmweb_score = filmweb_score
        self.prod_year = prod_year

def make_movie(title, prod_year, filmweb_score):
    movie = Movie(title, prod_year, filmweb_score)
    return movie