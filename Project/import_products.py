import pandas as pd
import json
import mysql.connector

# Read the JSON data from the file
with open("petlebi_products.json") as f:
    data = json.load(f)
    data = pd.DataFrame(data)


# Connection to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="user_54",
    database="Petlebi_db"
)
cursor = connection.cursor()

# Read sql file
with open("petlebi_create.sql", "r") as sql_file:
    sql_query = sql_file.read()

# Run sql query
cursor.execute(sql_query)
connection.commit()

cursor.close()
connection.close()

# Connection to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="user_54",
    database="Petlebi_db"
)
cursor = connection.cursor()

# Read the SQL file
with open("petlebi_insert.sql", "r") as sql_file:
    sql_query = sql_file.read()

# All datas are imported to the database
for index, row in data.iterrows():
    cursor.execute(sql_query, tuple(row))

# Save all changes
connection.commit()

# Connection and cursor close
cursor.close()
connection.close()

print("All datas are imported successfully.")

