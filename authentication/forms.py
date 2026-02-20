from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import django.forms as forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    username = forms.EmailField(
        label='Email',
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
            }
        )
    )

    password1 = forms.CharField(
        label='Passwd1',
        help_text='Passwd1 label text override',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password1',
            }
        )
    )

    password2 = forms.CharField(
        label='Passwd2',
        help_text='Passwd2 label text override 123456789000000000',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password1',
            }
        )
    )

    def clean_username(self):
        email = self.cleaned_data.get('username')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email
         