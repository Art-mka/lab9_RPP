from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Species, Breed, Owner, Animal, UserProfile

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'species')
    list_filter = ('species',)
    search_fields = ('name',)

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'phone')
    search_fields = ('last_name', 'first_name', 'phone')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'breed', 'age', 'gender', 'status', 'owner')
    list_filter = ('breed', 'gender', 'status')
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    list_filter = ('role',)
    search_fields = ('user__username',)

# Расширяем стандартный UserAdmin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_role', 'is_staff')

    def get_role(self, obj):
        return obj.profile.get_role_display()

    get_role.short_description = 'Роль'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)