from django.contrib import admin

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Customer)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("f_name",)}


admin.site.register(Reviews)
admin.site.register(Rating)
