# Library Service Project Readme

## Overview

The Library Service Project 📚 is a comprehensive online management system tailored to address the challenges encountered by local libraries in manually tracking books, borrowings, users, and payments. The primary objective is to streamline administrative processes, enhance user experience, and introduce seamless online payment capabilities.

## Features

The Library Service Project incorporates a range of features to efficiently manage library operations and provide a seamless experience for users. Here are some key features:

1. **Book Management 📚:**
   - Add, edit, and delete books in the library catalog.
   - Track book availability and current status (available, checked out, overdue).

2. **User Management 👤:**
   - Create and manage user accounts.
   - View user details and history of borrowings.

3. **Borrowing Operations 🔄:**
   - Borrow and return books with automated due date calculations.
   - Receive notifications for overdue books.

4. **Payment Integration 💳:**
   - Enable secure online payments for fines and fees.
   - Integrated with Stripe for reliable and secure payment processing.

5. **Notifications 📣:**
   - Receive notifications via Telegram for important events (book borrowings, overdue reminders, and payments).

6. **Authentication and Authorization 🔐:**
   - Implement JWT token-based authentication for secure user access.
   - Define roles and permissions to control access to different functionalities.

7. **Swagger Documentation 📖:**
   - Utilize Swagger for comprehensive and interactive API documentation.
   - Easily explore and test API endpoints.

8. **Dockerized Deployment 🚀:**
   - Deploy the entire system using Docker Compose for consistent and scalable deployment across environments.

9. **Automated Testing 🧪:**
   - Implement a suite of automated tests to ensure the reliability and correctness of system functionalities.

10. **Celery for Background Tasks 🌐:**
    - Utilize Celery for handling background tasks such as asynchronous notifications and email sending.
    - Enhance system responsiveness and efficiency by offloading time-consuming operations.

11. **Admin Interface 🌐:**
    - Integrate Django Admin for a powerful and user-friendly administrative interface.
    - Easily manage and visualize data, users, and system configurations through the admin dashboard.

12. **Flexible Configuration 🛠️:**
    - Easily configure the system through environment variables, making it adaptable to various deployment scenarios.

These features collectively contribute to the efficient management of library resources, enhance user interactions, and promote a modern and user-friendly library experience.
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
### System Requirements

Before running the Library Service Project, ensure that your system meets the following requirements:

1. **Docker and Docker Compose:**
   - Docker: [Install Docker](https://docs.docker.com/get-docker/)

## How to Run

Ensure that you have Docker, Python (with the required version), and the specified Python dependencies installed to run the Library Service Project successfully.

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