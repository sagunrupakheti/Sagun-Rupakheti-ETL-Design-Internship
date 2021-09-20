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

    def extract_product_data(filePath):
        connection = connect()
        cursor = connection.cursor()

        with open(filePath, 'r') as file:
            i = 0
            # delete if any data exists in the table
            sql = "DELETE FROM raw_product;"
            cursor.execute(sql)
            for data in file:
                if i == 0:
                    i += 1
                    continue
                # removes any new lines and splits the data by a comma
                row = data.strip().split(",")
                # %s to pass the rows
                insert_query = "INSERT INTO raw_product(product_id,product_name,description,price,mrp,pieces_per_case,weight_per_piece,uom," \
                               "brand,category,tax_percent,active,created_by,created_date,updated_by,updated_date)" \
                               "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(insert_query, row)
                connection.commit()

    if __name__ == "__main__":
        extract_product_data('../../data/product_dump - Sheet1.csv')

except Exception as e:
    print(e)