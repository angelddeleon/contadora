import mysql.connector
from mysql.connector import Error
import os

def execute_sql_file():
    try:
        # Database connection parameters
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=input("Enter MySQL password: "),
            database="contadora"
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Read and execute the SQL file
            with open('create_retenciones_tables.sql', 'r', encoding='utf-8') as file:
                sql_commands = file.read().split(';')
                
                for command in sql_commands:
                    if command.strip():
                        try:
                            cursor.execute(command + ';')
                            print(f"Executed command successfully")
                        except Error as e:
                            print(f"Error executing command: {e}")
                            print(f"Command was: {command}")
                
                connection.commit()
                print("SQL file executed successfully!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    execute_sql_file() 