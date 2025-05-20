from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)


@pytest.fixture(params=[
    ({'name': 'kirill', 'email': 'abs222@mail.ru', 'password': 'qwerty', 'role': 'client'}, 200), 

    ({'name': 'ivan', 'email': 'ivanRmail.ru', 'password': 'ivan123', 'role': 'master'}, 422),  # Ошибка валидации email

    ({'name': 'igor', 'email': 'igor@example.com', 'password': None, 'role': 'client'}, 422),  # Ошибка, так как пароль пустой

    ({'name': None, 'email': 'exmp@mail.ru', 'password': 'mypass1', 'role': 'master'}, 422),  # Ошибка из-за пустого имени
])
def registration_case(request):
    return request.param

def test_register_user_fixture(registration_case):
    payload, expected_status = registration_case
    response = client.post('/register', json=payload)
    assert response.status_code == expected_status