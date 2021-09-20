from establish_connection import connect

try:

    def insert_into_table(filePath):
        connection = connect()
        cursor = connection.cursor()

        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            connection.commit()

    if __name__ == "__main__":
        #department
        #insert_into_table('../../sql/queries/insert_dim_department.sql')
        #shift_type
        #insert_into_table('../../sql/queries/insert_dim_shift_type.sql')
        #shift_type
        #insert_into_table('../../sql/queries/insert_dim_role.sql')
        #status
        #insert_into_table('../../sql/queries/insert_dim_status.sql')
        #status
        insert_into_table('../../sql/queries/insert_fact_employee.sql')

except Exception as e:
    print(e)