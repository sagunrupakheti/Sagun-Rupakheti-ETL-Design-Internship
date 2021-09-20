from establish_connection import connect

try:

    def create_table_dim_category(filePath):
        connection = connect()
        cursor = connection.cursor()
        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            connection.commit()

    def insert_into_dim_category(filePath):
        connection = connect()
        cursor = connection.cursor()

        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            connection.commit()

    if __name__ == "__main__":
        create_table_dim_category('../../../schema/final/create_table_dim_category.sql')
        insert_into_dim_category('../../../sql/queries/insert_dim_category.sql')

except Exception as e:
    print(e)