#Sales data documentation

**1. The data given in the .sql file is used to create tables, establish relationships and insert data into the tables**
The 5 tables include:
   * Users
   * Administrator
   * Category
   * Product 
   * Sales
***    
**2. Query the table for extraction**    
~~~python 
SELECT s.user_id, u.username, s.product_id, p.name, p.category_id, c.name, p.price, s.price, s.quantity,
(p.quantity-s.quantity),s.updated_at
FROM sales s
JOIN users u
ON u.id = s.user_id
JOIN products p
ON p.id = s.product_id
JOIN categories c
ON c.id = p.category_id;
~~~
* Start by querying the sales table
* List out all the necessary attributes to export
* JOIN tables accordingly
* For the remaining quantity, subtract the sold quantity from total quantity of the product
***

**3. Create a table for storing**
~~~python
CREATE TABLE data_extract_scenario(
    user_id VARCHAR(255),
    username VARCHAR(255),
    product_id VARCHAR(255),
    product_name VARCHAR(255),
    category_id VARCHAR(255),
    category_name VARCHAR(255),
    current_price VARCHAR(255),
    sold_price VARCHAR(255),
    sold_quantity VARCHAR(255),
    remaining_quantity VARCHAR(255),
    sales_date VARCHAR(255)
);
~~~
* A table data_extract_scenario created
* The data from the query needs to be copied to this table

**4. Establish connection using environment**

* Create a .env file and add the values for user, password, host, port and database
* The values are written without spacing, comma and quotes

~~~python
import psycopg2
from dotenv import load_dotenv
load_dotenv()
import os
~~~
* import psycopg2 for connection
* import dotenv for environment variables
* import load_dotenv to load the environment file
* import os for interacting with the file

~~~python
    def connect():
        return psycopg2.connect(
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
            database=os.getenv("database2")
        )
~~~
* connect to psycopg2
* get environment using os and assign the variables

**5. Insert from the query to the table

~~~python
    def extract_db_data(filename):
        source_conn = connect()
        dest_conn = connect()

        source_cursor = source_conn.cursor()
        dest_cursor = dest_conn.cursor()

        with open(filename) as file:
            sql = "".join(file.readlines())
            source_cursor.execute(sql)
            result = source_cursor.fetchall()
            sql = 'INSERT INTO data_extract_scenario(user_id, username, product_id, product_name, category_id,category_name,' \
                  'current_price,sold_price,sold_quantity,remaining_quantity,sales_date)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            for row in result:
                dest_cursor.execute(sql,row)
                dest_conn.commit()
~~~

* open the file containing the query
* fetch all the rows
* insert the rows into the created table
