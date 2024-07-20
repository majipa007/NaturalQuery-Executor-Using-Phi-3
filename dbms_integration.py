import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()


def execute_query(query):
    try:
        cursor.execute(query)

        # Check if the query is a SELECT statement
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            return results
        else:
            conn.commit()
            return "Query executed successfully."
    except sqlite3.Error as e:
        return f"An error occurred: {e}"


print("Welcome to the SQL Query Executor.")
print("Type your SQL queries and press Enter to execute.")
print("Type 'quit' to exit the program.")

while True:
    query = input("\nEnter your SQL query: ")

    if query.lower() == 'quit':
        break

    result = execute_query(query)
    print("Result:")
    print(result)

# Close the database connection
conn.close()
print("Database connection closed. Goodbye!")