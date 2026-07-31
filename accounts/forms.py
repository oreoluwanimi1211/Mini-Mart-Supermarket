from django import forms
from .models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': "Enter Password",
    'class': 'form-control',

    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Confirm Password",
        'class': 'form-control',
    }))

    class Meta:
        model = CustomUser
        fields = ['name','username', 'email', 'phone_number', 'password']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Enter Full Name'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    # def clean(self):
    #     cleaned_data = super(UserRegistrationForm, self).clean()
    #     password = cleaned_data.get('password')
    #     confirm_password = cleaned_data.get('confirm_password')


    #     if password != confirm_password:
    #         raise forms.ValidationError('password does not match!')
