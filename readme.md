### Containerizing the Movie Shop Application with Docker

In this guide, we will walk through the process of containerizing a FastAPI application and PostgreSQL database using Docker. The process involves creating a custom Docker network, attaching volumes, configuring environment variables, and connecting both the application and the database containers.

---

### Step 1: Create a Docker Network

We'll start by creating a Docker bridge network that allows containers to communicate with each other within a predefined IP range.

```bash
docker network create -d "bridge" --subnet "192.168.0.0/24" movie_net
```

- `-d "bridge"`: This flag specifies the type of network driver to use. In this case, we choose a `bridge` network.
- `--subnet "192.168.0.0/24"`: This defines the IP address range for the network.

![image](images/1.png)

---

### Step 2: Create a Docker Volume

Next, we create a Docker volume to persist PostgreSQL data. The volume ensures that database data is not lost when the container stops or is removed.

```bash
docker volume create my-volume
```

- `my-volume`: The name of the volume that will be used to store the database data.

---

### Step 3: Launch the PostgreSQL Container

Now, let's launch a PostgreSQL container and attach the volume for data persistence, along with the network created earlier. We will also define environment variables for PostgreSQL user credentials and the database name.

```bash
docker container run -d --name "moviedb" \
-v my-volume:/var/lib/postgresql/data \
--network movie_net \
-e "POSTGRES_PASSWORD=password" \
-e "POSTGRES_USER=user" \
-e "POSTGRES_DB=movieshop" \
postgres:17
```

- `-d`: Runs the container in detached mode (in the background).
- `--name "moviedb"`: The name of the container is set to `moviedb`.
- `-v my-volume:/var/lib/postgresql/data`: This mounts the `my-volume` to the PostgreSQL data directory, ensuring persistent storage.
- `--network movie_net`: Attaches the container to the previously created network `movie_net`.
- `-e POSTGRES_PASSWORD=password`: Sets the password for the PostgreSQL user.
- `-e POSTGRES_USER=user`: Sets the username for PostgreSQL.
- `-e POSTGRES_DB=movieshop`: Creates a PostgreSQL database named `movieshop`.
- `postgres:17`: Specifies the PostgreSQL image version (17) to use.

![image](images/2.png)



---

### Step 4: Create the Dockerfile for the FastAPI Application

We now need to containerize the FastAPI application by writing a `Dockerfile`. This `Dockerfile` will specify the steps to build the container image.

Create a file named `Dockerfile` in the root of your FastAPI application folder, and add the following content:

```Dockerfile
# Use the official Python image as the base image
FROM python:3.11

# Set the working directory inside the container to /app
WORKDIR /app

# Set an environment variable for the database connection
ENV DATABASE_URL=postgresql://user:password@localhost:5432/movieshop

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the FastAPI application code into the container
COPY . .

# Expose the port that the FastAPI application will use (8000)
EXPOSE 8000

# Command to start the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- `FROM python:3.11`: Specifies the base image as Python 3.11.
- `WORKDIR /app`: Sets `/app` as the working directory inside the container.
- `ENV DATABASE_URL=postgresql://user:password@localhost:5432/movieshop`: Defines the environment variable to configure the connection to PostgreSQL.
- `COPY requirements.txt .`: Copies the `requirements.txt` file into the container.
- `RUN pip install --no-cache-dir --upgrade -r requirements.txt`: Installs the Python dependencies from `requirements.txt`.
- `COPY . .`: Copies the rest of the FastAPI application code into the container.
- `EXPOSE 8000`: Exposes port `8000`, which FastAPI will use.
- `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`: Starts the FastAPI application using the Uvicorn server.

---

### Step 5: Build the FastAPI Application Docker Image

Once the `Dockerfile` is ready, navigate to the FastAPI application directory and build the Docker image using the following command:

```bash
docker build -t movieapp:1 .
```

- `-t movieapp:1`: Tags the image as `movieapp` with version `1`.

![image](images/3.png)


---

### Step 6: Run the FastAPI Application Container

After building the image, it's time to run the FastAPI container. We will connect it to the same Docker network as the PostgreSQL container (`movie_net`) and pass the correct database connection string as an environment variable.

```bash
docker run -d \
--name movieapp1 \
--network movie_net \
-P \
-e DATABASE_URL=postgresql://user:password@moviedb:5432/movieshop \
movieapp:1
```

- `--name movieapp1`: Names the container `movieapp1`.
- `--network movie_net`: Attaches the container to the same network as the database, enabling communication between them.
- `-P`: Automatically maps the exposed container port to an available host port.
- `-e DATABASE_URL=postgresql://user:password@moviedb:5432/movieshop`: Sets the database connection URL, where `moviedb` is the name of the PostgreSQL container. This allows the FastAPI container to communicate with the PostgreSQL database.
![image](images/4.png)
![image](images/5.png)



---

### Step 7: Verify the Database Connection

To verify that the FastAPI application is correctly connected to the PostgreSQL database, you can enter the PostgreSQL container and inspect the `movieshop` database.

1. Access the PostgreSQL container using the following command:

```bash
docker exec -it moviedb psql -U user -d movieshop
```

- `-it`: Opens an interactive terminal.
- `psql -U user -d movieshop`: Connects to the PostgreSQL database `movieshop` using the `user` account.

2. Inside the PostgreSQL interactive shell, run the following SQL query to retrieve all records from the `movies` table:

```sql
SELECT * FROM movies;
```

This will display the movie data stored in the `movieshop` database.

![image](images/6.png)

---

By following these steps, you will have a fully containerized FastAPI application with a PostgreSQL database, connected through Docker's bridge network. You can manage the application and database independently while ensuring persistence with Docker volumes.