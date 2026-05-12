from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Species, Breed, Owner, Animal, UserProfile

class ModelsTest(TestCase):
    def test_create_species(self):
        species = Species.objects.create(name="Собака")
        self.assertEqual(species.name, "Собака")
    
    def test_create_breed(self):
        species = Species.objects.create(name="Кошка")
        breed = Breed.objects.create(name="Сиамская", species=species)
        self.assertEqual(breed.name, "Сиамская")
    
    def test_create_owner(self):
        owner = Owner.objects.create(
            first_name="Иван",
            last_name="Петров",
            phone="+79991234567"
        )
        self.assertEqual(owner.first_name, "Иван")
    
    def test_create_animal(self):
        species = Species.objects.create(name="Собака")
        breed = Breed.objects.create(name="Лабрадор", species=species)
        user = User.objects.create_user(username="test", password="123")
        animal = Animal.objects.create(
            name="Бобик",
            breed=breed,
            age=12,
            gender="M",
            status="available",
            created_by=user
        )
        self.assertEqual(animal.name, "Бобик")

class ViewsTest(TestCase):
    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
