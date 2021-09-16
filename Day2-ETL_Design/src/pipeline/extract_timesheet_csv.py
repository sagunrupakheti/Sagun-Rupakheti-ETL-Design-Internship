#imports
import psycopg2
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

    #create all columns with varchar datatype to minimize risk of unformatted or inconsistent data
    def create_table_raw():
        create_query = "CREATE TABLE raw_timesheet(employee_id VARCHAR(255),cost_center VARCHAR(255),punch_in_time VARCHAR(255),punch_out_time VARCHAR(255),punch_apply_date VARCHAR(255),hours_worked VARCHAR(255),paycode VARCHAR(255))"
        cursor.execute(create_query)

    #to view the data in the file
    def extract_timesheet_data_view(filePath):
        with open(filePath,'r') as file:
            i=0
            for line in file:
                if i==0:
                    i+=1
                    continue
                print(line)

    #extract the data and insert it into the table
    def extract_timesheet_data_insert(filePath):
        with open(filePath,'r') as file:
            i=0
            #delete if any data exists in the table
            sql = "DELETE FROM raw_timesheet;"
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

    if __name__ == "__main__":
        #create_table_raw()
    	extract_timesheet_data_insert("../../data/timesheet_2021_05_23-Sheet1.csv")
    	extract_timesheet_data_insert("../../data/timesheet_2021_06_23-Sheet1.csv")
    	extract_timesheet_data_insert("../../data/timesheet_2021_07_24-Sheet1.csv")

    connection.commit()
    cursor.close()
    connection.close()
except Exception as e:
    print(e)
