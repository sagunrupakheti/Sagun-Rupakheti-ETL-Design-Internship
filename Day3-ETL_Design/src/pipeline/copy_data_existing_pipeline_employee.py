import psycopg2
from dotenv import load_dotenv
load_dotenv()
import os
import json

try:
    def connect():
        return psycopg2.connect(
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
            database=os.getenv("database1")
        )

    # insert from json file
    def insert_table_raw_employee_json(filepath):
        # open the json file
        with open(filepath) as json_data:
            employee_list = json.load(json_data)
        # concatenate an SQL string
        sql = 'INSERT INTO raw_employee(employee_id, first_name, last_name, department_id, department_name, manager_employee_id, employee_role' \
              ', salary, hire_date, terminated_date, terminated_reason, dob, fte, location)VALUES'
        # Iteration
        for i, record_dict in enumerate(employee_list):
            values = []
            # dictionary items
            for columns, val in record_dict.items():
                # add to values array
                values += [str(val)]
            # join the list of values to the query
            sql += "(" + ', '.join(values) + "),\n"
        # remove the last comma and add a semicolon to the end
        sql = sql[:-2] + ";"
        curr = connect()
        cursor = curr.cursor()
        cursor.execute(sql)


    def extract_db_data(filename):
        source_conn = connect()
        dest_conn = connect()

        source_cursor = source_conn.cursor()
        dest_cursor = dest_conn.cursor()

        # delete - one at a time views constraint
        # truncate - data space reclaim gardaina
        with open("../../sql/extract_raw_data_timesheet.sql") as file:
            sql = "".join(file.readlines())
            source_cursor.execute(sql)
            result = source_cursor.fetchall()
            sql = 'INSERT INTO raw_employee_archive(employee_id, first_name, last_name, department_id, department_name, manager_employee_id, employee_role' \
              ', salary, hire_date, terminated_date, terminated_reason, dob, fte, location)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            for row in result:
                row = list(row)
                row.append(filename)
                row= tuple(row)
                dest_cursor.execute(sql, row)
                dest_conn.commit()


    if __name__ == "__main__":
    	insert_table_raw_employee_json('../../data/employee_2021_08_01.json')
        #extract_db_data("timesheet_2021_05_23-Sheet1.csv")


except Exception as e:
    print(e)
