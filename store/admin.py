from django.contrib import admin
from .models import Stock, Category, StockHistory
from .forms import StockCreateForm

# Register your models here.
class StockCreateAdmin(admin.ModelAdmin):
   list_display = ['category', 'item_name', 'quantity']
   form = StockCreateForm
   list_filter = ['category']
   search_fields = ['category', 'item_name']

admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category)
admin.site.register(StockHistory)