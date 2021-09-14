import psycopg2
try:
    connection = psycopg2.connect(
        host="localhost",
        database="ETLweek1",
        user="postgres",
        password="sagun",
        port=5432
    )
    cursor = connection.cursor()

    def create_table_raw():
        create_query = "CREATE TABLE raw_timesheet(employee_id VARCHAR(255),cost_center VARCHAR(255),punch_in_time VARCHAR(255),punch_out_time VARCHAR(255),punch_apply_date VARCHAR(255),hours_worked VARCHAR(255),paycode VARCHAR(255))"
        cursor.execute(create_query)

    def extract_timesheet_data_view(filePath):
        with open(filePath,'r') as file:
            i=0
            for line in file:
                if i==0:
                    i+=1
                    continue
                print(line)

    def extract_timesheet_data_insert(filePath):
        with open(filePath,'r') as file:
            i=0
            sql = "DELETE FROM raw_timesheet;"
            cursor.execute(sql)
            for line in file:
                if i==0:
                    i+=1
                    continue
                row = line.strip().split(",")
                insert_query = "INSERT INTO raw_timesheet(employee_id,cost_center,punch_in_time,punch_out_time,punch_apply_date,hours_worked,paycode)VALUES(%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(insert_query,row)

    if __name__ == "__main__":
    	extract_timesheet_data_insert("../../data/timesheet_2021_05_23-Sheet1.csv")
    	extract_timesheet_data_insert("../../data/timesheet_2021_06_23-Sheet1.csv")
    	extract_timesheet_data_insert("../../data/timesheet_2021_07_24-Sheet1.csv")

    connection.commit()
    cursor.close()
    connection.close()
except Exception as e:
    print(e)
