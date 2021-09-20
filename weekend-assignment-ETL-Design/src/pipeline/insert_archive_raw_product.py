import establish_connection
from establish_connection import connect

try:

    def insert_archive_product_raw_data(filePath,filename):
        connection = connect()
        cursor = connection.cursor()
        dest_conn = connect()
        dest_cursor = dest_conn.cursor()

        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            sql = "INSERT INTO raw_product_archive(product_id,product_name,description,price,mrp,pieces_per_case,weight_per_piece,uom," \
                           "brand,category,tax_percent,active,created_by,created_date,updated_by,updated_date,filename)" \
                           "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            result = cursor.fetchall()
            for row in result:
                row = list(row)
                row.append(filename)
                row = tuple(row)
                dest_cursor.execute(sql, row)
                dest_conn.commit()

    if __name__ == "__main__":
        insert_archive_product_raw_data('../../sql/queries/query_raw_product.sql','product_dump - Sheet1.csv')


except Exception as e:
    print(e)