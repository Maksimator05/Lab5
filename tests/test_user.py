from fastapi import status
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
BASE_URL = "/api/v1/user"  # Общий endpoint для всех тестов

# Тестовые данные
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get(BASE_URL, params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get(BASE_URL, params={"email": "nonexistent@example.com"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        "name": "Test User",
        "email": "unique@example.com"
    }
    response = client.post(BASE_URL, json=new_user)
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.json(), int)

def test_create_user_with_invalid_email():
    '''Создание пользователя с существующей почтой'''
    existing_user = {
        "name": "Existing User",
        "email": "exists@example.com"
    }
    client.post(BASE_URL, json=existing_user)
    
    duplicate_user = {
        "name": "Duplicate User",
        "email": "exists@example.com"
    }
    response = client.post(BASE_URL, json=duplicate_user)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    user_to_delete = {
        "name": "User To Delete",
        "email": "delete@example.com"
    }
    create_response = client.post(BASE_URL, json=user_to_delete)
    user_id = create_response.json()

    delete_response = client.delete(BASE_URL, params={"email": "delete@example.com"})
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(BASE_URL, params={"email": "delete@example.com"})
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
