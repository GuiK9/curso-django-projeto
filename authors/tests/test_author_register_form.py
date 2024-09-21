from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your email'),
        ('first_name', 'Ex: Jhonathan'),
        ('last_name', 'Ex: Harker'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder_test):
        form = RegisterForm()
        placeholder = form.fields[field].widget.attrs['placeholder']
        self.assertEqual(placeholder, placeholder_test)

    @parameterized.expand([
        ('email', 'E-mail must be valid'),
        ('username', 'Username must have letters, numbers or one of those @/./+/-/_. '
            'the length should be between 4 and 150 characters'),
        ('password', 'Password must have at least one uppercase letter, '
            'one lowercase letter and one numbere. The length should be at least 8 characters.'),
    ])
    def test_fields_help_text_is_correct(self, field, placeholder_test):
        form = RegisterForm()
        help_text = form.fields[field].help_text
        self.assertEqual(help_text, placeholder_test)

    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password')
    ])
    def test_fields_label_is_correct(self, field, placeholder_test):
        form = RegisterForm()
        help_text = form.fields[field].label
        self.assertEqual(help_text, placeholder_test)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'StrongP@assword1',
            'password2': 'StrongP@assword1',
        }
        return super(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'Email is required'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please repeat your password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have at least for characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_min_length_should_be_less_than_150_characters(self):
        def characters(qty):
            string = []
            for i in range(qty):
                string.append(f'{i}')
            return ''.join(string)

        self.form_data['username'] = characters(qty=150)
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have less than 150 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
