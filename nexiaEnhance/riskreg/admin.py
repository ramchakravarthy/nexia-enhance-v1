from django.contrib import admin
from riskreg.models import RiskRegister, RCA, QuillPost, NonQuillPost

# Register your models here.

admin.site.register(RiskRegister)
admin.site.register(RCA)
admin.site.register(QuillPost)
admin.site.register(NonQuillPost)
