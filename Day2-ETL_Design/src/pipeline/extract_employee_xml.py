from lxml import etree
import psycopg2
from psycopg2.extras import execute_values
import datetime
import os
import psutil


def import_xml(filename, connect, insert_command, batch = [], batch_size = 100):
    print('asd')
    count = 0
    cursor = connect.cursor()
    process = psutil.Process(os.getpid())
    try:
        for event, element in etree.iterparse(filename, events=('end',), tag='row'):
            print('asd')
            count += 1
            row = [element.get(n) for n in ('employee_id', 'first_name', 'last_name', 'department_id', 'department_name', 'manager_employee_id', 'employee_role', 'salary', 'hire_date', 'terminated_date', 'terminated_reason', 'dob', 'fte', 'location')]
            batch.append(row)
            # Free memory
            element.clear()
            if element.getprevious() is not None:
                del(element.getparent()[0])
            # Save batch to DB
            if count % batch_size == 0:
                execute_values(cursor, insert_command, batch)
                batch = []
        # Save the rest
        if len(batch):
            execute_values(cursor, insert_command, batch)
    except Exception as e:
        print(e)

def import_dump():
    filename = '../../data/employee_2021_08_01.xml'
    start_date = datetime.datetime.now()
    print ("Import data from {}".format(filename))
    connect = psycopg2.connect(
        host="localhost",
        database="ETLweek1",
        user="postgres",
        password="sagun",
        port=5432
    )
    connect.autocommit = True
    cursor = connect.cursor()

    insert_command = "INSERT INTO raw_employee (employee_id, first_name, last_name, department_id, department_name, manager_employee_id, employee_role, salary, hire_date, terminated_date, terminated_reason, dob, fte, location)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    import_xml(filename, connect, insert_command)
    cursor.execute(insert_command,import_xml)
    connect.close()

    end_date = datetime.datetime.now()
    seconds = (end_date - start_date).total_seconds()
    print ("\nExecuted in {}s".format(seconds))

if __name__ == '__main__':
    import_dump()