from django import forms
from django.contrib.auth.models import User
from.models import Profile
from complaints.models import Department


class ResidentRegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    confirm_password = forms.CharField(widget=forms.PasswordInput)

    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class StaffRegisterForm(forms.ModelForm):

   
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department"
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username'
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password'])

        department = self.cleaned_data['department']

        user.email = department.email or ''

        if commit:
            user.save()

            Profile.objects.create(
                user=user,
                role='staff',
                department=department
            )

        return user