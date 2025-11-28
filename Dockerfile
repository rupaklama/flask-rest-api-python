FROM python:3.12

# Set the port number the container should expose
# Flask will listen on port 5000 inside the container
EXPOSE 5000

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# run flask app
CMD ["flask", "run", "--host=0.0.0.0"]

# To build the Docker image once, use the following command and it will build in watch mode after that:
# It will map the current local directory to /app in the container
# docker run -dp 5001:5000 -w /app -v "$(pwd):/app" flask-web
