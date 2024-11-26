# Multiprocess Demo Application

This project is a FastAPI application that demonstrates how to run 1000 concurrent Python processes, track their resource usage (CPU and RAM), and log their status into a SQLite database. The application uses asynchronous programming to manage the processes and ensure efficient resource usage.

## Project Structure

```plaintext
multiprocess-demo
├── multiprocess_demo
│   ├── db.py
│   ├── __init__.py
│   ├── main.py
│   └── process.py
├── poetry.lock
├── processes.db
├── pyproject.toml
├── README.md
└── tests
    └── __init__.py
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/emrekndl/fastapi-projects.git
   cd fastapi-projects/multiprocess-demo
   ```

2. Install the dependencies using Poetry:

   ```bash
   poetry install
   ```

## Usage

1. Initialize the database:

   ```bash
   poetry run python -c "from multiprocess_demo.db import init_db; import asyncio; asyncio.run(init_db())"
   ```

2. Run the FastAPI application:

   ```bash
   poetry run uvicorn multiprocess_demo.main:app --reload
   ```

3. Access the application at `http://localhost:8000/`. The root endpoint (`/`) will start the multiple process tasks.

## Features

- Starts 1000 concurrent Python processes at the same time.
- Tracks CPU and RAM usage for each process.
- Logs the status and resource usage of each process into a SQLite database.
- Uses asynchronous programming to handle multiple tasks efficiently.

## File Descriptions

- `multiprocess_demo/main.py`: Contains the FastAPI application setup and the endpoint to start the background processes.
- `multiprocess_demo/db.py`: Manages the SQLite database connections and schema.
- `multiprocess_demo/process.py`: Handles the logic for running processes and updating their status in the database.
- `tests/__init__.py`: Placeholder for potential tests.

## Database Schema

The SQLite database contains a table named `process_status` with the following columns:

- `process_id` (INTEGER): The unique ID of the process.
- `status` (TEXT): The current status of the process (e.g., Running, Finished).
- `cpu_usage` (REAL): The CPU usage of the process.
- `memory_usage` (REAL): The memory usage of the process in MB.

## Notes

- The application uses `aiosqlite` for asynchronous SQLite database interactions.
- `psutil` is used to monitor CPU and memory usage of the processes.
- `uvloop` is used for faster event loop implementation.
- Ensure that the database file `processes.db` is accessible and writable by the application.

