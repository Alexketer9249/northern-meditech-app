from django.db import models

# 1. Category Table (e.g., Surgical, Imaging)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True) # URL-friendly name

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# 2. Product Table (The Medical Equipment)
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    model_number = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    specifications = models.TextField(help_text="Detailed technical specs")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.name} ({self.model_number})"

# 3. RFQ Table (Leads from Customers)
class RFQSubmission(models.Model):
    institution = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    details = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RFQ from {self.institution}"