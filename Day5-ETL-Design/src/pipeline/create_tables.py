from establish_connection import connect

try:

    def create_table_dim_fact(filePath):
        connection = connect()
        cursor = connection.cursor()
        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            connection.commit()


    #extract the data and insert it into the table
    def extract_timesheet_data_insert(filePath):
        connection = connect()
        cursor = connection.cursor()
        with open(filePath,'r') as file:
            i=0
            #delete if any data exists in the table
            sql = "DELETE FROM raw_employee;"
            cursor.execute(sql)
            for data in file:
                if i==0:
                    i+=1
                    continue
                #removes any new lines and splits the data by a comma
                row = data.strip().split(",")
                #%s to pass the rows
                insert_query = 'INSERT INTO raw_employee(employee_id,first_name,last_name,department_id,department_name,manager_employee_id,employee_role,' \
                  'hire_date,terminated_date,terminated_reason,dob,fte,location,salary)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(insert_query,row)

    if __name__ == "__main__":
        # create_table_dim_fact('../../schema/create_table_dim_department.sql')
        # create_table_dim_fact('../../schema/create_table_dim_period.sql')
        # create_table_dim_fact('../../schema/create_table_dim_role.sql')
        # create_table_dim_fact('../../schema/create_table_dim_shift_type.sql')
        # create_table_dim_fact('../../schema/create_table_dim_status.sql')
        # create_table_dim_fact('../../schema/create_table_fact_employee.sql')
        # create_table_dim_fact('../../schema/create_table_fact_timesheet.sql')
        extract_timesheet_data_insert('../../data/employee_2021_08_01 - Sheet1.csv')

except Exception as e:
    print(e)