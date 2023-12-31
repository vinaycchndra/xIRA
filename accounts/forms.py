from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password',  }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'work_email', 'contact_number', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']= 'Enter Last Name'
        self.fields['work_email'].widget.attrs['placeholder']= 'Enter Work-Email'
        self.fields['contact_number'].widget.attrs['placeholder']= 'Enter Contact Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password!=confirm_password:
            raise forms.ValidationError(
                "Password does not match!."
            )


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'contact_number', 'work_profile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']= 'Enter Last Name'
        self.fields['contact_number'].widget.attrs['placeholder']= 'Enter Contact Number'
        self.fields['work_profile'].widget.attrs['placeholder'] = 'Work Profile'
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'