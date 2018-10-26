#!/usr/bin/python
# -*- coding: UTF-8 -*-

import psycopg2
from configparser import ConfigParser
 
def config(filename='database.ini', section='postgresql'):
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
        params = config()
 
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn

def close_database_connection(conn):
    if conn is not None:
            conn.close()
            print('Connection to the PostgreSQL database closed')

def select_database_version(conn):
    cur = conn.cursor()
    cur.execute('SELECT version()')
    result = cur.fetchone()
    cur.close()
    return result

def select_all_films(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies")
    result = cur.fetchall()
    cur.close()
    return result


    
