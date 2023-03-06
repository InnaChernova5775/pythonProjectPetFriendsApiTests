from api import PetFriends
from settings import valid_email, valid_password


class TestPetFriends:
    def setup(self):
        self.pf = PetFriends()

    def test_get_api_key_for_valid_user(self, email=valid_email, password=valid_password):
        status, result = self.pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

    def test_get_all_pets(self, filters=""):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filters)
        assert status == 200
        assert len(result['pets']) > 0

    def test_post_add_new_pets_with_pet_photo(self, name='Бимбо', animal_type='лабрадор', age='2', pet_photo='images/Bimbo.jpg'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    def test_successful_deletion_pet_with_valid_pet_id(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, filter="my_pets")

        if len(myPets['pets']) == 0:
            self.pf.add_new_pet(auth_key, name='Бимбо', animal_type='лабрадор', age='2', pet_photo='images/Bimbo.jpg')
            _, myPets = self.pf.get_list_of_pets(auth_key, filter="my_pets")
        pet_id = myPets['pets'][0]['id']
        status, result = self.pf.delete_pet(auth_key, pet_id)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in myPets.values()

    def test_successful_update_info_pet(self, name='Ричи', animal_type='сенбернар', age='3'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, filter="my_pets")

        if len(myPets['pets']) > 0:
            status, result = self.pf.update_info_pet(auth_key, myPets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        elif len(myPets['pets']) == 0:
            self.pf.add_new_pet(auth_key, name='Бимбо', animal_type='лабрадор', age='2', pet_photo='images/Bimbo.jpg')
            _, myPets = self.pf.get_list_of_pets(auth_key, filter="my_pets")
            status, result = self.pf.update_info_pet(auth_key, myPets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")


    def test_create_new_pets_without_photo(self, name='Матроскин', animal_type='кот', age=4):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.greate_pet_simple(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

    def test_add_pet_photo_for_pet_id(self, pet_photo='images/Cat.jpg'):

        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pet = self.pf.greate_pet_simple(auth_key, name='Севастьян', animal_type='кот', age=3)
        _, myPets = self.pf.get_list_of_pets(auth_key, filter="my_pets")
        pet_id = myPets['pets'][0]['id']
        status, result = self.pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
        assert status == 200

    def test_multytest(self, name='Бимбо', animal_type='лабрадор', age='2', pet_photo='images/Bimbo.jpg'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name
        print(result)

        _, myPets = self.pf.get_list_of_pets(auth_key, filter="my_pets")
        status, result = self.pf.update_info_pet(auth_key, myPets['pets'][0]['id'], name='Айрис',
                                                 animal_type='сенбернар', age='1')
        assert status == 200
        assert result['name'] == 'Айрис'
        print(result)

        status, result = self.pf.delete_pet(auth_key, myPets['pets'][0]['id'])
        assert status == 200
        assert myPets['pets'][0]['id'] not in myPets.values()
        print(result)

        status, result = self.pf.greate_pet_simple(auth_key, name='Мартин', animal_type='золотистый ретривер', age=2)
        assert status == 200
        assert result['name'] == 'Мартин'
        print(result)

        _, MyPets = self.pf.get_list_of_pets(auth_key, filter="my_pets")
        status, result = self.pf.add_photo_of_pet(auth_key, MyPets['pets'][0]['id'], 'images/Dog.jpg')
        assert status == 200
        print(result)

    def test_get_api_key_for_invalid_email(self, email='1234', password=valid_password):
        status, result = self.pf.get_api_key(email, password)
        assert status == 403

    def test_get_api_key_for_invalid_email2(self, email='', password=valid_password):
        status, result = self.pf.get_api_key(email, password)
        assert status == 403

    def test_get_api_key_for_invalid_password(self, email=valid_email, password='0123'):
        status, result = self.pf.get_api_key(email, password)
        assert status == 403

    def test_get_api_key_for_invalid_password2(self, email=valid_email, password=''):
        status, result = self.pf.get_api_key(email, password)
        assert status == 403

    def test_create_new_pets_with_invalid_age(self, name='Матроскин', animal_type='кот', age=2000):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.greate_pet_simple(auth_key, name, animal_type, age)
        assert status == 400
        #БАГ!!! ожидаемый ответ статус:400, получаем актуальный статус:200. Новый питомец с данными
        # параметрами появляется на сайте

    def test_create_new_pets_with_invalid_type_name(self, name='', animal_type='кот', age=4):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.greate_pet_simple(auth_key, name, animal_type, age)
        assert status == 400
        #БАГ!!! ожидаемый ответ статус:400, получаем актуальный статус:200. Новый питомец с данными
        # параметрами появляется на сайте

    def test_create_new_pets_with_invalid_type_name2(self, name= '@@@@@$$$$', animal_type='кот', age=4):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.greate_pet_simple(auth_key, name, animal_type, age)
        assert status == 400
        #БАГ!!! ожидаемый ответ статус:400, получаем актуальный статус:200. Новый питомец с данными
        # параметрами появляется на сайте

    def test_create_new_pets_with_invalid_type_animal_type(self, name='Феликс', animal_type='',age=4):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.greate_pet_simple(auth_key, name, animal_type, age)
        assert status == 400
        # #БАГ!!!ожидаемый ответ: статус:400, получаем актуальный статус:200. Новый питомец с данными
        # параметрами появляется на сайте

