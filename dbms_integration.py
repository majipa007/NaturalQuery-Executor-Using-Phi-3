import sqlite3


class Query_execution:
    def __init__(self):
        # Connect to the database (creates it if it doesn't exist)
        self.conn = sqlite3.connect('your_database.db')
        self.cursor = self.conn.cursor()

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
