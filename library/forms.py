from django import forms
from .models import Material, Review, UserProfile
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'description', 'category', 'file', 'author', 'release_date']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your review here...'
            }),
        }

class SimpleUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="Your password can be anything you like."
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    picture = forms.ImageField(
        required=False,
        label="Profile Picture",
        help_text="Upload a profile picture (optional)",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'id': 'id_picture'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['picture', 'bio', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'id': 'id_bio',
                'placeholder': 'Write something about yourself'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'id_birth_date'
            }),
        }

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field_name].label
            })
