import establish_connection
from establish_connection import connect

try:

    def insert_archive_customer_raw_data(filePath,filename):
        connection = connect()
        cursor = connection.cursor()
        dest_conn = connect()
        dest_cursor = dest_conn.cursor()

        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            sql = 'INSERT INTO raw_customer_archive(customer_id,user_name,first_name,last_name,country,town,active,filename)VALUES(%s,%s,%s,%s,%s,%s,%s,%s);'
            result = cursor.fetchall()
            for row in result:
                row = list(row)
                row.append(filename)
                row = tuple(row)
                dest_cursor.execute(sql, row)
                dest_conn.commit()

    if __name__ == "__main__":
        insert_archive_customer_raw_data('../../sql/queries/insert_archive_raw_customer.sql','customer_dump - Sheet1.csv')


except Exception as e:
    print(e)