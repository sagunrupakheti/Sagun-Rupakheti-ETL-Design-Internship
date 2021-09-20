from dotenv import load_dotenv
load_dotenv()
import os
import psycopg2

def connect():
    return psycopg2.connect(
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port"),
        database=os.getenv("database")
    )