# Credit Card Demmo Backend API Application

This repository contains a Django-based backend service that simulates transaction handling and summary views for a fictional application. It includes a REST API with endpoints for transaction authorization, settlement, clearing, and more. The service uses PostgreSQL for data persistence and Docker for easy setup and deployment.

## Features

- Transaction authorization, settlement, and cancellation.
- Payment initiation and posting.
- User summary views for quick and detailed transaction overviews.
- Comprehensive Swagger documentation for easy access and testing of all API endpoints.
- Dockerized environment for easy setup.

## Requirements

- Docker
- Docker Compose

## Installation & Running

1. Clone the repository to your local machine:

```sh
git clone https://github.com/KoushikAS/pomelo-test.git
cd pomelo-test
```
## Start the application using Docker Compose:

Before Starting the application make sure the port 8000, 5050 and 5000 are free.

```sh
docker-compose up --build
```
This command will build the Docker images and start the services defined in your docker-compose.yml file.

## Accessing the Application

- API Endpoints: Once the Docker containers are up and running, the API will be available at http://127.0.0.1:8000/
- Swagger Documentation: Access the Swagger UI for the API documentation and to interact with the API at http://127.0.0.1:8000/swagger/

## Database Management with pgAdmin

For easier view of DB I have enabled PG Admin to connect and view DB.

- **Access pgAdmin**: Navigate to `http://127.0.0.1:5050/` in your web browser to manage the PostgreSQL database.
- **Login Credentials**: Use the email `dummy@duke.edu` and the password `root` for access.
- **Connecting to the Database**:
  - Click on "Add New Server" to establish a new database connection.
  - Under the "General tab:
    - Name: any value like `db`.
  - Under the "Connection" tab:
    - Host name/address: `db`
    - Username: `pomelo`
    - Password: `pomelopswd`

## API Endpoints
The service includes the following endpoints:

- POST /transaction/authorization: Authorizes transactions.
- POST /transaction/settled: Settles previously authorized transactions.
- POST /transaction/authorization-cleared: Clears previously authorized transactions.
- POST /payment/initiated: Initiates a payment.
- POST /payment/posted: Posts a payment.
- POST /payment/canceled: Cancels a payment.
- GET /users/< userId >/summary: Retrieves a quick summary of the user's transactions.
- GET /users/< userId >/detailed-summary: Retrieves a detailed summary of the user's transactions.

Each endpoint accepts specific parameters and returns a JSON response as documented in the Swagger UI.

## Development
This project follows standard Django project structure. The main application logic resides in the logic.py file, while the views are located in views.py. The helper_functions.py file contains utility functions used across the application.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
