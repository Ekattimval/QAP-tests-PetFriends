from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result =pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name: str = 'Мася', animal_type: str ='лопоухий', age: str ='2', pet_photo: str ='images/cat_1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_pet_info(name='Масяня', animal_type='длинноухий', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_delete_my_all_pets():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    for i in range(len(my_pets['pets'])):
        pet_id = my_pets['pets'][i]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)

    try:
        assert status == 200
        assert pet_id not in my_pets.values()
    except:
        print(' status = ', status)
        print("There is no my pets")

def test_create_pet_without_photo(name = 'Жирик', animal_type ='жираф африканский', age ='10'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_get_api_key_for_non_valid_user(email='123hgf@gmail.com', password='459876j'):
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_all_pets_with_non_valid_key(filter = ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result =pf.get_list_of_pets(auth_key, filter)
    assert status == 400


def test_add_new_pet_with_non_valid_name_more_100_symbols(name=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_non_valid_name_more_100_symbols(auth_key, name)
    if len(name) > 100:
        status, result = pf.add_new_pet_with_non_valid_name_more_100_symbols(auth_key, name)
    assert status == 400

def test_add_new_pet_with_non_valid_name_more_100_symbols(age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_non_valid_age_more_100_symbols(auth_key, age)
    if len(age) > 100:
        status, result = pf.add_new_pet_with_non_valid_age_more_100_symbols(auth_key, age)
    assert status == 400