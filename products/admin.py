from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("image_preview",)
    list_display = (
        'name',
        'get_categories',
        'price',
        'image_preview',
    )

    ordering = ('name',)

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.category.all()])


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
