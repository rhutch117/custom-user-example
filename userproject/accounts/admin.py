from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models import UserAccount


class AccountCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ["email"]

    def save(self, commit=True) -> UserAccount:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AccountChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserAccount
        fields = ["email", "password", "is_active", "is_admin"]


class UserAdmin(BaseUserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm

    list_display = ("email", "is_staff", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = [
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_admin",)}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ("wide"),
                "fields": ("email", "name", "password"),
            },
        ),
    ]
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(UserAccount, UserAdmin)
admin.site.unregister(
    Group
)  # since we aren't using django's built-in permissions, unregister Group model
