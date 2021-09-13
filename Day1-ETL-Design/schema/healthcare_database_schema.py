import psycopg2
try:
    connection = psycopg2.connect(
        host="localhost",
        database="ETLweek1",
        user="postgres",
        password="sagun",
        port=5432
    )
    cursor = connection.cursor()

    cursor.execute("CREATE SCHEMA healthcare;")



    connection.commit()
    cursor.close()
    connection.close()
except Exception as e:
    print(e)