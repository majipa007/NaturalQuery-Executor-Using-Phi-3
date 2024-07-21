from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import sqlite3
import chainlit as cl
import torch


class Text_to_database:
    def __init__(self):
        quantization_config = BitsAndBytesConfig(load_in_4bit=True)

        self.model = AutoModelForCausalLM.from_pretrained("Majipa/text-to-SQL",
                                                          device_map="cuda",
                                                          torch_dtype=torch.float16,
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


@cl.on_chat_start
async def start():
    cl.user_session.set("db", Text_to_database())
    # Send a welcome message
    welcome_message = """
        👋 Welcome to the Text-to-SQL Assistant!
        
        Enter your question or description in natural language.
        
        For example, you could ask:
        "Show me all the rows where first name starts with j"
        "Show me all the name and phone numbers of people where first name starts with j"
        "insert (20, 'Hitman', 'Dark', 'hitman.dark@email.com', '+1-123-223-4567')"
        Let's get started! What would you like to know about your contacts database?
        """
    await cl.Message(content=welcome_message).send()


@cl.on_message
async def main(message: cl.Message):
    db = cl.user_session.get("db")
    # await cl.Message(content="db variable set").send()
    # Generate SQL query
    sql_query = db.query(message.content)
    # await cl.Message(content="query retrieved").send()
    await cl.Message(content=f"Generated SQL Query:\n```sql\n{sql_query}\n```").send()

    # Execute query
    result = db.execute_query(sql_query)

    if isinstance(result, list):
        # If the result is a list, it's likely from a SELECT query
        # Convert the result to a formatted string
        result_str = "\n".join([str(row) for row in result])
        await cl.Message(content=f"Query Result:\n```sql\n{result_str}\n```").send()
    else:
        # For non-SELECT queries or error messages
        await cl.Message(content=f"Result: {result}").send()
