from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(CustomerUser)
class CategoryAdmin(admin.ModelAdmin):
    model = CustomerUser

@admin.register(ActivationCode)
class ActivationCodeAdmin(admin.ModelAdmin):
    model = ActivationCode
   