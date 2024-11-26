# CRUD Application for Product and Category Management

This project is a FastAPI application designed to perform high-performance Insert, Update, and Delete operations on a large dataset (100,000 records) using PostgreSQL as the database. The application includes at least two tables (Product and Category) with a minimum of five columns.

## Project Structure

```plaintext
crud-app
├── compose-postgresql.yml
├── crud
│   ├── category.py
│   ├── __init__.py
│   └── product.py
├── crud_perf_test.py
├── db
│   ├── database.py
│   ├── __init__.py
│   └── models.py
├── db-data
├── main.py
├── poetry.lock
├── pyproject.toml
├── routers
│   ├── category_api.py
│   ├── __init__.py
│   └── product_api.py
├── schemas
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   └── schema.cpython-311.pyc
│   └── schema.py
└── settings.py
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/emrekndl/fastapi-project.git
   cd fastapi-project/crud-app
   ```

2. Set up the environment variables in a `.env` file:

   ```plaintext
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/crudapp
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=crudapp
   ```

3. Use Docker Compose to set up the PostgreSQL database:

   ```bash
   docker-compose -f compose-postgresql.yml up -d
   ```

4. Install the dependencies using Poetry:

   ```bash
   poetry install
   ```

## Usage

1. Run the FastAPI application:

   ```bash
   poetry run uvicorn main:app --reload
   ```

2. Access the application at `http://localhost:8000/`.

## API Endpoints

- **Create Products**: `POST /api/products/`
- **Update Product**: `PUT /api/products/{product_id}`
- **Delete Product**: `DELETE /api/products/{product_id}`
- **Get All Products**: `GET /api/products/`
- **Get Product by ID**: `GET /api/products/{product_id}`

## Performance Testing

The `crud_perf_test.py` script is designed to test the performance of Insert, Update, and Delete operations on 100,000 records.

1. Run the performance test:

   ```bash
   poetry run python crud_perf_test.py
   ```

## Features

- Handles CRUD operations for Product and Category entities.
- Concurrent and asynchronous database interactions using SQLAlchemy and asyncpg.
- Performance testing for handling large datasets.
- Dockerized PostgreSQL setup.

