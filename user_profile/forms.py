from django.forms import ModelForm, ValidationError, CharField
from django.contrib.auth.models import User


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']  


    email = CharField(
        disabled=True,
        help_text='Current email address'
    )

    first_name = CharField(
        help_text='Make sure you provide valid first name'
    )

    last_name = CharField(
        help_text='Make sure you provide valid last name'
    )

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if len(first_name) < 3:
            raise ValidationError('First name is too short', 'first_name')
        
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if len(last_name) < 3:
            raise ValidationError('Last name is too short', 'last_name')
        
        return last_name
        