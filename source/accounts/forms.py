from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from urllib.parse import urlparse

from accounts.models import Profile


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False, label='First name')
    last_name = forms.CharField(max_length=100, required=False, label='Last name')
    username = forms.CharField(max_length=100, required=True, label='Username')
    password = forms.CharField(max_length=100, required=True, label='Password',
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=100, required=True, label='Password confirm',
                                       widget=forms.PasswordInput)
    email = forms.EmailField(required=True, label='Email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise ValidationError('Username already taken.', code='username_taken')
        except User.DoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise ValidationError('Email already registered.', code='email_registered')
        except User.DoesNotExist:
            return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name.strip() == '':
            raise ValidationError('First name cannot be empty', code='first_name_empty')
        return first_name

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_confirm')
        if password_1 != password_2:
            raise ValidationError('Passwords do not match.', code='passwords_do_not_match')
        return self.cleaned_data


class UserChangeForm(forms.ModelForm):

    avatar = forms.ImageField(label='Аватар', required=False)
    birth_date = forms.DateField(label='День рождения', input_formats=['%Y-%m-%d', '%d.%m.%Y'], required=False)
    gitProfile = forms.URLField(label='git profile', required=False)
    about = forms.CharField(label='about', required=False, widget=forms.Textarea)

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.profile_fields:
            return getattr(self.instance.profile, field_name)
        return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.profile = self.save_profile(commit)
        return user

    def save_profile(self, commit=True):
        profile, _ = Profile.objects.get_or_create(user=self.instance)
        for field in self.Meta.profile_fields:
            setattr(profile, field, self.cleaned_data.get(field))
        if not profile.avatar:
            profile.avatar = None
        if commit:
            profile.save()
        return profile

    def clean_gitProfile(self):
        url = self.cleaned_data.get('gitProfile')
        check_url = urlparse(url)
        print(check_url.netloc)
        if url:
            if check_url.netloc == 'github.com':
                return url
            raise ValidationError('It is not a link to github profile', code='invalid_github_url')
        return None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gitProfile', 'about']
        profile_fields = ['avatar', 'birth_date', 'gitProfile', 'about']


class UserChangePasswordForm(forms.ModelForm):
    password = forms.CharField(max_length=100, required=True, label='New Password',
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=100, required=True, label='New Password confirm',
                                       widget=forms.PasswordInput)
    old_password = forms.CharField(max_length=100, required=True, label='Old Password',
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.instance
        if not user.check_password(old_password):
            raise ValidationError('Invalid password.', code='invalid_password')
        return old_password

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_confirm')
        if password_1 != password_2:
            raise ValidationError('Passwords do not match.', code='passwords_do_not_match')
        return self.cleaned_data

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'old_password']


class UserPasswordResetForm(forms.ModelForm):
    password = forms.CharField(max_length=100, required=True, label='New Password',
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=100, required=True, label='New Password confirm',
                                       widget=forms.PasswordInput)

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_confirm')
        if password_1 != password_2:
            raise ValidationError('Passwords do not match.', code='passwords_do_not_match')
        return self.cleaned_data

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = []