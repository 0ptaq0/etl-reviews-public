#!/usr/bin/python
# -*- coding: UTF-8 -*-

from configparser import ConfigParser

import psycopg2
import os

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
        cur.execute('CREATE TABLE movies (id serial primary key, title VARCHAR(40) not null, filmweb_score integer);')
        cur.execute('CREATE TABLE reviews (id serial primary key, movie_id serial, rev_title VARCHAR(100) not null, content text, author varchar(40), review_rating integer);')
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_movie(conn, movie):
    try:
        cur = conn.cursor()
        sql = "INSERT INTO movies (title, filmweb_score) VALUES (%s, %s)"
        cur.execute(sql, (movie.title, movie.filmweb_score))
        conn.commit()
        print str(cur.rowcount) + " new movie score(s) was uploaded into database"
        cur.execute('SELECT LASTVAL()')
        id = cur.fetchone()[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return id

def insert_review(conn, review, movie_id):
    try:
        cur = conn.cursor()
        sql = "INSERT INTO reviews (movie_id, rev_title, content, author, review_rating) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql, (movie_id, review.rev_title, review.content, review.author, review.review_rating))
        conn.commit()
        print str(cur.rowcount) + " new review score(s) was uploaded into database"
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
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies")
    result = cur.fetchall()
    cur.close()
    return result

def delete_all_movies(conn):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM movies")
    
        print "Operation DELETE erased " + str(cur.rowcount) + " record(s)"
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)