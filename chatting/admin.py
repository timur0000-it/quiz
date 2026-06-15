from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Room)
class SellerAdmin(admin.ModelAdmin):
    model = Room

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    model = Answer