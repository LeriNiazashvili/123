from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="კატეგორიის სახელი")

    class Meta:
        verbose_name_plural = "კატეგორიები"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="პროდუქტის სახელი")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ფასი")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="სურათი")
    is_discounted = models.BooleanField(default=False, verbose_name="ფასდაკლება აქვს?")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name="კატეგორია"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "პროდუქტები"

    def __str__(self):
        return self.name
