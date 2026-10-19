from app.database.connection import get_db_connection

try:
    connection = get_db_connection()
    print("MySQL connected successfully!")

    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    print(cursor.fetchall())

    cursor.close()
    connection.close()

except Exception as error:
    print("Connection failed:", error)