from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Animal, Owner, Breed, Species, UserProfile

class AnimalForm(forms.ModelForm):
    # Форма для создания/редактирования животного (для приёмщика)
    class Meta:
        model = Animal
        fields = ['name', 'breed', 'age', 'gender', 'owner', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите кличку'}),
            'breed': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Возраст в месяцах'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class AnimalAdoptForm(forms.ModelForm):
    # Форма для отдачи животного (только поле владелец и статус)
    class Meta:
        model = Animal
        fields = ['owner', 'status']
        widgets = {
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BreedForm(forms.ModelForm):
    class Meta:
        model = Breed
        fields = ['name', 'species']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'species': forms.Select(attrs={'class': 'form-control'}),
        }

class SpeciesForm(forms.ModelForm):
    class Meta:
        model = Species
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RegistrationForm(UserCreationForm):
    # Форма регистрации нового пользователя
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = user.profile
            profile.role = self.cleaned_data['role']
            profile.phone = self.cleaned_data['phone']
            profile.save()
        return user