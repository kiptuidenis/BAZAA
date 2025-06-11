# BAZAA - Financial Management App

A microservices-based financial management application that helps users manage their daily expenses through automated MPESA transactions.

## Architecture

The application is built using a microservices architecture with the following services:

- **Auth Service**: Handles user authentication and registration
- **Budget Service**: Manages budgets and transactions
- **MPESA Service**: Handles MPESA payments and transactions
- **Notification Service**: Manages notifications across different channels

## Security Features

- JWT-based authentication
- Environment variable management
- Secure password handling
- MPESA API integration with proper security measures
- Database security with proper user permissions
- CORS configuration
- Input validation and sanitization

## Prerequisites

- Python 3.8+
- MySQL 8.0+
- Docker and Docker Compose
- MPESA API credentials
- SMTP server for email notifications

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bazaa.git
cd bazaa
```

2. Create and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your actual values
```

3. Start the services using Docker Compose:
```bash
docker-compose up -d
```

4. Run migrations:
```bash
docker-compose exec auth-service python manage.py migrate
docker-compose exec budget-service python manage.py migrate
docker-compose exec mpesa-service python manage.py migrate
docker-compose exec notification-service python manage.py migrate
```

5. Start the notification processor:
```bash
docker-compose exec notification-service python notification_service/tasks.py
```

## Development Guidelines

1. **Security**:
   - Never commit sensitive information to Git
   - Always use environment variables for secrets
   - Keep dependencies updated
   - Follow the principle of least privilege

2. **Code Style**:
   - Follow PEP 8 guidelines
   - Use meaningful variable and function names
   - Add proper documentation
   - Write unit tests for new features

3. **Git Workflow**:
   - Create feature branches from main
   - Write meaningful commit messages
   - Create pull requests for code review
   - Keep commits atomic and focused

## API Documentation

API documentation is available at:
- Auth Service: http://localhost:8001/api/docs/
- Budget Service: http://localhost:8002/api/docs/
- MPESA Service: http://localhost:8003/api/docs/
- Notification Service: http://localhost:8004/api/docs/

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 