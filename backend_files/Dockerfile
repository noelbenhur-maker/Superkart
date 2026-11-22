FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy dependency list and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files (app.py and superkart_model.joblib)
COPY . .

# Expose port 7860 to receive requests
EXPOSE 7860

# Run the application using Python
CMD ["python", "app.py"]
