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

def create_table(conn):
    try:
        cur = conn.cursor()
        cur.execute('CREATE TABLE movies (id serial primary key, title VARCHAR(40) not null, filmweb_score integer, rotten_tomatoes_score integer, imdb_score integer);')
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_movie(conn, title, filmweb_score, rotten_tomatoes_score, imdb_score):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO movies (title, filmweb_score, rotten_tomatoes_score, imdb_score) VALUES ('" + title + "', " + str(filmweb_score) + ", " + str(rotten_tomatoes_score) + ", " + str(imdb_score) + ")")
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

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
