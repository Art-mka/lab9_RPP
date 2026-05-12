from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Species(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название вида")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вид"
        verbose_name_plural = "Виды"

class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название породы")
    species = models.ForeignKey(Species, on_delete=models.CASCADE, verbose_name="Вид")
    
    def __str__(self):
        return f"{self.name} ({self.species.name})"

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"

class Owner(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Владелец"
        verbose_name_plural = "Владельцы"

class Animal(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    STATUS_CHOICES = [
        ('available', 'Без владельца'),
        ('reserved', 'Забронирован'),
        ('adopted', 'Отдан'),
    ]

    name = models.CharField(max_length=100, verbose_name="Кличка")
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name="Порода")
    age = models.IntegerField(verbose_name="Возраст (месяцы)")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    owner = models.OneToOneField(
        Owner, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Владелец"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='available', 
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата поступления")
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Кто добавил"
    )
    adopted_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='adopted_animals', 
        verbose_name="Кто отдал в семью"
    )

    def __str__(self):
        return f"{self.name} ({self.breed.name})"

    class Meta:
        verbose_name = "Животное"
        verbose_name_plural = "Животные"
        permissions = [
            ("can_adopt_animal", "Может отдавать животных в семьи"),
            ("can_receive_animal", "Может принимать животных в приют"),
        ]

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('receiver', 'Приёмщик животных'),
        ('giver', 'Отдающий животных'),
    ]

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='receiver', 
        verbose_name="Роль"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
