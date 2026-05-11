from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Animal, Owner, Breed, Species, UserProfile
from .forms import AnimalForm, AnimalAdoptForm, OwnerForm, BreedForm, SpeciesForm, RegistrationForm

class ReceiverRequiredMixin(UserPassesTestMixin):
    # Только для приёмщика
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.role == 'receiver'

class GiverRequiredMixin(UserPassesTestMixin):
    # Только для отдающего
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.role == 'giver'

# РЕГИСТРАЦИЯ И ВХОД
class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        if self.request.user.profile.role == 'receiver':
            return reverse_lazy('animal_list')
        return reverse_lazy('animal_list_for_giver')

class AnimalListView(LoginRequiredMixin, ReceiverRequiredMixin, ListView):
    model = Animal
    template_name = 'animals/animal_list.html'
    context_object_name = 'animals'

class AnimalListForGiverView(LoginRequiredMixin, GiverRequiredMixin, ListView):
    # Список животных для отдающего - показывает доступных и забронированных
    model = Animal
    template_name = 'animals/animal_list_giver.html'
    context_object_name = 'animals'

    def get_queryset(self):
        # Показываем животных с определенными статусами
        return Animal.objects.filter(status__in=['available', 'reserved'])

class AnimalDetailView(LoginRequiredMixin, DetailView):
    model = Animal
    template_name = 'animals/animal_detail.html'
    context_object_name = 'animal'

class AnimalCreateView(LoginRequiredMixin, ReceiverRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/animal_form.html'
    success_url = reverse_lazy('animal_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AnimalUpdateView(LoginRequiredMixin, ReceiverRequiredMixin, UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/animal_form.html'
    success_url = reverse_lazy('animal_list')

class AnimalAdoptView(LoginRequiredMixin, GiverRequiredMixin, UpdateView):
    model = Animal
    form_class = AnimalAdoptForm
    template_name = 'animals/animal_adopt_form.html'
    success_url = reverse_lazy('animal_list_for_giver')

    def form_valid(self, form):
        form.instance.adopted_by = self.request.user
        return super().form_valid(form)

class AnimalDeleteView(LoginRequiredMixin, ReceiverRequiredMixin, DeleteView):
    model = Animal
    template_name = 'animals/animal_confirm_delete.html'
    success_url = reverse_lazy('animal_list')

class BreedListView(LoginRequiredMixin, ReceiverRequiredMixin, ListView):
    model = Breed
    template_name = 'animals/breed_list.html'
    context_object_name = 'breeds'

class BreedCreateView(LoginRequiredMixin, ReceiverRequiredMixin, CreateView):
    model = Breed
    form_class = BreedForm
    template_name = 'animals/breed_form.html'
    success_url = reverse_lazy('breed_list')

class BreedUpdateView(LoginRequiredMixin, ReceiverRequiredMixin, UpdateView):
    model = Breed
    form_class = BreedForm
    template_name = 'animals/breed_form.html'
    success_url = reverse_lazy('breed_list')

class BreedDeleteView(LoginRequiredMixin, ReceiverRequiredMixin, DeleteView):
    model = Breed
    template_name = 'animals/breed_confirm_delete.html'
    success_url = reverse_lazy('breed_list')

class SpeciesListView(LoginRequiredMixin, ReceiverRequiredMixin, ListView):
    model = Species
    template_name = 'animals/species_list.html'
    context_object_name = 'species'

class SpeciesCreateView(LoginRequiredMixin, ReceiverRequiredMixin, CreateView):
    model = Species
    form_class = SpeciesForm
    template_name = 'animals/species_form.html'
    success_url = reverse_lazy('species_list')

class SpeciesUpdateView(LoginRequiredMixin, ReceiverRequiredMixin, UpdateView):
    model = Species
    form_class = SpeciesForm
    template_name = 'animals/species_form.html'
    success_url = reverse_lazy('species_list')

class SpeciesDeleteView(LoginRequiredMixin, ReceiverRequiredMixin, DeleteView):
    model = Species
    template_name = 'animals/species_confirm_delete.html'
    success_url = reverse_lazy('species_list')

class OwnerListView(LoginRequiredMixin, ListView):
    model = Owner
    template_name = 'animals/owner_list.html'
    context_object_name = 'owners'

class OwnerCreateView(LoginRequiredMixin, CreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'animals/owner_form.html'
    success_url = reverse_lazy('owner_list')

class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'animals/owner_form.html'
    success_url = reverse_lazy('owner_list')

class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    model = Owner
    template_name = 'animals/owner_confirm_delete.html'
    success_url = reverse_lazy('owner_list')