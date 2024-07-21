from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import sqlite3


class Text_to_database:
    def __init__(self):
        quantization_config = BitsAndBytesConfig(load_in_4bit=True)

        self.model = AutoModelForCausalLM.from_pretrained("Majipa/text-to-SQL",
                                                          device_map="cuda",
                                                          torch_dtype="auto",
                                                          quantization_config=quantization_config)

        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
        )
        self.generation_args = {
            "max_new_tokens": 500,
            "temperature": 0,
            "return_full_text": False,
        }
        # Connect to the database (creates it if it doesn't exist)
        self.conn = sqlite3.connect('your_database.db')
        self.cursor = self.conn.cursor()

    def query(self, inp):
        messages = [
            {"role": "system", "content": "You are a helpful text-to-SQL assistant."},
            {"role": "user",
             "content": f"question:{inp} context:CREATE TABLE contacts (contact_id INTEGER PRIMARY KEY,first_name TEXT "
                        f"NOT NULL,last_name TEXT NOT NULL,email TEXT NOT NULL UNIQUE,phone TEXT NOT NULL UNIQUE)"},
        ]
        output = self.pipe(messages, **self.generation_args)
        return output[0]['generated_text']

    def execute_query(self, query):
        try:
            self.cursor.execute(query)

            # Check if the query is a SELECT statement
            if query.strip().upper().startswith("SELECT"):
                results = self.cursor.fetchall()
                return results
            else:
                self.conn.commit()
                return "Query executed successfully."
        except sqlite3.Error as e:
            return f"An error occurred: {e}"

    def __call__(self, *args, **kwargs):
        print("Welcome to the SQL Query Executor.")
        print("Type your SQL queries and press Enter to execute.")
        print("Type 'quit' to exit the program.")

        while True:
            query = input("\nEnter your SQL query: ")
            if query.lower() == 'quit':
                break
            query = self.query(query)
            result = self.execute_query(query)
            print("Result:")
            for i in result:
                print(i)

        # Close the database connection
        self.conn.close()
        print("Database connection closed. Goodbye!")


x = Text_to_database()
x.__call__()