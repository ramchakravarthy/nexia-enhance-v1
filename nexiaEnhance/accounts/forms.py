from django import forms
from accounts.models import Firm, User, UserAttributes

# TODO: Delete the following commented lines
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm

# User form

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

# User attributes form

class CreateUserAttributesForm(forms.ModelForm):
    class Meta:
        model = UserAttributes
        fields = ['user_role', 'firm_name', 'profile_pic', 'is_viewer', 'is_preparer', 'is_reviewer',
                  'is_ult_authority', 'is_user_manager', 'is_nexia_reviewer', 'is_nexia_superuser', ]

# TODO: Delete the following commented lines
# class CreateNexiaSuperUserAttributesForm(forms.ModelForm):
#     firm_name = forms.CharField(initial='Nexia International', disabled=True)
#     user_role = forms.CharField(initial='nexia_superuser', disabled=True)
#
#     class Meta:
#         model = UserAttributes
#         fields = ['user_role', 'firm_name', 'profile_pic']
#
#
# class CreateNexiaUserAttributesForm(forms.ModelForm):
#     firm_name = forms.CharField(initial='Nexia International', disabled=True)
#     user_role = forms.CharField(initial='Nexia user', disabled=True)
#
#     class Meta:
#         model = UserAttributes
#         fields = ['user_role', 'firm_name', 'profile_pic']
#
#
# class CreateFirmITAdminUserAttributesForm(forms.ModelForm):
#     user_role = forms.CharField(initial='IT administrator', disabled=True)
#
#     class Meta:
#         model = UserAttributes
#         fields = ['user_role', 'firm_name', 'profile_pic']













# class UserCreateForm(UserCreationForm):
#     user_role_choices = [
#         ('staff', 'Staff'),
#         ('reviewer', 'Reviewer'),
#         ('ult_resp', 'Ultimate responsibility'),
#         ('admin', 'Nexia Enhance administrator'),
#         # ('IT_admin', 'IT administrator'),
#     ]
#     user_role = forms.ChoiceField(choices=user_role_choices)
#
#     class Meta:
#         fields = ('first_name', 'last_name', 'email', 'username')
#         # fields = ("username", "email", "password1", "password2")
#         model = get_user_model()
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.fields["username"].label = "Username/email"
#         # self.fields["email"].label = "Email address"


# class UserCreateForm2_1(forms.ModelForm):
#     class Meta:
#         fields = ('first_name','last_name',"username",'firm_name')
#         model = User
#
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     self.fields["username"].label = "Username"
#     #     # self.fields["email"].label = "Email address"


# class UserCreateForm2(UserCreationForm):
#     user_role_choices = [
#         ('staff', 'Staff'),
#         ('reviewer', 'Reviewer'),
#         ('ult_resp', 'Ultimate responsibility'),
#         ('admin', 'Nexia Enhance administrator'),
#         # ('IT_admin', 'IT administrator'),
#     ]
#     user_role = forms.ChoiceField(choices=user_role_choices)
#
#     class Meta:
#         fields = ('first_name', 'last_name', "username")
#         model = get_user_model()
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["username"].label = "Username"
#         # self.fields["email"].label = "Email address"

#
# class UserCreateForm(UserCreationForm, forms.ModelForm):
#     class Meta:
#         firms = Firm.objects.values('firm_name')
#         firm_name = forms.ChoiceField(choices=firms)
#         fields = ("username", "email", "password1", "password2")
#         model = get_user_model()
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["username"].label = "Display name"
#         self.fields["email"].label = "Email address"

# class CreateITAdminUserForm(forms.ModelForm):
#
#     user_role_choices = [
#         ('staff', 'Staff'),
#         ('reviewer', 'Reviewer'),
#         ('ult_resp', 'Ultimate responsibility'),
#         ('admin', 'Nexia Enhance administrator'),
#         ('IT_admin', 'IT administrator'),
#     ]
#     user_role = forms.ChoiceField(choices=user_role_choices)
#
#     class Meta:
#
#         model = User
#         fields = ['first_name','last_name','email', 'firm_name']

# def __int__(self):
#     super(CreateUserForm, self).__int__(**kwargs)
