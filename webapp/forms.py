from django import forms

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
