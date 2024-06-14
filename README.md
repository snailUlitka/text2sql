# ✨ RAG System with LangChain, Ollama, and LLaMa 💡

## 📚 Project Overview

Welcome to our awesome Retrieval-Augmented Generation (RAG) project! 🚀 This system is tailored to supercharge your AI-driven data retrieval and generation capabilities. We've packed it with fantastic features and some delightful tech ingredients to make it all work smoothly.

### What’s Inside? 🤔

This RAG system is like the Swiss Army knife of AI. Here’s a sneak peek at what it includes:

- 🔗 **LangChain**: This helps in chaining multiple components together.
- 🦙 **Ollama & LLaMa**: No, not the animal! These are powerful models working behind the scenes.
- 🗄️ **Vector Database**: For those fancy embeddings.
- 🧪 **Test Database**: Because we all need to test stuff before going big.
- 🤖 **AI Prompt Generation**: Super smart prompts to get you the best results.

### How to Start the Agent? 🚦

Our RAG system comes with an agent that can be started through the server using FastAPI. Just imagine FastAPI as the chef, and the agent as the delicious dish ready to be served. 🍽️

### Setup and Manage Connections 🔧

Effortlessly set up and manage connections to your vector database for embeddings and our small test database. Less hassle, more action! 🏃‍♂️

### Get Started and Have Fun! 🎈

Ready to dive in? This project makes setting things up a breeze and ensures you have fun while at it. Data doesn't have to be boring, and with a bit of humor and emojis, everything's more enjoyable. 😎

---

Now, go ahead, start the agent with FastAPI, and witness the power-packed combo of LangChain, Ollama, LLaMa, and our databases at work. 🚀

---

## 📜 Some information about scripts

### 🔍 `test_data.py`

A class with a set of data and useful functions for managing this data.

### 🤖 `sql_agent.ipynb`

Jupyter notebook that which shows the agent's capabilities.

### 🔌 `vc_connect.py` and `db_connect.py`

Contains connection utilities for a connection to vector and test DB. 

Key function:
- `get_selector`: Sets up a semantic similarity example selector.
- `get_vc`: Initializes a database connection for vector embeddings.
- `get_db`: Initializes a database connection for small test DB.

### ✨ `prompt_generator.py`

Class `PromptGenerator` allows the creation and management of prompts used by the AI agent. 

It includes:
- `set_example_selector`: Configures the example selector based on provided examples and embeddings.
- `get_prompt`: Generates a prompt based on given parameters like prefix/suffix and table descriptions.

---

## 🚀 Getting Started

### 🔧 Setup Instructions

1. **Clone the repository**:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Set up the database**:
    - Use the SQL script in `app/llm_app/databases/_config/...` to create the necessary database.

3. **Generate local data configuration**:
    - Run the `app/llm_app/config/local_data_template.py` script to create `local_data.py` with your local database credentials.

4. **Install dependencies**:
    - Ensure you install all necessary Python packages (not listed here, but you may refer to your package manager or a `requirements.txt` file).

### 📚 Examples

Jupyter notebook `examples/sql_agent.ipynb` to see the agent in action.

---

## 🤝 Contributing

Feel free to submit issues or pull requests. Contributions are welcome!

---

## ✨ Acknowledgments

Special thanks to all contributors and the open-source community!