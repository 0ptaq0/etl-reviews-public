#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Review(object):
    film_id = 0
    rev_title = ""
    content = ""
    author = ""
    review_rating = 0

    # The class "constructor" - It's actually an initializer 
    def __init__(self, film_id, rev_title,  content, author, review_rating):
        self.film_id = film_id
        self.rev_title = rev_title
        self.content = content
        self.author = author
        self.review_rating = review_rating

def make_review(film_id, rev_title, content, author, review_rating):
    review = Review(film_id, rev_title, content, author, review_rating)
    return review