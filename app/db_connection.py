#!/usr/bin/python
# -*- coding: UTF-8 -*-

from configparser import ConfigParser

import psycopg2
import os
import psycopg2.extras

def config(filename, section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db

def connect_to_database_and_get_connection():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        if os.path.isfile('database.ini'):
            params = config('database.ini')
        else:
            params = config('app\database.ini')
 
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn

def close_database_connection(conn):
    if conn is not None:
            conn.close()
            print('Connection to the PostgreSQL database closed')

def create_tables(conn):
    try:
        cur = conn.cursor()
        cur.execute('CREATE TABLE movies (id serial primary key, title VARCHAR(40) not null UNIQUE, prod_year VARCHAR(6), filmweb_score integer);')
        cur.execute('CREATE TABLE reviews (id serial primary key, movie_id serial, rev_title VARCHAR(100) not null UNIQUE, content text, author varchar(40), review_rating integer);')
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_movie(conn, movie):
    try:
        cur = conn.cursor()
        sql_update = "UPDATE SET filmweb_score = %s"
        sql = "INSERT INTO movies (title, prod_year, filmweb_score) VALUES (%s, %s, %s) ON CONFLICT (title) DO " + sql_update
        cur.execute(sql, (movie.title, movie.prod_year, movie.filmweb_score, movie.filmweb_score))
        conn.commit()
        cur.execute('SELECT LASTVAL()')
        id = cur.fetchone()[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return id

def insert_review(conn, review, movie_id):
    try:
        cur = conn.cursor()
        sql_update = "UPDATE SET content = %s, author = %s, review_rating = %s"
        sql = "INSERT INTO reviews (movie_id, rev_title, content, author, review_rating) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (rev_title) DO " + sql_update
        cur.execute(sql, (movie_id, review.rev_title, review.content, review.author, review.review_rating, review.content, review.author, review.review_rating))
        conn.commit()
        cur.execute('SELECT LASTVAL()')
        id = cur.fetchone()[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return id

def select_database_version(conn):
    cur = conn.cursor()
    cur.execute('SELECT version()')
    result = cur.fetchone()
    cur.close()
    return result

def select_all_movies(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM movies")
        result = cur.fetchall()
        cur.close()
        print(result[1])
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return result

def select_all_reviews(conn):
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM reviews LEFT JOIN movies ON reviews.movie_id = movies.id")
        result = cur.fetchall()
        cur.close()
        dict_result = []
        for row in result:
            dict_result.append(dict(row))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return dict_result

def select_reviews_fiter_by_movie(conn, string):
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT * FROM reviews LEFT JOIN movies ON reviews.movie_id = movies.id WHERE movies.title || movies.prod_year ILIKE '%" + string + "%'"
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        dict_result = []
        for row in result:
            dict_result.append(dict(row))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return dict_result

def delete_all_movies(conn):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM movies")
        number_of_erased_movies_from_db = str(cur.rowcount)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return number_of_erased_movies_from_db


def delete_all_reviews(conn):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM reviews")
    
        number_of_erased_movie_reviews_from_db = str(cur.rowcount)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return number_of_erased_movie_reviews_from_db