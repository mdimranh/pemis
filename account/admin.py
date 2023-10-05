from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.utils.html import format_html
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import (PhoneNumberPrefixWidget,
                                       RegionalPhoneNumberWidget)

from .models import User, Verify


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    phone = PhoneNumberField(region="BD", widget=PhoneNumberPrefixWidget(country_choices=[('+880', "BD +880")]))

    class Meta:
        model = User
        fields = ('email', 'phone', 'password', 'is_active')
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    def user_profile(self, obj):
        if obj.picture and obj.picture.file:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />'.format(obj.picture.url))
        else:
            return format_html('<img src=""/>')

    user_profile.short_description = 'Image'

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('full_name', 'user_profile', 'email', 'phone', 'is_staff', 'is_active', 'last_login', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('full_name', 'email', 'phone', 'password', 'is_active', 'picture')}),
        ('Permissions', {'fields': ('is_staff', 'groups', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'phone')
    ordering = ('email',)

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Verify)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)