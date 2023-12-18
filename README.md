# Library Service Project Readme

## Overview

The Library Service Project 📚 is a comprehensive online management system tailored to address the challenges encountered by local libraries in manually tracking books, borrowings, users, and payments. The primary objective is to streamline administrative processes, enhance user experience, and introduce seamless online payment capabilities.

## Project Structure

### Dockerized Deployment

The Library Service Project is designed to be deployed using Docker Compose, simplifying the setup process and ensuring consistent deployment across different environments.

### Services

The project is divided into several services, each handling specific aspects of the library management system:

1. **Books Service 📖:**
   - Manages CRUD operations for books.
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

## How to Run

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/library-service.git
   cd library-service
   ```

2. **Build and Run Docker Containers:**
- Execute the following command to build and run the Docker containers:
  ```bash
  docker-compose up --build
  ```

3. **Access the API:**
   - Open your browser and navigate to [http://localhost:8000/doc/swagger](http://localhost:8000/doc/swagger) for API documentation.

## Automated Tests

The project includes a suite of automated tests to ensure the reliability of implemented functionalities. To run the tests within the Docker environment, use the following command:

```bash
docker-compose exec web python manage.py test
```

This ensures that the entire system, including dependencies, is thoroughly tested.