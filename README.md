# Water Jug Riddle Flask App

This is a Flask web application that solves the water jug riddle.

## Prerequisites

Before you begin, make sure you have the following installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Git: [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/water-jug-riddle.git
    cd water-jug-riddle
    ```
2. Build the Docker image:

    ```bash
    docker build -t water-jug-riddle .
    ```
3. Run the Docker container:

    ```bash
    docker run -p 8000:8000 water-jug-riddle
    ```
4. Access the application:

    Open your web browser and go to: http://localhost:8000

## API Endpoint

You can also use the API endpoint to solve the water jug riddle. The API endpoint is available at:

http://localhost:8000/api/

You can send a JSON POST request with the following format:

```json
{
  "x": 3,
  "y": 4,
  "z": 2
}
```

The API will respond with a JSON object containing the solution steps, or a message indicating no solution.
