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

    #extract the data and insert it into the table
    def extract_timesheet_data_insert(filePath):
        with open(filePath,'r') as file:
            i=0
            #delete if any data exists in the table
            sql = "DELETE FROM raw_timesheet;"
            conn = connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            for data in file:
                if i==0:
                    i+=1
                    continue
                #removes any new lines and splits the data by a comma
                row = data.strip().split(",")
                #%s to pass the rows
                insert_query = "INSERT INTO raw_timesheet(employee_id,cost_center,punch_in_time,punch_out_time,punch_apply_date,hours_worked,paycode)VALUES(%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(insert_query,row)


    def extract_db_data(filename):
        source_conn = connect()
        dest_conn = connect()

        source_cursor = source_conn.cursor()
        dest_cursor = dest_conn.cursor()

        with open(filename) as file:
            sql = "".join(file.readlines())
            source_cursor.execute(sql)
            result = source_cursor.fetchall()
            sql = 'INSERT INTO raw_timesheet_archive(employee_id,cost_center,punch_in_time,punch_out_time,punch_apply_date,' \
                  'hours_worked,paycode,filename)VALUES(%s,%s,%s,%s,%s,%s,%s,%s);'
            for row in result:
                row = list(row)
                row.append(filename)
                row= tuple(row)
                dest_cursor.execute(sql, row)
                dest_conn.commit()


    if __name__ == "__main__":
    	extract_timesheet_data_insert("../../data/timesheet_2021_05_23-Sheet1.csv")
        extract_db_data("timesheet_2021_05_23-Sheet1.csv")
    	extract_timesheet_data_insert("../../data/timesheet_2021_06_23-Sheet1.csv")
        extract_db_data("timesheet_2021_06_23-Sheet1.csv")
    	extract_timesheet_data_insert("../../data/timesheet_2021_07_24-Sheet1.csv")
        extract_db_data("timesheet_2021_07_24-Sheet1.csv")

except Exception as e:
    print(e)
