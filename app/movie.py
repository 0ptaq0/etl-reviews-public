#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Movie(object):
    title = ""
    filmweb_score = 0
    rotten_tomatoes_score = 0
    imdb_score = 0

    # The class "constructor" - It's actually an initializer 
    def __init__(self, title, filmweb_score, rotten_tomatoes_score, imdb_score):
        self.title = title
        self.filmweb_score = filmweb_score
        self.rotten_tomatoes_score = rotten_tomatoes_score
        self.imdb_score = imdb_score

def make_movie(title, filmweb_score, rotten_tomatoes_score, imdb_score):
    movie = Movie(title, filmweb_score, rotten_tomatoes_score, imdb_score)
    return movie