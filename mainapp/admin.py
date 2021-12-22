from django.contrib import admin

from mainapp.models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
