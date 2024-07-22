import sqlite3
from text_to_query import Text_to_query


class Query_execution:
    def __init__(self):
        # Connect to the database (creates it if it doesn't exist)
        self.conn = sqlite3.connect('your_database.db')
        self.cursor = self.conn.cursor()
        self.x = Text_to_query()

    def execute_query(self, query):
        try:
            self.cursor.execute(query)

            # Check if the query is a SELECT statement
            if query.strip().upper().startswith("SELECT"):
                columns = [description[0] for description in self.cursor.description]
                results = self.cursor.fetchall()
                return columns, results
            else:
                self.conn.commit()
                return "Query executed successfully."
        except sqlite3.Error as e:
            return f"An error occurred: {e}"
#
#     def __call__(self, *args, **kwargs):
#         print("Welcome to the SQL Query Executor.")
#         print("Type your SQL queries and press Enter to execute.")
#         print("Type 'quit' to exit the program.")
#
#         while True:
#             query = input("\nEnter your SQL query: ")
#             query = self.x.query(query)
#             if query.lower() == 'quit':
#                 break
#
#             result = self.execute_query(query)
#             print("Result:")
#             print(result)
#
#         # Close the database connection
#         self.conn.close()
#         print("Database connection closed. Goodbye!")
#
#
# Query_execution()
