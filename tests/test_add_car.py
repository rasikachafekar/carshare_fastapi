from unittest import mock
from fastapi.testclient import TestClient
from routers.cars import add_car
from schemas import Car, CarInput, User
from carsharing import app

client = TestClient(app)

def test_add_car_with_db():
    """Testing with fastapi client"""
    response = client.post("/api/cars",
                           json={"doors":4, "size":"s"},
                           headers={"Authorization": "Bearer rasika"})
    assert response.status_code == 200
    car = response.json()
    assert car["doors"] == 4
    assert car["size"] == "s"


def test_add_car():
    """Testing with mocked DB session"""
    mock_session = mock.Mock()
    input = CarInput(doors=2, size="m")
    user = User(username="rasika")
    result = add_car(car_input=input, session=mock_session, user=user)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert isinstance(result, Car)
    assert result.doors == 2
    assert result.size == "m"
    