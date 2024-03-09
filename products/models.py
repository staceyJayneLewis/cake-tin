from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def show_display_name(self):
        return self.display_name


class Product(models.Model):
    category = models.ManyToManyField('Category')
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    nutritional = models.TextField(null=True)
    allergen = models.TextField(null=True)
    # sale item
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def image_preview(self):
        from django.utils.html import format_html
        if self.image:
            return format_html(f"<img src='{self.image.url}' height='150'>")
        else:
            return format_html(
                f"<img src='../../../media/no_image.png' height='150'>")

    def __str__(self):
        return self.name
