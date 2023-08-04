# CoRider Internship Take-Home Interview Assignment

Welcome to the CoRider Internship Take-Home Interview Assignment project! This project is a Flask-based REST API that provides CRUD operations on a User resource. The application uses MongoDB as the database to store user information securely.

## REST API Endpoints

- **GET /users**: Returns a list of all users.

- **GET /users/\<id>**: Returns the user with the specified ID.

- **POST /users**: Creates a new user with the specified data.

- **PUT /users/\<id>**: Updates the user with the specified ID with the new data.

- **DELETE /users/\<id>**: Deletes the user with the specified ID.

## Demo Video
Demo Video of the project is on Youtube.
You can find it [here](https://youtu.be/a1ANr5miPkA)

## Requirements

To successfully run this application, make sure you have the following components installed:

- Python
- Docker (as using Docker is mandatory for this project)
- Postman (for testing the REST API endpoints)

## Setup

1. Clone this repository to your local machine.
2. Create a new Python virtual environment and activate it.
3. Create a virtual environment and activate it
    ```bash
    python -m venv venv
    source venv/bin/activate   
    ```
4. Install the required packages using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
    ```
5. Create a `.env` file in the root directory of the project and add the following environment variables:
    ```bash
    MONGO_URI=<your_mongodb_uri>
    DB_NAME=<your_mongodb_database_name>
    ```
6. Run the application using the following command:
    ```bash
    python app.py
    ```
## Run using Docker
Replace MONGO_URI and DB_NAME in the docker-compose.yml file with your own MongoDB URI and database name. Then run the following command:
```bash
docker-compose up
```
## Results
The application should now be running on `http://localhost:5000/`. You can test the endpoints using Postman or any other REST API testing tool.