from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Главные страницы
    path('', views.AnimalListView.as_view(), name='animal_list'),
    path('for-giver/', views.AnimalListForGiverView.as_view(), name='animal_list_for_giver'),

    # CRUD для животных
    path('<int:pk>/', views.AnimalDetailView.as_view(), name='animal_detail'),
    path('create/', views.AnimalCreateView.as_view(), name='animal_create'),
    path('<int:pk>/update/', views.AnimalUpdateView.as_view(), name='animal_update'),
    path('<int:pk>/adopt/', views.AnimalAdoptView.as_view(), name='animal_adopt'),
    path('<int:pk>/delete/', views.AnimalDeleteView.as_view(), name='animal_delete'),

    # Регистрация и аутентификация
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Управление породами
    path('breeds/', views.BreedListView.as_view(), name='breed_list'),
    path('breeds/create/', views.BreedCreateView.as_view(), name='breed_create'),
    path('breeds/<int:pk>/update/', views.BreedUpdateView.as_view(), name='breed_update'),
    path('breeds/<int:pk>/delete/', views.BreedDeleteView.as_view(), name='breed_delete'),

    # Управление видами
    path('species/', views.SpeciesListView.as_view(), name='species_list'),
    path('species/create/', views.SpeciesCreateView.as_view(), name='species_create'),
    path('species/<int:pk>/update/', views.SpeciesUpdateView.as_view(), name='species_update'),
    path('species/<int:pk>/delete/', views.SpeciesDeleteView.as_view(), name='species_delete'),

    # Управление владельцами
    path('owners/', views.OwnerListView.as_view(), name='owner_list'),
    path('owners/create/', views.OwnerCreateView.as_view(), name='owner_create'),
    path('owners/<int:pk>/update/', views.OwnerUpdateView.as_view(), name='owner_update'),
    path('owners/<int:pk>/delete/', views.OwnerDeleteView.as_view(), name='owner_delete'),
]