import pytest
from rest_framework.test import APIClient
from pereval.models import PerevalAreas
from pereval.services.submit_data_service import SubmitDataService

@pytest.mark.django_db
def test_filter_perevals_by_user_email():
    client = APIClient()

    area = PerevalAreas.objects.create(id_parent=0, title="Регион A")

    user_data_1 = {
        "email": "user1@example.com",
        "phone": "+79000000001",
        "last_name": "Перевалов",
        "first_name": "Илья",
        "patronymic": "Сергеевич"
    }

    user_data_2 = {
        "email": "user2@example.com",
        "phone": "+79000000002",
        "last_name": "Горный",
        "first_name": "Анна",
        "patronymic": "Петровна"
    }

    coords = {
        "latitude": 50.0,
        "longitude": 60.0,
        "height": 1000
    }

    pereval_data = {
        "beautytitle": "перевал",
        "title": "Двойной тест",
        "other_titles": "",
        "connect": "тест",
        "area": area,  # ✅ объект
        "winter_level": "1A",
        "summer_level": "1A",
        "autumn_level": "1A",
        "spring_level": "1A"
    }

    user1 = SubmitDataService.get_or_create_user(user_data_1)
    coords1 = SubmitDataService.create_coords(coords)
    SubmitDataService.create_pereval(pereval_data, user1, coords1)

    user2 = SubmitDataService.get_or_create_user(user_data_2)
    coords2 = SubmitDataService.create_coords(coords)
    SubmitDataService.create_pereval(pereval_data, user2, coords2)

    response = client.get("/api/submitData/user/?user__email=user1@example.com")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["user"]["email"] == "user1@example.com"
