import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            (
                'Password must have at least one uppercase letter, '
                'one lowercase letter and one numbere. The length should be at least 8 characters.'
            ),
            code='Invalid'
            )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your email')
        add_placeholder(self.fields['first_name'], 'Ex: Jhonathan')
        add_placeholder(self.fields['last_name'], 'Ex: Harker')
        add_attr(self.fields['username'], 'css', 'a-css-class')

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

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password'
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }

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
