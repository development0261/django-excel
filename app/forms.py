from django import forms
from django.contrib.auth.models import User

class userform(forms.ModelForm):
    # required_css_class = 'required'
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(),required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(),label="Confirm Password")

    class Meta():
        model = User
        fields = ('username','password')

    def clean(self):
        cleaned_data = super(userform, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password2")
         
        if password != confirm_password:
             print(password)
             print(confirm_password)
             raise forms.ValidationError(
                 "passwords do not match"
             )
