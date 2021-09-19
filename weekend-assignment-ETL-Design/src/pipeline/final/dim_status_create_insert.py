from establish_connection import connect

try:

    def create_table_dim_status(filePath):
        connection = connect()
        cursor = connection.cursor()
        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            connection.commit()

    def insert_into_dim_status(filePath):
        connection = connect()
        cursor = connection.cursor()

        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            connection.commit()

    if __name__ == "__main__":
        create_table_dim_status('../../../schema/final/create_table_dim_status.sql')
        insert_into_dim_status('../../../sql/queries/insert_dim_status.sql')

except Exception as e:
    print(e)