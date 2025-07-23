import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from pereval.models import PerevalAreas
from pereval.services.submit_data_service import SubmitDataService

@pytest.mark.django_db
def test_full_pereval_flow():
    client = APIClient()

    area = PerevalAreas.objects.create(id_parent=0, title="Южный Урал")

    user_data = {
        "email": "alpine@test.com",
        "phone": "+79998887766",
        "last_name": "Горный",
        "first_name": "Леонид",
        "patronymic": "Алексеевич"
    }

    coords_data = {
        "latitude": 54.321,
        "longitude": 59.876,
        "height": 1230
    }

    pereval_data = {
        "beautytitle": "перевал",
        "title": "Тестовый хребет",
        "other_titles": "ТХ",
        "connect": "соединяет два ущелья",
        "area": area,  # ✅ объект, не ID
        "winter_level": "1A",
        "summer_level": "1B",
        "autumn_level": "1A",
        "spring_level": "2A"
    }

    image_file = SimpleUploadedFile("test.jpg", b"fake image", content_type="image/jpeg")
    images_data = [{
        "title": "пик",
        "file": image_file
    }]

    user = SubmitDataService.get_or_create_user(user_data)
    coords = SubmitDataService.create_coords(coords_data)
    pereval = SubmitDataService.create_pereval(pereval_data, user, coords)
    SubmitDataService.attach_images(pereval, images_data)

    get_response = client.get(f"/api/submitData/{pereval.id}/")
    assert get_response.status_code == 200
    retrieved = get_response.json()

    assert retrieved["title"] == pereval_data["title"]
    assert retrieved["user"]["email"] == user_data["email"]
    assert retrieved["coords"]["height"] == coords_data["height"]
    assert float(retrieved["coords"]["latitude"]) == coords_data["latitude"]
    assert float(retrieved["coords"]["longitude"]) == coords_data["longitude"]
    assert retrieved["status"] == "new"
    assert isinstance(retrieved["images"], list)

    patch_payload = {
        "title": "Обновлённый хребет",
        "connect": "соединяет две долины",
        "coords": {
            "latitude": 54.000,
            "longitude": 60.000,
            "height": 1250
        },
        "area": area.id,
        "spring_level": "1A",
        "summer_level": "2B",
        "autumn_level": "1B",
        "winter_level": "1A"
    }

    patch_response = client.patch(
        f"/api/submitData/{pereval.id}/edit/",
        patch_payload,
        format="json"
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["state"] == 1

    updated = client.get(f"/api/submitData/{pereval.id}/").json()

    assert updated["title"] == patch_payload["title"]
    assert updated["connect"] == patch_payload["connect"]
    assert updated["coords"]["height"] == patch_payload["coords"]["height"]
    assert float(updated["coords"]["latitude"]) == patch_payload["coords"]["latitude"]
    assert float(updated["coords"]["longitude"]) == patch_payload["coords"]["longitude"]
