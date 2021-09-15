#Day 2 Documentation

**1. Extract data from a  csv file**

[//]:comment

~~~ python
 def extract_timesheet_data_view(filePath):
        with open(filePath,'r') as file:
~~~

Open the file to read the data contained in the csv file

---
~~~ python
    def create_table_raw():
        create_query = "CREATE TABLE raw_timesheet(employee_id VARCHAR(255),cost_center VARCHAR(255),punch_in_time VARCHAR(255),punch_out_time VARCHAR(255),punch_apply_date VARCHAR(255),hours_worked VARCHAR(255),paycode VARCHAR(255))"
        cursor.execute(create_query)
~~~

Using varying character for all columns to minimize the risk posed by inconsistent values

---

~~~python
row = data.strip().split(",")
~~~
Removes new line character '/n' and splits the values by a comma

---
**2. Extract data from a  JSON file**

~~~python
 with open('../../data/employee_2021_08_01.json') as json_data:
            employee_list = json.load(json_data)
~~~
Using json library of python to load the json data

---
~~~ python
        for i, record_dict in enumerate(employee_list):
            values = []
            #dictionary items
            for columns, val in record_dict.items():
                #add to values array
                values += [ str(val) ]
            # join the list of values to the query
            sql += "(" + ', '.join(values) + "),\n"
        # remove the last comma and add a semicolon to the end
        sql = sql[:-2] + ";"
        cursor.execute(sql)
~~~

* iterate over the file records
* get into each dictionary
* add each value of dictionary into values array
* concatenate the values to the query

**3. Extract data from a  XML file**

~~~python
        try:
            for event, element in etree.iterparse(filename, events=('end',), tag='row'):
~~~

* etree.iterparse returns iterator providing (event, element) pairs
* batch insert done for faster insert
