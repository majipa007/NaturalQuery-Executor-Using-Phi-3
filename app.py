import chainlit as cl
import pandas as pd
from text_to_database import Text_to_database


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

    columns, result = db.execute_query(sql_query)

    await cl.Message(content=f"Query execution complete. Type of result: {type(result)}").send()

    if columns and isinstance(result, list) and len(result) > 0:
        # Create a pandas DataFrame
        df = pd.DataFrame(result, columns=columns)

        # Convert DataFrame to string
        table_str = df.to_string(index=False)

        await cl.Message(content=f"Query Result:\n```\n{table_str}\n```").send()

    elif columns:
        await cl.Message(content=f"Query returned no data. Columns: {columns}").send()
    else:
        await cl.Message(content=f"Result: {result}").send()
