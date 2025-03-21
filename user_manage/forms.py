from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserModel

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password']