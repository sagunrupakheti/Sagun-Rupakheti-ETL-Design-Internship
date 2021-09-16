#imports
import json
from lxml import etree
import psycopg2
from psycopg2.extras import execute_values
import datetime
from dotenv import load_dotenv
load_dotenv()
import os

try:
    #establish connection
    connection = psycopg2.connect(
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port"),
        database=os.getenv("database1")
    )
    cursor = connection.cursor()

    #create the table
    def create_table_raw_employee():
        create_query = 'CREATE TABLE raw_employee(' \
                       'employee_id VARCHAR(255), first_name VARCHAR(255), last_name VARCHAR(255), department_id VARCHAR(255), ' \
                       'department_name VARCHAR(255), manager_employee_id VARCHAR(255), employee_role VARCHAR(255), salary VARCHAR(255), ' \
                       'hire_date VARCHAR(255), terminated_date VARCHAR(255),' \
                       ' terminated_reason VARCHAR(255), dob VARCHAR(255), fte VARCHAR(255), location VARCHAR(255))'
        cursor.execute(create_query)

    #insert from json file
    def insert_table_raw_employee_json():
        #open the json file
        with open('../../data/employee_2021_08_01.json') as json_data:
            employee_list = json.load(json_data)
        # concatenate an SQL string
        sql = 'INSERT INTO raw_employee(employee_id, first_name, last_name, department_id, department_name, manager_employee_id, employee_role' \
                     ', salary, hire_date, terminated_date, terminated_reason, dob, fte, location)VALUES'
        # Iteration
        for i, record_dict in enumerate(employee_list):
            values = []
            #dictionary items
            for columns, val in record_dict.items():
                #add to values array
                values += [ str(val) ]
            # join the list of values to the query
            sql += "(" + ', '.join(values) + "),\n"
        # remove the last comma and add a semicolon to the end
        sql = sql[:-2] + ";"
        cursor.execute(sql)


    def import_xml(filename, insert_command, batch=[], batch_size=30):
        count = 0
        try:
            for event, element in etree.iterparse(filename, events=('end',), tag='row'):
                count += 1
                row = [element.get(n) for n in (
                'employee_id', 'first_name', 'last_name', 'department_id', 'department_name', 'manager_employee_id',
                'employee_role', 'salary', 'hire_date', 'terminated_date', 'terminated_reason', 'dob', 'fte',
                'location')]
                batch.append(row)
                #delete previous record if exists
                if element.getprevious() is not None:
                    del (element.getparent()[0])
                # Save batch to DB
                if count % batch_size == 0:
                    execute_values(cursor, insert_command, batch)
                    batch = []
            # Save the rest
            if len(batch):
                execute_values(cursor, insert_command, batch)
        except Exception as e:
            print(e)

    def insert_table_raw_employee_xml(file):
        filename = file
        start_date = datetime.datetime.now()
        insert_command = "INSERT INTO raw_employee (employee_id, first_name, last_name, department_id, department_name, manager_employee_id, employee_role, salary, hire_date, terminated_date, terminated_reason, dob, fte, location)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        import_xml(filename, connection, insert_command)


    if __name__ == "__main__":
        insert_table_raw_employee_json('../../data/employee_2021_08_01.xml')
        #insert_table_raw_employee_xml('../../data/employee_2021_08_01.xml')

    connection.commit()
    cursor.close()
    connection.close()
except Exception as e:
    print(e)