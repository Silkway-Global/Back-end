FROM python:3.11

# Set the working directory
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron

# Create log file for cron
RUN touch /var/log/cron.log

# Copy the rest of the application code
COPY . /code/

# Expose the port
EXPOSE 8000

# Command to run cron and the server
CMD ["cron", "-f", "&&", "python", "manage.py", "migrate", "&&", "python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["sh", "-c", "cron -f & python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
