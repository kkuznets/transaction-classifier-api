# Transactions Classifier API

This project provides an API for storing and querying transaction data, managing a PostgreSQL database using FastAPI, SQLModel, Alembic, and Poetry. The entire setup is containerized using Docker and managed with docker-compose, including a PostgreSQL database and pgAdmin4 for database management.

## Project Structure

- `app/main.py`: Entry point of the FastAPI application.
- `app/db.py`: Contains database setup and connection code.
- `app/routes.py`: API route definitions.
- `app/models.py`: SQLModel models representing the database schema and route-related data types.
- `app/dependencies.py`: Contains dependencies for the API.
- `app/helpers.py`: Helper functions used across the project to filter down the queries based on query params.
- `app/utils.py`: Utility functions (for now, just the classifier function to predict transaction categories).
- `Dockerfile`: Dockerfile to build the application container.
- `docker-compose.yml`: Docker Compose file to set up and run the services (FastAPI, PostgreSQL, pgAdmin4).
- `pyproject.toml`: Poetry configuration file. It's used to manage dependencies and packaging in Docker too.

## Setup and Installation

### Prerequisites

Ensure you have the following installed on your system:

- Docker
- Docker Compose

### Build and Run the Docker Container

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/kkuznets/transaction-classifier-api.git
    cd transaction-classifier-api
    ```

2. Populate the `.env` file with the necessary environment variables. Create a file named `.env` in the root directory and add the following content (example):

    ```env
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=transactions
    DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432
    OPENAI_API_KEY=your_openai_api_key
    PGADMIN_DEFAULT_EMAIL=admin@pgadmin.org
    PGADMIN_DEFAULT_PASSWORD=admin
    ```

3. Build and run the Docker containers using Docker Compose:

    ```bash
    docker-compose up --build
    ```

    This command will:
    - Build the application Docker image.
    - Start a PostgreSQL container.
    - Start a pgAdmin4 container.
    - Run the Alembic migrations to create the database schema.
    - Start the FastAPI application container.

4. Access the FastAPI application at `http://0.0.0.0:8000`.

5. Access pgAdmin4 at `http://0.0.0.0:5050` and configure it to connect to the PostgreSQL database.

## Usage

### API Endpoints

The API provides the following endpoints:

- **GET /transactions**: Retrieve a list of transactions.
- **GET /transactions/{transaction_id}**: Retrieve a specific transaction by transaction_id.
- **GET /categories_summary**: Retrieve all categories with transaction counts and total amounts.
- **GET /counterparts_per_category**: Retrieve unique counterpart names per category.
- **POST /transactions**: Create a new transaction.

Detailed programmatic API documentation can be accessed via either (if you're running the application locally):

- [ReDoc](http://0.0.0.0:8000/redoc) (preferred for all extra information and examples)
- [Swagger UI](http://0.0.0.0:8000/docs)

### Schema Migrations with Alembic

If the database schema changes, you can generate a new migration script using Alembic:

```bash
    docker-compose run web poetry run alembic revision --autogenerate -m "migration message"
```

Alembic will generate a new migration script in the `alembic/versions` directory. These migrations will run automatically when the application container is started.

### Database Management with pgAdmin4

pgAdmin4 can be used to manage the PostgreSQL database. To connect to the database:

1. Open pgAdmin4 at `http://0.0.0.0:5050`.
2. Add a new server:
    - Name: PostgreSQL
    - Hostname/address: as set in `docker-compose.yml` (default: db)
    - Port: as set in `docker-compose.yml` (default: 5432)
    - Username: as set in `.env`
    - Password: as set in `.env`

## Assumptions and Design Decisions

- **Database Choice**: PostgreSQL was chosen for its robustness and scalability.
- **ORM**: SQLModel is used for its simplicity and integration with FastAPI.
- **Containerization**: Docker is used to ensure consistent environments across different development and production setups.
- **Configuration Management**: Poetry is used for dependency management and packaging.
- **Database Migrations**: Alembic is used for handling database migrations if the schema changes.
- **API Documentation**: FastAPI provides automatic API documentation using OpenAPI via ReDoc and Swagger UI.
- **Classification Model**: The API uses an OpenAI GPT-3.5-turbo model to predict transaction categories. These categories are predefined and stored in the database for each transaction, allowing for easy querying.

### Additional Notes

- The API is designed to be simple and easy to use, with minimal setup and overhead.
- The API is designed to be extensible, with the ability to add more endpoints and functionality as needed.
- The API allowes querying transactions based on categories and/or counterpart names based on date(time) ranges provided in the query params. See the API documentation for more details.
- The POST requests are assumed to be sent with lower_case keys in the JSON body. This was not an easy choice, but it was made to keep the codebase consistent and easy to read.
- The transaction_id is not unique and is not used as a primary key. This was done to support the possibility of multiple transactions with the same transaction_id (e.g., in the case of refund or card decline). Instead, the primary key (`id` field) is generated for each transaction.
- The transaction category doesn't exist as a db table. Instead, it's stored in the `category` field of the `Transaction` model. This was done to simplify the database schema and queries. The allow-list of categories is stored in the Enum that is also used to filter categories in the serving API. This allows to easily add new categories and have them available in the API without changing the database schema.
- OpenAI API is used to classify the transaction category. There was no training data provided, so it wasn't possible to pre-train custom models. It would be possible to build a custom classifier with sentence-transformers, but if previous experienceif any indication, its accuracy would be lower than that of GPT-3.5-turbo.

### Future Improvements

- **Authentication and Authorization**: Add authentication and authorization mechanisms to secure the API.
- **Testing**: Add unit tests and integration tests to ensure the correctness of the API.
- **Logging**: Add logging to track API requests and responses for debugging and monitoring.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
