#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Review(object):
    film_id = 0
    review_content = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, film_id, review_content):
        self.film_id = film_id
        self.review_content = review_content

def make_review(film_id, review_content):
    review = Review(film_id, review_content)
    return review