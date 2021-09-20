from establish_connection import connect

try:

    def create_table_fact_product_sales(filePath):
        connection = connect()
        cursor = connection.cursor()
        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            connection.commit()

    def insert_into_fact_product_sales(filePath):
        connection = connect()
        cursor = connection.cursor()

        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            connection.commit()

    if __name__ == "__main__":
        create_table_fact_product_sales('../../../schema/final/create_fact_product_sales.sql')
        insert_into_fact_product_sales('../../../sql/queries/insert_fact_product_sales.sql')

except Exception as e:
    print(e)