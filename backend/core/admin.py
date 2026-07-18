from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Analysis,Review
admin.site.register(User,UserAdmin); admin.site.register(Analysis); admin.site.register(Review)
