# Use the official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright with all required dependencies
RUN playwright install --with-deps

# Copy the entire project into the container
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Command to start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]