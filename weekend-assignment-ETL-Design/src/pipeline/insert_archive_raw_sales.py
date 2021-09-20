import establish_connection
from establish_connection import connect

try:

    def insert_archive_sales_raw_data(filePath,filename):
        connection = connect()
        cursor = connection.cursor()
        dest_conn = connect()
        dest_cursor = dest_conn.cursor()

        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            sql = "INSERT INTO raw_sales_archive( id,transaction_id,bill_no,bill_date,bill_location,customer_id,product_id,qty,uom," \
                           "price,gross_price,tax_pc,tax_amt,discount_pc,discount_amt,net_bill_amt,created_by,updated_by,created_date," \
                           "updated_date,filename)" \
                           "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            result = cursor.fetchall()
            for row in result:
                row = list(row)
                row.append(filename)
                row = tuple(row)
                dest_cursor.execute(sql, row)
                dest_conn.commit()

    if __name__ == "__main__":
        insert_archive_sales_raw_data('../../sql/queries/query_raw_sales.sql','sales_dump - Sheet1.csv')


except Exception as e:
    print(e)