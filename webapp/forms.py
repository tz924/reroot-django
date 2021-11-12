from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

EDUCATION_CHOICES = [
    (1, 'Highschool'),
    (2, 'Some college'),
    (3, 'College'),
    (4, 'Graduate'),
    (5, 'Professional'),
]


class NewQuestionnaireForm(forms.Form):
    education = forms.MultipleChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=EDUCATION_CHOICES,
    )


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserLogInForm(AuthenticationForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1")
