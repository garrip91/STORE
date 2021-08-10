from django.contrib import admin

from .models import ProductCategory, Product, Basket


# Register your models here.
admin.site.register(ProductCategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'image', 'description', 'short_description', ('price', 'quantity'), 'category')
    readonly_fields = ('short_description',)
    ordering = ('name',)
    search_fields = ('name',)

admin.site.register(Basket)
class BasketAdminInline(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('product', 'created_timestamp',)
    #extra = 0