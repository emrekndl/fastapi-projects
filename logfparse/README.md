# LogfParse Project

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.70.0-green.svg)
![Podman](https://img.shields.io/badge/Podman-3.0.0-lightgrey.svg)
![Go](https://img.shields.io/badge/Go-1.17-blue.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.22-red.svg)

This project is a FastAPI-based application designed to parse and handle DHCP request data from streaming logs.

## Project Structure

```plaintext
.
├── compose-postgresql.yml
├── db-data
├── log_demo_server
│   ├── cmd
│   │   └── main.go
│   ├── Dockerfile.logdemo
│   ├── go.mod
│   └── stream_demo_data.txt
├── logfparse
│   ├── crud
│   │   ├── dhcp_request_data.py
│   │   ├── __init__.py
│   │   └── parse_tasks.py
│   ├── db
│   │   ├── database.py
│   │   ├── __init__.py
│   │   └── models.py
│   ├── __init__.py
│   ├── main.py
│   ├── routers
│   │   ├── dhcp_request_data_api.py
│   │   ├── __init__.py
│   │   └── parse_task_api.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── schema.py
│   ├── service
│   │   ├── __init__.py
│   │   └── log_parser_service.py
│   ├── settings.py
│   ├── tasks
│   │   ├── __init__.py
│   │   └── log_parser_task.py
│   └── utils
│       ├── foo_bar_baz.py
│       ├── __init__.py
│       ├── ip_address_validator.py
│       ├── parser_templates
│       │   └── dhcp_request.template
│       ├── ssh_client.py
│       └── task_status.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── tests
    ├── __init__.py
    └── parse_ssh_test.py
```

## Docker Setup

### Build and Run

The Dockerfile and `compose-postgresql.yml` file help you build and run the project using Docker and Podman.

1. **Build the Docker Image:**

```sh
podman build -t log-demo-app-with-ssh -f Dockerfile.logdemo .
```

2. **Run the Docker Container:**

```sh
podman run -d -p 2222:22 -p 8080:8080 --name log-demo-container log-demo-app-with-ssh
```

## API Documentation

The project uses OpenAPI 3.1.0 for API documentation. You can access the API documentation at `/docs` when the server is running.

### Endpoints

- `/api/data`:
  - `GET`: Get all data.
  - `POST`: Create new data.
- `/api/data/{data_id}`:
  - `GET`: Get data by ID.
  - `PUT`: Update data by ID.
  - `DELETE`: Delete data by ID.
- `/api/tasks`:
  - `GET`: Get all tasks.
  - `POST`: Create a new task.
- `/api/tasks/{task_id}`:
  - `GET`: Get task by ID.
  - `PUT`: Update task by ID.
  - `DELETE`: Delete task by ID.
  - `/start`: Start task.
  - `/stop`: Stop task.

## Parsing Functionality

The application listens to a specific SSH command for 300 seconds to gather and parse streaming log data. It extracts the following fields from logs that include `"OPTION: 53 (1) DHCP message type 3 (DHCPREQUEST)"`:

1. Client Identifier
2. Request IP Address
3. Vendor Class Identifier
4. Host Name

Parsed data is stored in a text file or database, depending on configuration.

### Example TextFSM Template

```plaintext
Value ClientIdentifier (\w{2}(:\w{2}){6})
Value RequestIpAddress (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
Value VendorClassIdentifier (.+)
Value HostName (\S+)

Start
  ^OPTION:\s53\s\(\s1\)\sDHCP\smessage\stype\s3\s\(\S+\) -> Con

Con
  ^OPTION:\s\d+\s\(\s\d+\)\sClient-identifier\s${ClientIdentifier}
  ^OPTION:\s\d+\s\(\s\d+\)\sRequest\sIP\saddress\s${RequestIpAddress}
  ^OPTION:\s\d+\s\(\s\d+\)\sVendor\sclass\sidentifier\s${VendorClassIdentifier}
  ^OPTION:\s\d+\s\(\s\d+\)\sHost\sname\s${HostName}
```

## Background Tasks

The application can run tasks in the background using `asyncio`. These tasks are designed to execute SSH commands continuously, collect data from logs, and parse the results using `TextFSM`.

### Task Management Endpoints

- **Start Task:**
    - This endpoint starts a specified task.
    - The system checks if the task is already running. If it is not, the task is started using `asyncio` to run it in the background.

- **Stop Task:**
    - This endpoint stops a specified task.
    - The system checks if the task is running and stops it by setting a stop signal.

### Streaming Logs

The project includes a Go-based application to simulate streaming logs. This application continuously writes logs to a file, which can then be parsed by the FastAPI application. It handles creating and resetting log blocks, ensuring a consistent stream of data for the parser.

## Installation

### Prerequisites

- **Python 3.11**
- **Podman**
- **PostgreSQL**

### Steps

1. **Clone the Repository:**

```sh
git clone https://github.com/emrekndl/fastapi-projects.git
cd fastapi-projects/logfparse
```

2. **Set Up the Environment:**

   Create a `.env` file in the root directory and add the following environment variables:

```plaintext
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_postgres_db
DATABASE_URL=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost:5432/$POSTGRES_DB
SSH_PASSWORD=your_ssh_password
SSH_USERNAME=your_ssh_username
SSH_HOST=your_ssh_host
SSH_PORT=your_ssh_port
```

3. **Install Dependencies:**

   Use Poetry to install dependencies:

```sh
poetry install
```

4. **Run the Application:**

   Start the Docker containers:

```sh
podman-compose -f compose-postgresql.yml up
```

   Run the FastAPI application:

```sh
python logfparse/main.py
```

## Request And Response Examples

### Requests
Task Creation
```plaintext
POST /api/tasks HTTP/1.1
Host: localhost:8080
Content-Type: application/json

{
    "task_name": "logfparse",
    "run_command": "tail -f",
    "is_running": false,
    "command_run_time": 300,
    "log_file_path": "/root/stream_demo.log",
    "parse_template_path": "logfparse/utils/parser_templates/dhcp_request.template"
}
```

### Responses
Data Response
```plaintext
HTTP/1.1 201 Created
Content-Type: application/json

{
    "client_identifier": "00:00:00:00:00:00",
    "request_ip_address": "244.178.44.111",
    "vendor_class_identifier": "VendorClassIdentifier",
    "host_name": "HostName",
    id: 1,
    "created_at": "2023-06-26T12:34:56.789Z",
    "updated_at": "2023-06-26T12:34:56.789Z"
}
```
}
