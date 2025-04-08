from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
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
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
        # Данные для нового пользователя
    new_user = {
        "name": "Test User",
        "email": "unique@example.com"  # Уникальный email
    }

    # Создаем пользователя
    response = client.post(BASE_URL, json=new_user)

    # Проверяем успешное создание (201 код)
    assert response.status_code == status.HTTP_201_CREATED
    # Проверяем что вернулся ID (число)
    assert isinstance(response.json(), int)

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    # Сначала создаем пользователя
    existing_user = {
        "name": "Existing User",
        "email": "exists@example.com"
    }
    client.post(BASE_URL, json=existing_user)

    # Пытаемся создать пользователя с таким же email
    duplicate_user = {
        "name": "Duplicate User",
        "email": "exists@example.com"  # Такой же email
    }
    response = client.post(BASE_URL, json=duplicate_user)

    # Проверяем конфликт (409 код)
    assert response.status_code == status.HTTP_409_CONFLICT
    # Проверяем текст ошибки
    assert response.json() == {"detail": "User with this email already exists"}


def test_delete_user():
    '''Удаление пользователя'''
     # Сначала создаем пользователя для удаления
    user_to_delete = {
        "name": "User To Delete",
        "email": "delete@example.com"
    }
    create_response = client.post(BASE_URL, json=user_to_delete)
    user_id = create_response.json()

    # Удаляем пользователя
    delete_response = client.delete(BASE_URL, params={"email": "delete@example.com"})

    # Проверяем успешное удаление (204 код)
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Проверяем что пользователь действительно удален
    get_response = client.get(BASE_URL, params={"email": "delete@example.com"})
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
