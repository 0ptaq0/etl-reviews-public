#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Review(object):
    movie_id = 0
    rev_title = ""
    content = ""
    author = ""
    review_rating = 0

    # The class "constructor" - It's actually an initializer 
    def __init__(self, movie_id, rev_title,  content, author, review_rating):
        self.movie_id = movie_id
        self.rev_title = rev_title
        self.content = content
        self.author = author
        self.review_rating = review_rating

def make_review(movie_id, rev_title, content, author, review_rating):
    review = Review(movie_id, rev_title, content, author, review_rating)
    return review