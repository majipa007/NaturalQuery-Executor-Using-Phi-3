# Text-to-SQL Converter

---

## Overview

The Text-to-SQL Converter is an advanced natural language processing tool designed to transform plain English queries into SQL commands. This application bridges the gap between human language and database queries, making data access more intuitive and efficient for users without extensive SQL knowledge.

## Features

- Natural Language Processing: Converts English queries to SQL
- AI-Powered Model: Utilizes state-of-the-art language models
- Database Integration: Executes queries on SQLite database
- Real-time Interaction: Implements Chainlit for interactive user interface
- User-Friendly Design: Accessible to users with varying levels of technical expertise

## Installation

To set up the Text-to-SQL Converter, follow these steps:

1. Clone the repository:
```commandline
git clone git@github.com:majipa007/text-to-SQL.git
cd text-to-SQL
```


2. Install dependencies:
```commandline
pip install -r requirements.txt
```

## Usage

To launch the application:

1. Run the following command:
```commandline
chainlit run chainlit.py -w
```
2. Open a web browser and navigate to `http://localhost:8000`

3. Input your query in natural language in the chat interface

4. The system will generate and execute the corresponding SQL query

## Technical Architecture

The Text-to-SQL Converter is built on the following technologies:

- Hugging Face Transformers
- Chainlit
- Python
- SQLite

Key components include:

1. Text_to_database Class: Manages model initialization, query generation, and database operations
2. Chainlit Integration: Provides the interactive user interface
3. Query Processing Pipeline: Handles natural language input, SQL generation, and query execution

## Contributing

We welcome contributions to the Text-to-SQL Converter project.

## License

This project is licensed under the MIT License.

## Acknowledgements

We extend our gratitude to the developers and researchers behind the language model (Microsoft and Unsloth), Dataset (https://huggingface.co/b-mc2) and libraries that power this application.

---

