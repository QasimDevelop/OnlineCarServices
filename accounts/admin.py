from django.contrib import admin

# Register your models here.
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('username','email','role')
    list_filter=('role',)
    search_fields=('username','email')
    list_per_page=10
    list_editable=('role',)
    list_display_links=('username','email')
    list_max_show_all=100