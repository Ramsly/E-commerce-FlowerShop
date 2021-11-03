from django.contrib import admin

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    exclude = ("search_vector",)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    exclude = ('password',)

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     exclude = ('products_wishlist',)


admin.site.register(Reviews)
admin.site.register(Rating)
