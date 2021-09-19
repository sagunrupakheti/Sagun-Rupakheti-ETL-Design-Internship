from establish_connection import connect

try:

    def create_table_dim_bill(filePath):
        connection = connect()
        cursor = connection.cursor()
        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            connection.commit()

    def insert_into_dim_bill(filePath):
        connection = connect()
        cursor = connection.cursor()

        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            connection.commit()

    if __name__ == "__main__":
        #create_table_dim_bill('../../../schema/final/create_table_dim_bill.sql')
        insert_into_dim_bill('../../../sql/queries/insert_dim_bill.sql')

except Exception as e:
    print(e)