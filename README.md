# 🚀 Silkway Global Backend

<div align="center">

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)

</div>

## 📋 Prerequisites

- 🐳 Docker
- 🔄 Docker Compose

## 🔧 Setup Instructions

### 1. **Clone the Repository**
   ```bash
   git clone https://github.com/Silkway-Global/Back-end.git
   cd BACK-END
   ```

### 2. **Environment Variables** ⚙️
   
   Ensure the `.env` file is correctly set up in the `static` directory with the following variables:
   ```env
   DB_NAME=silkwayglobal
   DB_USER=postgres
   DB_PASSWORD=@Grandtalim1
   DB_HOST=db
   DB_PORT=5432
   ```

### 3. **Build and Run the Containers** 🏗️
   
   Navigate to the `static` directory and run:
   ```bash
   docker-compose up --build
   ```
   
   This will build the Docker images and start the containers.

### 4. **Access the Application** 🌐
   
   The application will be accessible at `http://localhost:8000`. 

   > **⚠️ Important:** Manual Migration Required
   > 
   > To apply database migrations, go to Docker → `static-web-1` container → `EXEC` and run:
   > ```bash
   > python manage.py migrate
   > ```

### 5. **Stopping the Containers** 🛑
   
   To stop the running containers, use:
   ```bash
   docker-compose down
   ```

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| Docker not running | Ensure Docker and Docker Compose are installed and running |
| Environment issues | Verify that the `.env` file is correctly configured |
| Container errors | Check the logs using: `docker-compose logs` |

## 📝 Notes

- The `version` attribute in `docker-compose.yaml` is obsolete and can be removed to avoid warnings.
