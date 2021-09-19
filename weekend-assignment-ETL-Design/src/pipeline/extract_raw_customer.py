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
            database=os.getenv("database")
        )

    def extract_customer_data(filePath):
        connection = connect()
        cursor = connection.cursor()

        with open(filePath, 'r') as file:
            i = 0
            # delete if any data exists in the table
            sql = "DELETE FROM raw_customer;"
            cursor.execute(sql)
            for data in file:
                if i == 0:
                    i += 1
                    continue
                # removes any new lines and splits the data by a comma
                row = data.strip().split(",")
                # %s to pass the rows
                insert_query = "INSERT INTO raw_customer(customer_id,user_name,first_name,last_name,country,town,active)" \
                               "VALUES(%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(insert_query, row)
                connection.commit()

    if __name__ == "__main__":
        extract_customer_data('../../data/customer_dump - Sheet1.csv')

except Exception as e:
    print(e)