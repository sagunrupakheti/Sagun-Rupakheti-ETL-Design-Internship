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

    def extract_sales_data(filePath):
        connection = connect()
        cursor = connection.cursor()

        with open(filePath, 'r') as file:
            i = 0
            # delete if any data exists in the table
            sql = "DELETE FROM raw_sales;"
            cursor.execute(sql)
            for data in file:
                if i == 0:
                    i += 1
                    continue
                # removes any new lines and splits the data by a comma
                row = data.strip().split(",")
                # %s to pass the rows
                insert_query = "INSERT INTO raw_sales( id,transaction_id,bill_no,bill_date,bill_location,customer_id,product_id,qty,uom," \
                               "price,gross_price,tax_pc,tax_amt,discount_pc,discount_amt,net_bill_amt,created_by,updated_by,created_date," \
                               "updated_date)"\
                               "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(insert_query, row)
                connection.commit()

    if __name__ == "__main__":
        extract_sales_data('../../data/sales_dump - Sheet1.csv')

except Exception as e:
    print(e)