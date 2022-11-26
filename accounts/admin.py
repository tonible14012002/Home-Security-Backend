from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import MyUser, Visit
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.admin import ModelAdmin, TabularInline
# Register your models here.

class VisitInline(TabularInline):
    model = Visit
    readonly_fields = ('time',)

@admin.register(MyUser)
class CustomUserAdmin(UserAdmin):
    inlines = [VisitInline]
    add_form = UserCreationForm
    form = UserChangeForm
    model = MyUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'image', 'created_at', 'updated_at')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'image',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        (None, {'fields': ('first_name', 'last_name')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 
                       'is_staff', 'is_active', 'image', 'phone', 'address')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

@admin.register(Visit)
class VisitAdmin(ModelAdmin):
    list_display = ('time', 'user')
    
