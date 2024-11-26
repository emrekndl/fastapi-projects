# Ping Connection Test

This project is a FastAPI application designed to perform concurrent pings to 512 IP addresses in the background continuously. The application logs inactive IP addresses and provides an endpoint to start the pinging process.

## Project Structure

```plaintext
ping-conn
├── ping_conn
│   ├── __init__.py
│   ├── main.py
│   └── ping.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── tests
    └── __init__.py
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/emrekndl/fastapi-projects.git>
   cd fastapi-projects/ping-conn
   ```

2. Install the dependencies using Poetry:

   ```bash
   poetry install
   ```

## Usage

1. Run the FastAPI application:

   ```bash
   <!--poetry run uvicorn ping_conn.main:app --reload-->
   python ping_conn/main.py
   ```

2. Access the application at `http://localhost:8000/`. The root endpoint (`/`) will start the ping connection test.

## Files

- `ping_conn/main.py`: Contains the FastAPI application setup and the endpoint to start the background ping process.
- `ping_conn/ping.py`: Contains the logic for performing asynchronous pings and logging inactive IP addresses.
- `tests/__init__.py`: Placeholder for potential tests.

## Features

- Concurrently pings 512 IP addresses.
- Logs inactive IP addresses.
- Runs continuously, checking and logging every 10 seconds by default.


## Notes

- The application uses Python's `asyncio` for asynchronous operations.
- `icmplib` is used for the ping functionality.
- Optionally, you can use `uvloop` for better performance.
- Optionally, you can use `ORJSONResponse` for faster JSON responses.

