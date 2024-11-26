# SSH Command Execution via FastAPI

This project is a FastAPI application designed to connect to multiple remote Linux servers over SSH and execute commands or send configurations concurrently across a given network block.

## Project Structure

```plaintext
ssh-cmd
├── Dockerfile
├── Dockerfile.ssh_server
├── poetry.lock
├── pyproject.toml
├── README.md
├── run_ssh_servers.sh
├── ssh_cmd
│   ├── __init__.py
│   ├── main.py
│   ├── network_scanner.py
│   └── ssh_client.py
└── tests
    └── __init__.py
```

## Installation

1. Clone the repository:

   ```bash
   git clone  https://github.com/emrekndl/fastapi-projects.git
   cd fastapi-projects/ssh-cmd
   ```

2. Install the dependencies using Poetry:

   ```bash
   poetry install
   ```

## Usage

1. Build and run the Docker containers for SSH servers:

   ```bash
   podman build -f Dockerfile.ssh_server -t ssh_server .
   podman network create --subnet=172.18.0.0/29 my_custom_network
   ./run_ssh_servers.sh
   podman run -dit --net my_custom_network --ip 172.18.0.1 -p 8001:8001 --name ssh_cmd ssh_cmd:latest
   ```

2. Run the FastAPI application:

   ```bash
   poetry run uvicorn ssh_cmd.main:app --reload
   ```

3. Access the application at `http://localhost:8001/`.

## API Endpoint

- **Execute Command**: `POST /execute-command/`
  - Request Body:
    ```json
    {
      "network": "172.18.0/29",
      "command": "ip a",
      "username": "root",
      "password": "toor"
    }
    ```

## Features

- Connects to multiple remote Linux servers over SSH concurrently.
- Executes specified commands or sends configurations to all servers in the given network block.
- Logs the output of the SSH commands.
- Runs asynchronously to handle multiple tasks efficiently.
- Dockerized setup for easy deployment and testing.

## Docker Setup

- **Dockerfile**: Sets up the main FastAPI application.
- **Dockerfile.ssh_server**: Sets up an SSH server for testing.
- **run_ssh_servers.sh**: Script to run multiple SSH server containers using Podman.

## File Descriptions

- `ssh_cmd/main.py`: Contains the FastAPI application setup and the endpoint to start the background SSH command execution.
- `ssh_cmd/network_scanner.py`: Handles network scanning and SSH command execution.
- `ssh_cmd/ssh_client.py`: Manages SSH connections and command execution on remote servers.

## Notes

- Ensure that the `parallel` tool is installed for the `run_ssh_servers.sh` script.
- Usernames and passwords should be encrypted and securely stored. The current implementation uses plain text for simplicity.
- You can modify the `run_ssh_servers.sh` script to customize the SSH server setup as needed.
