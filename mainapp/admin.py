from django.contrib import admin

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    exclude = ('password',)

admin.site.register(Reviews)
admin.site.register(Order)
admin.site.register(Rating)
