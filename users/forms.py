from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django.forms import ModelForm, HiddenInput, EmailField, Form


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class ResetPasswordForm(Form):
    email = EmailField(label='Почтовый адрес')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = HiddenInput()
