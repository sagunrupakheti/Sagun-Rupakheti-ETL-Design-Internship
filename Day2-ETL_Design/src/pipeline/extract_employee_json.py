#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import connect, Error

# import Python's built-in JSON library
import json
import psycopg2
# import the JSON library from psycopg2.extras
from psycopg2.extras import Json

# import psycopg2's 'json' using an alias
from psycopg2.extras import json as psycop_json

# import Python's 'sys' library
import sys

# accept command line arguments for the Postgres table name
try:
    connection = psycopg2.connect(
        host="localhost",
        database="ETLweek1",
        user="postgres",
        password="sagun",
        port=5432
    )
    cursor = connection.cursor()

    if len(sys.argv) > 1:
        table_name = '_'.join(sys.argv[1:])
    else:
        # ..otherwise revert to a default table name
        table_name = "raw_employee"

    print ("\ntable name for JSON data:", table_name)

    # use Python's open() function to load the JSON data
    with open('../../data/employee_2021_08_01.json') as json_data:

        # use load() rather than loads() for JSON files
        record_list = json.load(json_data)

    print ("\nrecords:", record_list)
    print ("\nJSON records object type:", type(record_list)) # should return "<class 'list'>"

    # concatenate an SQL string
    sql_string = 'INSERT INTO {} '.format( table_name )

    # if record list then get column names from first key
    if type(record_list) == list:
        first_record = record_list[0]

        columns = list(first_record.keys())
        print ("\ncolumn names:", columns)

    # if just one dict obj or nested JSON dict
    else:
        print ("Needs to be an array of JSON objects")
        sys.exit()

    # enclose the column names within parenthesis
    sql_string += "(" + ', '.join(columns) + ")\nVALUES "

    # enumerate over the record
    for i, record_dict in enumerate(record_list):

        # iterate over the values of each record dict object
        values = []
        for col_names, val in record_dict.items():

            # Postgres strings must be enclosed with single quotes
            if type(val) == str:
                # escape apostrophies with two single quotations
                val = val.replace("'", "''")
                val = "'" + val + "'"

            values += [ str(val) ]

        # join the list of values and enclose record in parenthesis
        sql_string += "(" + ', '.join(values) + "),\n"

    # remove the last comma and end statement with a semicolon
    sql_string = sql_string[:-2] + ";"

    print ("\nSQL string:")
    print (sql_string)
    cursor.execute(sql_string)
    connection.commit()
    cursor.close()
    connection.close()
except Exception as e:
    print(e)