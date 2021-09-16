#Copy of Existing Pipeline 

**1. Query the table for extraction**    
~~~python 
SELECT 
employee_id, 
cost_center, 
punch_in_time, 
punch_out_time, 
punch_apply_date, 
hours_worked, 
paycode
FROM raw_timesheet;
~~~
* Start by querying the raw_timesheet table
* List out all the necessary attributes to export
***

**2. Create a table for storing the archive**
~~~python
CREATE TABLE raw_timesheet_archive(
employee_id VARCHAR(255),
cost_center VARCHAR(255),
punch_in_time VARCHAR(255),
punch_out_time VARCHAR(255),
punch_apply_date VARCHAR(255),
hours_worked VARCHAR(255),
paycode VARCHAR(255),
filename VARCHAR(255)
)
~~~
* A table raw_timesheet_archive created
* A new attribute filename added to track the file from which the data is loaded  
* The data from the previous query needs to be copied to this table

**3. Establish connection using environment**

* Create a .env file and add the values for user, password, host, port and database
* The values are written without spacing, comma and quotes

~~~python
import psycopg2
from dotenv import load_dotenv
load_dotenv()
import os
~~~
* import psycopg2 for connection
* import dotenv for environment variables
* import load_dotenv to load the environment file
* import os for interacting with the file

~~~python
    def connect():
        return psycopg2.connect(
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
            database=os.getenv("database2")
        )
~~~
* connect to psycopg2
* get environment using os and assign the variables

**4. Insert from the query to the table

~~~python
 def extract_db_data(filename):
        source_conn = connect()
        dest_conn = connect()

        source_cursor = source_conn.cursor()
        dest_cursor = dest_conn.cursor()
~~~
* Establish the source connection and destination connection
* Create cursors for connections

~~~python
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
~~~
* open the file containing the query
* fetch all the rows
* convert the tuple into list as tuples cannot be ammended
* append the file name for the filename column
* again convert the list into tuple for insertion  
* insert the rows into the created table

**5. Call the functions** 

~~~python 
 if __name__ == "__main__":
    	extract_timesheet_data_insert("../../data/timesheet_2021_05_23-Sheet1.csv")
        extract_db_data("timesheet_2021_05_23-Sheet1.csv")
    	extract_timesheet_data_insert("../../data/timesheet_2021_06_23-Sheet1.csv")
        extract_db_data("timesheet_2021_06_23-Sheet1.csv")
    	extract_timesheet_data_insert("../../data/timesheet_2021_07_24-Sheet1.csv")
        extract_db_data("timesheet_2021_07_24-Sheet1.csv") if __name__ == "__main__":
    	extract_timesheet_data_insert("../../data/timesheet_2021_05_23-Sheet1.csv")
        extract_db_data("timesheet_2021_05_23-Sheet1.csv")
    	extract_timesheet_data_insert("../../data/timesheet_2021_06_23-Sheet1.csv")
        extract_db_data("timesheet_2021_06_23-Sheet1.csv")
    	extract_timesheet_data_insert("../../data/timesheet_2021_07_24-Sheet1.csv")
        extract_db_data("timesheet_2021_07_24-Sheet1.csv")
~~~
* Call the extraction function immediately after insertion
* This created an archive of the inserted data 
* The data is stored in the archive table even if it gets removed from the raw data table
