# Library Service Project Readme

## Overview

The Library Service Project 📚 is an online management system designed to address the challenges faced by a local library with manual tracking of books, borrowings, users, and payments. The project aims to streamline administrative processes, enhance user experience, and introduce online payment capabilities.

## Project Structure

### Apps

1. **Books Service 📖:**
   - Manages the CRUD operations for books.
   - Ensures proper permissions for book-related actions.

2. **Users Service 👤:**
   - Handles user-related operations, including user creation and retrieval.

3. **Borrowings Service 🔄:**
   - Manages borrowings, returns, and overdue notifications.
   - Integrates with the Notifications Service for notifications.

4. **Payments Service 💳:**
   - Facilitates payment-related functionalities.
   - Integrates with Stripe for secure payment processing.

5. **Notifications Service 📣:**
   - Manages notifications, including Telegram notifications for borrowings and payments.

## Authentication

User authentication is implemented using JWT tokens. Users are required to authenticate to perform certain actions, ensuring data security.

## API Documentation

API documentation is available through Swagger, providing detailed information about available endpoints and their functionalities.

## How to Run

### Setup Without Docker

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/library-service.git
   cd library-service
   ```

2. **Environment Setup:**
   - Create a virtual environment and activate it.
   - Install project dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Database Migration:**
   - Apply database migrations:
     ```bash
     python manage.py migrate
     ```

4. **Run the Server:**
   - Start the Django development server:
     ```bash
     python manage.py runserver
     ```

5. **Access the API:**
   - Open your browser and navigate to [http://localhost:8000/swagger](http://localhost:8000/swagger) for API documentation.

### Setup With Docker

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/library-service.git
   cd library-service
   ```

2. **Create Docker Image:**
   - Build the Docker image:
     ```bash
     docker build -t library-service .
     ```

3. **Run Docker Container:**
   - Run the Docker container:
     ```bash
     docker run -p 8000:8000 library-service
     ```

4. **Access the API:**
   - Open your browser and navigate to [http://localhost:8000/doc/swagger](http://localhost:8000/doc/swagger) for API documentation.

## Automated Tests

The project includes automated tests to ensure the reliability of the implemented functionalities. Run the tests using the following command:

```bash
python manage.py test
```
