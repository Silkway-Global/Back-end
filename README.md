
# Project Setup Guide

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Environment Variables**
   
   Ensure the `.env` file is correctly set up in the `static` directory with the following variables:
   ```
   DB_NAME=silkwayglobal
   DB_USER=postgres
   DB_PASSWORD=@Grandtalim1
   DB_HOST=db
   DB_PORT=5432
   ```

3. **Build and Run the Containers**
   
   Navigate to the `static` directory and run:
   ```bash
   docker-compose up --build
   ```
   
   This will build the Docker images and start the containers.

4. **Access the Application**
   
   The application will be accessible at `http://localhost:8000`. 

   **Manual Migration Required**: To apply database migrations, go to Docker -> `static-web-1` container -> `EXEC` and run:
   ```bash
   python manage.py migrate
   ```

5. **Stopping the Containers**
   
   To stop the running containers, use:
   ```bash
   docker-compose down
   ```

## Troubleshooting

- Ensure Docker and Docker Compose are installed and running.
- Verify that the `.env` file is correctly configured.
- Check the logs for any errors using:
  ```bash
  docker-compose logs
  ```

## Notes

- The `version` attribute in `docker-compose.yaml` is obsolete and can be removed to avoid warnings. 
