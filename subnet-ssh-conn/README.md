# Subnet SSH Connection Project

This project scans the `172.29.0.1/16` network asynchronously and establishes simultaneous SSH connections to the found IP addresses.

## Project Overview

The main objective of this project is to:
1. Asynchronously scan the `172.29.0.1/16` network to find active IP addresses.
2. Establish simultaneous SSH connections to the found IP addresses.


## Project Structure

```
./subnet-ss-conn
├── ip_ping.py
├── main.py
├── poetry.lock
├── pyproject.toml
└── ssh_conn.py
```

- `main.py`: Contains the FastAPI application that starts the background task.
- `ip_ping.py`: Handles the IP pinging process to identify active IP addresses.
- `ssh_conn.py`: Manages SSH connections to the active IP addresses.

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/emrekndl/fastapi-project.git
    ```

2. Navigate to the project directory:
    ```
    cd fastapi-project/subnet-ss-conn
    ```

## How to Run

1. Install the necessary dependencies:
   ```
   poetry install
   ```

2. Run the FastAPI application:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. Access the endpoint to start the task:
   ```
   http -vv get http://localhost:8000/
   ```

This will start scanning the network and establish SSH connections to active IPs.




