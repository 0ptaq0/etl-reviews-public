#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Review(object):
    movie_id = 0
    rev_title = ""
    content = ""
    author = ""
    review_rating = 0
    pub_date = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, movie_id, rev_title,  content, author, review_rating, pub_date):
        self.movie_id = movie_id
        self.rev_title = rev_title
        self.content = content
        self.author = author
        self.review_rating = review_rating
        self.pub_date = pub_date

def make_review(movie_id, rev_title, content, author, review_rating, pub_date):
    review = Review(movie_id, rev_title, content, author, review_rating, pub_date)
    return review