FROM python:3.12

# Set the port number the container should expose
# Flask will listen on port 5000 inside the container
EXPOSE 5000

# Set the working directory in the container
WORKDIR /app

RUN pip install flask

# Copy the current directory contents into the container at /app
COPY . /app

# run flask app
CMD ["flask", "run", "--host=0.0.0.0"]

