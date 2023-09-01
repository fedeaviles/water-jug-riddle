# stdlib
import json
from unittest.mock import patch

# local
from app.main.routes import bfs


@patch("app.main.routes.bfs")
def test_index_post_with_solution(mock_bfs, client):
    """
    Test the POST request to the index page with a solution.
    """
    # Arrange
    mock_bfs.return_value = [
        {"x_state": "Empty", "y_state": "Empty", "action": "Start"}
    ]

    # Act
    response = client.post("/", data={"x": 3, "y": 4, "z": 2})

    # Assert
    assert response.status_code == 200
    assert b"Solution" in response.data


@patch("app.main.routes.bfs")
def test_index_post_with_no_solution(mock_bfs, client):
    """
    Test the POST request to the index page with no solution.
    """
    # Arrange
    mock_bfs.return_value = None

    # Act
    response = client.post("/", data={"x": 3, "y": 4, "z": 2})

    # Assert
    assert response.status_code == 200
    assert b"No solution" in response.data


@patch("app.main.routes.bfs")
def test_index_post_with_invalid_input(mock_bfs, client):
    """
    Test the POST request to the index page with invalid input.
    """
    # Arrange
    mock_bfs.return_value = None
    data = {"x": "invalid", "y": 4, "z": 2}

    # Act
    response = client.post("/", data=data)

    # Assert
    assert response.status_code == 200
    assert b"Invalid input" in response.data


def test_index_get(client):
    """
    Test the GET request to the index page.
    """
    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert b"X-gallon jug" in response.data
    assert b"Y-gallon jug" in response.data
    assert b"Z gallons to measure" in response.data


@patch("app.main.routes.bfs")
def test_api_with_valid_input(mock_bfs, client):
    """
    Test the API endpoint with valid input.
    """
    # Arrange
    mock_bfs.return_value = [
        {"x_state": "Empty", "y_state": "Empty", "action": "Start"}
    ]
    data = {"x": 3, "y": 4, "z": 2}

    # Act
    response = client.post(
        "/api/", data=json.dumps(data), content_type="application/json"
    )

    # Assert
    assert response.status_code == 200
    assert response.get_json() == mock_bfs.return_value


def test_api_missing_required_parameters(client):
    """
    Test the API endpoint with missing required parameters.
    """
    # Arrange
    data = {"y": 4, "z": 2}  # Missing 'x'

    # Act
    response = client.post(
        "/api/", data=json.dumps(data), content_type="application/json"
    )

    # Assert
    assert response.status_code == 400
    assert response.get_json() == {"message": "Missing required parameters"}


def test_api_with_invalid_input(client):
    """
    Test the API endpoint with invalid input.
    """
    # Arrange
    data = {"x": "invalid", "y": 4, "z": 2}

    # Act
    response = client.post(
        "/api/", data=json.dumps(data), content_type="application/json"
    )

    # Assert
    assert response.status_code == 400
    assert response.get_json() == {"message": "Invalid input"}


@patch("app.main.routes.bfs")
def test_api_with_no_solution(mock_bfs, client):
    """
    Test the API endpoint with valid input but no solution.
    """
    # Arrange
    mock_bfs.return_value = None
    data = {"x": 3, "y": 4, "z": 2}

    # Act
    response = client.post(
        "/api/", data=json.dumps(data), content_type="application/json"
    )

    # Assert
    assert response.status_code == 200
    assert response.get_json() == {"message": "No solution"}


def test_valid_solution():
    """
    Test a valid solution using the bfs function.
    """
    # Act
    solution = bfs(4, 3, 2)

    # Assert
    assert solution is not None


def test_no_solution():
    """
    Test a case with no solution using the bfs function.
    """
    # Act
    solution = bfs(5, 7, 9)

    # Assert
    assert solution is None
