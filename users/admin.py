from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Transaction, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'color', 'user')
    list_filter = ('type',)
    search_fields = ('name', 'user__username')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'amount', 'category', 'date')
    list_filter = ('type', 'date')
    search_fields = ('user__username', 'description')
    ordering = ('-date',)