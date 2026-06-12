from django.contrib import admin
from .models import Category, Product, RFQSubmission

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(RFQSubmission)