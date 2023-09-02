from django.contrib import admin
from Users.models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email',
                    'dob', 'created_on', 'phone', 'gender']
