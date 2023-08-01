import mysql.connector

#change details 
mydb = mysql.connector.connect(
    host = "host",
    user = "user",
    password = "password",
    database = "db"
)
