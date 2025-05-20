# ###     pytest app/tests/test_create_master_profile.py

# from fastapi.testclient import TestClient
# from app.main import app
# from app.database import SessionLocal
# from app import models, schemas
# import pytest

# client = TestClient(app)


# @pytest.fixture(scope="module")
# def clean_db():
#     db = SessionLocal()
#     db.query(models.User).delete()
#     db.query(models.MasterProfile).delete()
#     db.commit()
#     yield db
#     db.close()


# @pytest.fixture
# def create_master_profile(clean_db):
#     db = clean_db

#     user_data = {
#         'email' : 'test@example.com',
#         'hashed_password' : 'hashed_password',
#         'role' : 'master'
#     }

#     test_user = models.User(**user_data)
#     db.add(test_user)
#     db.commit()
#     db.refresh(test_user)

#     profile_data = {
#         'user_id' : test_user.id,
#         'specialization' : 'Электрик',
#         'description' : 'Мастер, 5 лет'
#     }

#     response = client.post('/masters/create_profile', json=profile_data)
#     return response



# def test_create_master_profile(create_master_profile):
#     response = create_master_profile
#     assert response.status_code == 200
#     assert response.json()['message'] == "Профиль мастера успешно создан"
