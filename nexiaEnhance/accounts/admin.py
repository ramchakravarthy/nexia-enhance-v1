from django.contrib import admin

from accounts.models import Firm, User, UserAttributes
# Register your models here.

admin.site.register(User)
admin.site.register(Firm)
admin.site.register(UserAttributes)
