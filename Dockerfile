# FROM python:3.9-slim-buster

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# # CMD ["python", "app.py"]
# ENTRYPOINT [ "python" ]

# CMD [ "app.py" ]


FROM alpine:3.18

# Install Python 3 and necessary packages
RUN apk add --no-cache python3 python3-dev py3-pip

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN python3 -m venv venv && \
    source venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code to the container
COPY . .

# Expose the Flask application port
EXPOSE 5000

# Start the application using Gunicorn
CMD ["/app/venv/bin/gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

