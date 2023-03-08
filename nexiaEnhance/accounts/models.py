from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Django's User Model
class User(auth.models.User, auth.models.PermissionsMixin, models.Model):

    def __str__(self):
        return "@{}".format(self.username)

# Firm Model
class Firm(models.Model):
    firm_id = models.AutoField(primary_key=True)
    firm_name = models.CharField(max_length=200, null=False, unique=False)
    firm_domain = models.CharField(max_length=200, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return str(self.firm_name)

    def get_absolute_url(self):
        return reverse('accounts:view-firms')

# Additional User Attributes Model
class UserAttributes(models.Model):
    # Create a user relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional attributes
    firm_name = models.ForeignKey(Firm, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    # User rights
    is_viewer = models.BooleanField(default=False)  # Can view risk register
    is_preparer = models.BooleanField(default=False)  # Can prepare risk register
    is_reviewer = models.BooleanField(default=False)  # Can prepare and review risk register
    is_ult_authority = models.BooleanField(
        default=False)  # Can prepare and review risk register. Can also prepare annual declaration
    is_user_manager = models.BooleanField(
        default=False)  # Can add users. Cannot view risk register or annual declarations.
    is_nexia_reviewer = models.BooleanField(default=False)  # Can view and review risks. Cannot prepare risks.
    is_nexia_superuser = models.BooleanField(default=False)  # Can do everything

    user_role = models.CharField(
        max_length=20,
        choices=[
            ('preparer', 'Preparer'),  # Should not be able to add new users. Can only prepare risks.
            ('reviewer', 'Reviewer'),  # Should not be able to add new users. Can prepare and review risks.
            ('ult_resp_auth', 'Ultimate responsible authority'),
            # Should not be able to add new users. Can prepare and review risks. Can sign off annual declaration.
            ('nexia_enhance_admin', 'Nexia Enhance administrator'),
            # Should be able to add new users. Can prepare and review risks. May be able to sign off annual declaration.
            ('IT_admin', 'IT administrator'),  # Should be able to add new users. Cannot view, prepare or review risks.
            ('nexia_user', 'Nexia user'),
            # Should not be able to add new users. Can only view risks. Cannot prepare or review risks.
            ('nexia_superuser', 'Nexia superuser'),  # Should be able to add new users. Can prepare and review risks.
        ],
        default='staff',
    )

    def __str__(self):
        return "@{}".format(self.user.username)

    def get_absolute_url(self):
        return reverse('accounts:view-users')
