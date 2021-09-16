import psycopg2
from dotenv import load_dotenv
load_dotenv()
import os

try:
    def connect():
        return psycopg2.connect(
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
            database=os.getenv("database1")
        )

    def extract_employee_data():
        source_conn = connect()
        dest_conn = connect()

        source_cursor = source_conn.cursor()
        dest_cursor = dest_conn.cursor()

        #delete - one at a time views constraint
        #truncate - data space reclaim gardaina
        with open("../../sql/extract_raw_data_from_db.sql") as file:
            sql = "".join(file.readlines())
            source_cursor.execute(sql)
            result = source_cursor.fetchall()
            sql = 'INSERT INTO raw_employee(employee_id, first_name, last_name, department_id, department_name,' \
                  'salary)VALUES(%s,%s,%s,%s,%s,%s)'
            for row in result:
                dest_cursor.execute(sql,row)
                dest_conn.commit()


except Exception as e:
    print(e)