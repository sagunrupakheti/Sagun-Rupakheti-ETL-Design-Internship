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
            database=os.getenv("database2")
        )

    # def create_table_for_extraction():
    #     create_query = 'CREATE TABLE data_extract_scenario(user_id VARCHAR(255),' \
    #                    'username VARCHAR(255),product_id VARCHAR(255),product_name VARCHAR(255),' \
    #                    'category_id VARCHAR(255),category_name VARCHAR(255),' \
    #                    'current_price VARCHAR(255),sold_price VARCHAR(255),sold_quantity VARCHAR(255),' \
    #                    'remaining_quantity VARCHAR(255),sales_date VARCHAR(255))'
    #     conn = connect()
    #     cursor = conn.cursor()
    #     cursor.execute(create_query)
    #     conn.commit()

    def extract_db_data():
        source_conn = connect()
        dest_conn = connect()

        source_cursor = source_conn.cursor()
        dest_cursor = dest_conn.cursor()

        #delete - one at a time views constraint
        #truncate - data space reclaim gardaina
        with open("../../sql/extract_raw_data_scenario.sql") as file:
            sql = "".join(file.readlines())
            source_cursor.execute(sql)
            result = source_cursor.fetchall()
            sql = 'INSERT INTO data_extract_scenario(user_id, username, product_id, product_name, category_id,category_name,' \
                  'current_price,sold_price,sold_quantity,remaining_quantity,sales_date)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            for row in result:
                dest_cursor.execute(sql,row)
                dest_conn.commit()


    if __name__ == "__main__":
        #create_table_for_extraction()
        extract_db_data()
except Exception as e:
    print(e)