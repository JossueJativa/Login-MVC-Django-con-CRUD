from django.db import models

# Create your models here.
class products(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    photo = models.ImageField(upload_to='products', null=True, blank=True)

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None