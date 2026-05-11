import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Species, Breed, Owner, Animal, UserProfile


class AnimalModelTest(TestCase):
    """Тесты для моделей с Django 6.0"""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных (Django 6.0 фича)"""
        cls.species = Species.objects.create(name='Собака')
        cls.breed = Breed.objects.create(name='Лабрадор', species=cls.species)
        cls.owner = Owner.objects.create(
            first_name='Иван',
            last_name='Петров',
            phone='+79991234567'
        )
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_species_creation(self):
        """Тест создания вида"""
        self.assertEqual(self.species.name, 'Собака')
        self.assertEqual(str(self.species), 'Собака')

    def test_breed_creation(self):
        """Тест создания породы"""
        self.assertEqual(self.breed.name, 'Лабрадор')
        self.assertEqual(self.breed.species, self.species)
        self.assertIn('Лабрадор', str(self.breed))

    def test_owner_creation(self):
        """Тест создания владельца"""
        self.assertEqual(self.owner.first_name, 'Иван')
        self.assertEqual(str(self.owner), 'Петров Иван')

    def test_animal_creation(self):
        """Тест создания животного"""
        animal = Animal.objects.create(
            name='Бобик',
            breed=self.breed,
            age=12,
            gender='M',
            owner=None,
            status='available',
            created_by=self.user
        )
        self.assertEqual(animal.name, 'Бобик')
        self.assertEqual(animal.status, 'available')
        self.assertEqual(animal.age, 12)
        self.assertIn('Бобик', str(animal))

    def test_animal_status_choices(self):
        """Тест валидности статусов"""
        valid_statuses = ['available', 'reserved', 'adopted']
        for status in valid_statuses:
            animal = Animal.objects.create(
                name=f'Test_{status}',
                breed=self.breed,
                age=6,
                gender='F',
                created_by=self.user,
                status=status
            )
            self.assertEqual(animal.status, status)

    def test_user_profile_auto_creation(self):
        """Тест автоматического создания профиля"""
        new_user = User.objects.create_user(
            username='newuser',
            password='pass123'
        )
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertEqual(new_user.profile.role, 'receiver')


class ViewAccessTest(TestCase):
    """Тесты доступа к страницам"""

    def setUp(self):
        self.client = Client()

        # Создание приемщика
        self.receiver_user = User.objects.create_user(
            username='receiver',
            password='testpass123'
        )
        self.receiver_user.profile.role = 'receiver'
        self.receiver_user.profile.save()

        # Создание отдающего
        self.giver_user = User.objects.create_user(
            username='giver',
            password='testpass123'
        )
        self.giver_user.profile.role = 'giver'
        self.giver_user.profile.save()

    def test_login_page_accessible(self):
        """Страница входа доступна"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_accessible(self):
        """Страница регистрации доступна"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_animal_list_requires_login(self):
        """Список животных требует авторизации"""
        response = self.client.get(reverse('animal_list'))
        # Должен быть редирект на страницу входа
        self.assertNotEqual(response.status_code, 200)

    def test_receiver_can_access_animal_list(self):
        """Приемщик имеет доступ к списку"""
        self.client.login(username='receiver', password='testpass123')
        response = self.client.get(reverse('animal_list'))
        self.assertEqual(response.status_code, 200)

    def test_giver_can_access_giver_list(self):
        """Отдающий имеет доступ к своему списку"""
        self.client.login(username='giver', password='testpass123')
        response = self.client.get(reverse('animal_list_for_giver'))
        self.assertEqual(response.status_code, 200)

    def test_giver_cannot_access_create_animal(self):
        """Отдающий не может создавать животных"""
        self.client.login(username='giver', password='testpass123')
        response = self.client.get(reverse('animal_create'))
        self.assertEqual(response.status_code, 403)


class AnimalCRUDTest(TestCase):
    """Тесты CRUD операций"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='receiver',
            password='testpass123'
        )
        self.user.profile.role = 'receiver'
        self.user.profile.save()

        self.species = Species.objects.create(name='Кошка')
        self.breed = Breed.objects.create(name='Сиамская', species=self.species)

    def test_animal_create_view(self):
        """Тест создания животного через view"""
        self.client.login(username='receiver', password='testpass123')
        response = self.client.post(reverse('animal_create'), {
            'name': 'Мурка',
            'breed': self.breed.id,
            'age': 6,
            'gender': 'F',
            'owner': '',
            'status': 'available'
        })
        # Должен быть редирект после успешного создания
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Animal.objects.count(), 1)
        animal = Animal.objects.first()
        self.assertEqual(animal.name, 'Мурка')
        self.assertEqual(animal.created_by, self.user)

    def test_animal_update_view(self):
        """Тест обновления животного"""
        self.client.login(username='receiver', password='testpass123')
        animal = Animal.objects.create(
            name='СтароеИмя',
            breed=self.breed,
            age=12,
            gender='M',
            created_by=self.user
        )
        response = self.client.post(
            reverse('animal_update', args=[animal.pk]),
            {
                'name': 'НовоеИмя',
                'breed': self.breed.id,
                'age': 24,
                'gender': 'M',
                'owner': '',
                'status': 'reserved'
            }
        )
        self.assertEqual(response.status_code, 302)
        animal.refresh_from_db()
        self.assertEqual(animal.name, 'НовоеИмя')
        self.assertEqual(animal.age, 24)

    def test_animal_delete_view(self):
        """Тест удаления животного"""
        self.client.login(username='receiver', password='testpass123')
        animal = Animal.objects.create(
            name='НаУдаление',
            breed=self.breed,
            age=3,
            gender='F',
            created_by=self.user
        )
        self.assertEqual(Animal.objects.count(), 1)
        response = self.client.post(reverse('animal_delete', args=[animal.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Animal.objects.count(), 0)