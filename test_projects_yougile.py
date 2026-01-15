import requests
import pytest

# Конфигурация
BASE_URL = "https://ru.yougile.com/api-v2"
API_KEY = "   "

# Заголовки для авторизации
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ==== POSITIVE TESTS ====

@pytest.mark.positive
@pytest.mark.create
def test_create_project_success():
    """Позитивный тест: создать проект с валидным названием"""
    url = f"{BASE_URL}/projects"
    data = {"title": "Мой первый проект"}
    
    response = requests.post(url, json=data, headers=headers)
    
    assert response.status_code == 201
    assert "id" in response.json()
    
@pytest.mark.positive
@pytest.mark.get
def test_get_project_success():
    """Позитивный тест: получить созданный проект"""
    # Создаю проект
    url = f"{BASE_URL}/projects"
    data = {"title": "Проект для получения"}
    response = requests.post(url, json=data, headers=headers)
    project_id = response.json()["id"]
    
    # Получаю его
    url = f"{BASE_URL}/projects/{project_id}"
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == project_id
    assert result["title"] == "Проект для получения"

@pytest.mark.positive
@pytest.mark.update
def test_update_project_success():
    """Позитивный тест: обновить название проекта"""
    # Создаю проект
    url = f"{BASE_URL}/projects"
    data = {"title": "Старое название"}
    response = requests.post(url, json=data, headers=headers)
    project_id = response.json()["id"]
    
    # Обновляю его
    url = f"{BASE_URL}/projects/{project_id}"
    data = {"title": "Новое название"}
    response = requests.put(url, json=data, headers=headers)
    
    assert response.status_code == 200
    
    # Проверяю что обновилось
    response = requests.get(url, headers=headers)
    assert response.json()["title"] == "Новое название"

# ==== NEGATIVE TESTS ====

@pytest.mark.negative
@pytest.mark.create
def test_create_project_without_auth():
    """Негативный тест: создать проект без авторизации"""
    url = f"{BASE_URL}/projects"
    data = {"title": "Проект без авторизации"}
    
    response = requests.post(url, json=data)  
    
    assert response.status_code == 401

@pytest.mark.negative
@pytest.mark.create
def test_create_project_empty_title():
    """Негативный тест: создать проект с пустым названием"""
    url = f"{BASE_URL}/projects"
    data = {"title": ""}
    
    response = requests.post(url, json=data, headers=headers)
    
    assert response.status_code == 400

@pytest.mark.negative
@pytest.mark.get
def test_get_nonexistent_project():
    """Негативный тест: получить несуществующий проект"""
    url = f"{BASE_URL}/projects/00000000-0000-0000-0000-000000000000"
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 404

@pytest.mark.negative
@pytest.mark.update
def test_update_nonexistent_project():
    """Негативный тест: обновить несуществующий проект"""
    url = f"{BASE_URL}/projects/00000000-0000-0000-0000-000000000000"
    data = {"title": "Новое название"}
    
    response = requests.put(url, json=data, headers=headers)
    
    assert response.status_code == 404

# ==== Проверка обязательных полей ====

@pytest.mark.negative
@pytest.mark.create
def test_create_project_missing_title():
    """Негативный тест: создать проект без поля title"""
    url = f"{BASE_URL}/projects"
    data = {}  # Нет поля title
    
    response = requests.post(url, json=data, headers=headers)
    
    assert response.status_code == 400