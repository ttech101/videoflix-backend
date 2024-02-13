from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user creation.
    This form extends the built-in UserCreationForm to include an email field.
    Meta Attributes:
        model (User): The model associated with this form.
        fields (tuple): The fields to include in the form.
    """
    email = forms.EmailField()

    class Meta:

        model = User
        fields = ('username', 'email' , 'password1', 'password2','first_name')