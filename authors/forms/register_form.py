from utils.django_forms import add_attr, add_placeholder, strong_password
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your email')
        add_placeholder(self.fields['first_name'], 'Ex: Jhonathan')
        add_placeholder(self.fields['last_name'], 'Ex: Harker')
        add_attr(self.fields['username'], 'css', 'a-css-class')

    username = forms.CharField(
        label='Username',
        help_text=(
            'Username must have letters, numbers or one of those @/./+/-/_. '
            'the length should be between 4 and 150 characters'),
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least for characters',
            'max_length': 'Username must have less than 150 characters',
            },
        min_length=4, max_length=150
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='First Name'
        )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last Name'
        )

    email = forms.EmailField(
        error_messages={'required': 'Email is required'},
        help_text='E-mail must be valid',
        label='E-mail'
        )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one numbere. The length should be at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password'

    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
        label='Password',
        error_messages={
            'required': 'Please repeat your password'
        }
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(
                'User e-mail is alredy in use', code='invalid'
            )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:

            password_confirmation_error = ValidationError('Password and password 2 must be equal')

            raise ValidationError({
                    'password': password_confirmation_error,
                    'password2': [
                        password_confirmation_error,
                    ],
                })
